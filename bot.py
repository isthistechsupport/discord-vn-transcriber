import os
import socket
import logging
import discord
import requests
from io import BytesIO
from dotenv import load_dotenv
from logging.handlers import SysLogHandler


load_dotenv()


class ContextFilter(logging.Filter):
    hostname = socket.gethostname()
    def filter(self, record):
        record.hostname = ContextFilter.hostname
        return True
    

syslog = SysLogHandler(address=(os.getenv('LOG_DESTINATION', 'localhost'), int(os.getenv('LOG_PORT', '514'))), facility=SysLogHandler.LOG_USER)
syslog.addFilter(ContextFilter())
format = '%(asctime)s %(hostname)s %(levelname)s discord_transcriber: %(message)s'
formatter = logging.Formatter(format, datefmt='%b %d %H:%M:%S')
syslog.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(syslog)
logger.setLevel(logging.INFO)


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


def extract_message_metadata(message: discord.Message, attachment: discord.Attachment) -> tuple:
    message_id = message.id
    message_author = message.author.name
    attachment_id = attachment.id
    attachment_content_type = attachment.content_type
    attachment_size = attachment.size
    return message_id, message_author, attachment_id, attachment_content_type, attachment_size


def validate_mime_type(audio_mime_type: str) -> bool:
    valid_mime_types = ['flac', 'mp3', 'mp4', 'mpeg', 'mpga', 'm4a', 'ogg', 'wav', 'webm']
    return any(mime_type in audio_mime_type for mime_type in valid_mime_types)


def transcribe_audio(audio_buffer: BytesIO, audio_mime_type: str) -> str:
    headers = {
        'Authorization': f"Bearer {os.getenv('OPENAI_API_KEY')}",
    }
    files = {
        'file': ('audio', audio_buffer, audio_mime_type),
        'model': (None, 'whisper-1'),
        'temperature': (None, '0.7'),
    }
    response = requests.post('https://api.openai.com/v1/audio/transcriptions', headers=headers, files=files)
    return response.json()['text']


async def process_audio(audio_attachment: discord.Attachment) -> str:
    file_mime_type, file_size = audio_attachment.content_type, audio_attachment.size
    if not validate_mime_type(file_mime_type):
        return f"Sorry, this attachment's audio format is invalid. The valid formats are: flac, mp3, mp4, mpeg, mpga, m4a, ogg, wav, and webm. This attachment's audio format is: `{file_mime_type}`"
    if file_size > 25 * 1024 * 1024:
        return f"Sorry, this attachment's size is too large. The maximum size allowed is: 25 MB. This attachment's size is: ```{file_size} bytes, {file_size / (1024 * 1024)} MB```"
    audio_bytes = await audio_attachment.read()
    with BytesIO(audio_bytes) as audio_file:
        transcription = transcribe_audio(audio_file, file_mime_type)
        return transcription


@client.event
async def on_ready():
    logging.info(f'Logged in as {client.user} (ID: {client.user.id})')


@client.event
async def on_message(message: discord.Message):
    if message.author.id == client.user.id: # we do not want the bot to reply to itself
        return
    if len(message.attachments) > 0:
        for attachment in message.attachments:
            if 'audio' in attachment.content_type:
                message_id, message_author, attachment_id, attachment_content_type, attachment_size = extract_message_metadata(message, attachment)
                logging.info(f"Processing audio attachment {message_id=}, {message_author=}, {attachment_id=}, {attachment_content_type=}, {attachment_size=} bytes")
                try:
                    transcription = await process_audio(attachment)
                    await message.reply(f"This message says: {transcription}")
                except Exception as e:
                    logging.error(e, stack_info=True, exc_info=True)
                    await message.reply("Sorry, an error occurred while processing this attachment. Please try again later.")
                    

client.run(os.getenv('DISCORD_BOT_TOKEN'))

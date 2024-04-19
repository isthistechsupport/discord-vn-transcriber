# Discord Voicenote Transcriber

This is a dockerized Python project that uses the Discord.py and the OpenAI speech-to-text Whisper 2 Model to return the transcription of any audio messages and voice notes that you send to it, or to any server where the bot is present to (and has permissions to read and send messages to).

## Installation

### Prerequisites

- Docker

- A Papertrail log destination to log the function output to. If you don't have one, you'll need to log into (or create an account on) Papertrail, [create a new log destination](https://papertrailapp.com/destinations/new). Save the destination URL and port number.

- A Discord Bot Account with an associated static token and the Message Content Intent enabled. If you don't have a Discord bot account, follow [this guide](https://discordpy.readthedocs.io/en/latest/discord.html). If you don't know how to enable intents, follow [this guide](https://discordpy.readthedocs.io/en/latest/intents.html)

- A OpenAI developer account and a related OpenAI project API key. If you don't have an OpenAI developer account, use [this guide](https://platform.openai.com/docs/quickstart?context=python) to get started. Once you're done with the "Account setup" instructions and have created a secret key, save the key value.

### Setup

- Clone this repo

- Rename the `.env.template` file to `.env` and fill in the blanks

  - `DISCORD_BOT_TOKEN` must be your Discord Bot Account static token

  - `OPENAI_API_KEY` has to be your OpenAI API key.

  - `PAPERTRAIL_LOG_DESTINATION` needs to be your Papertrail log destination URL.

  - `PAPERTRAIL_LOG_PORT` must be your Papertrail log destination port.

- Build the docker image and run it. If you don't have any particular requirements, you can paste in your terminal `source run.sh`. It will build the Docker image, tag it, prune any dangling images, and run the container in interactive mode with networking enabled and removal on stop. Don't forget to detach from the container (usually by pressing Ctrl + P Ctrl + Q on Windows/Linux or Cmd + P Cmd + Q on Mac) before closing the terminal window.

- Done! You should now see the transcription of any audios or voice notes you send to the bot, or on any channel that the bot has access to.

## License

This code is open sourced under the [MIT license](https://github.com/isthistechsupport/vn_webhooks/blob/main/LICENSE.md)

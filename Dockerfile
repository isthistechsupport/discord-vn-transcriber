FROM python:3.11-slim

COPY requirements.txt .
COPY .env .
COPY bot.py .

RUN pip install -r requirements.txt --trusted-host pypi.python.org --no-cache-dir

CMD [ "python", "bot.py" ]

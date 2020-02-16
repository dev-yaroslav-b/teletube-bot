FROM python:3.7-alpine

RUN apk add --no-cache gcc libffi-dev musl-dev openssl-dev ffmpeg

RUN pip install --upgrade pip
COPY requirements.txt /teletube_bot/requirements.txt
RUN pip install -r /teletube_bot/requirements.txt

RUN mkdir teletube_bot
COPY . teletube_bot/

WORKDIR teletube_bot
CMD python main.py
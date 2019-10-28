# Telegram Bot
Telegram bot created with:
1. [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) as bot core
2. [youtube-dl](https://github.com/ytdl-org/youtube-dl) for downloading audio files 
3. [pydub](https://github.com/jiaaro/pydub) for splitting audio files

It allows you:
1. Download single audio or playlists file from youtube
2. Download separated audio files as podcast parts from youtube 
3. Recommend similar songs using [last.fm api](https://www.last.fm/api/)
4. Send everything to telegram

## Installation
Clone repo:
```
git clone https://github.com/dev-yaroslav-b/teletube-bot.git
```
Create virtual env:
```
cd teletube-bot
virtualenv --python=python3.7 venv
```
Activate venv:
```
source venv/bin/activate
```
Install requirements:
```
pip install -r requirements.txt 
```
Create required dirs:
```
mkdir bot/audio bot/logs
```
Start server:
```
python main
```
And that is it!

## TDB
1. Add tests
2. Add webhook version

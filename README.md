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
Unix:
```
source venv/bin/activate
```
Windows:
```
venv\Scripts\activate
```
Install requirements:
```
pip install -r requirements.txt 
```
Install ffmpeg for Mac `brew install ffmpeg` or [Windows](http://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/)

Don't forget to add your tokens:
```
export TOKEN=TELEGRAM_BOT_TOKEN  
exportLAST_FM_API_TOKEN=LAST_FM_API_TOKEN
```
Start bot:
```
python main
```

Or run it using `docker-compose`:

Create `.env` file and fill it according to the `.env.template`

And run: 

```
docker-compose up
```

And that is it!

import json
import os
import re

import youtube_dl
import requests
from pydub import AudioSegment


def download_audio_or_playlist(audio_dir: str, url: str):
    """
    Download audio file or playlist with url to `chat_id` directory
    :param audio_dir: path to audio directory
    :param url: url with audio file or playlist
    :return:
    """
    # Create audio directory for user otherwise skip
    try:
        os.mkdir(audio_dir)
    except OSError:
        print("Directory %s already exists" % audio_dir)
    else:
        print("Successfully created the directory %s " % audio_dir)

    # YoutubeDL options
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        "outtmpl": audio_dir + '/%(title)s.%(ext)s',
    }
    # Downloader
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def clean(audio_dir: str):
    """
    Clean user`s directory
    :param audio_dir: path to audio directory
    :return: formatted result string
    """
    for filename in os.listdir(audio_dir):
        os.remove(os.path.join(audio_dir, filename))
    return f"{audio_dir} successfully cleaned"


def recommend_song(artist: str, track: str):
    """
    Gather recommendation from LastFM api(Api token required) using user`s params
    :param artist: handled artist
    :param track: handled track
    :return: list contains 3 most popular similar songs
    """
    api_token = os.environ.get('LAST_FM_API_TOKEN')
    url = f"http://ws.audioscrobbler.com/2.0/?method=track.getsimilar&artist={artist}&track={track}&api_key={api_token}&format=json"

    response = requests.get(url)
    data = json.loads(response.text)
    most_common = []
    if data.get('error') is None:
        for d in data['similartracks']['track']:
            most_common.append(
                [d['artist']['name'], d['name'], d['url'], d['playcount']])

        return sorted(most_common, key=lambda x: x[-1])[-3:]
    else:
        return None


def hours_minutes_seconds_to_milliseconds(milliseconds: int, time_code: list):
    """
    Convert hours, minutes, seconds to milliseconds
    1 second - 1000 mils | 1 minute = 60 000 mils | 3 600 000 000 mils
    :param milliseconds: current milliseconds
    :param time_code: list of time codes
    :return: milliseconds
    """
    if len(time_code) == 0:
        return milliseconds
    elif len(time_code) == 1:
        milliseconds += time_code[0] * 1000
        time_code.pop(0)
        return hours_minutes_seconds_to_milliseconds(milliseconds, time_code)
    else:
        milliseconds += time_code[0] * 60000
        time_code.pop(0)
        return hours_minutes_seconds_to_milliseconds(milliseconds, time_code)


def handle_time_codes(time_codes: str):
    """
    Transform user`s input to list of time codes in milliseconds
    :param time_codes: raw str contains time codes
    :return: list of time codes in milliseconds
    """
    pattern = '(\d*:\d*:\d*|\d*:\d*)'
    time_codes = re.sub('\\n', '', time_codes)
    time_codes = [x for x in re.findall(pattern, time_codes) if len(x) > 1]
    time_codes_millis = []
    for time_code in time_codes:
        milliseconds = 0
        m = hours_minutes_seconds_to_milliseconds(milliseconds,
                                                  [int(_) for _ in
                                                   time_code.split(':')])
        time_codes_millis.append(m)
    time_codes_millis.insert(0, 0)
    return time_codes_millis


def split_file(time_codes: list, audio_dir: str):
    """
    Split audio file to multiple audio files with time codes
    :param time_codes: list of time_codes in milliseconds
    :param audio_dir: path to audio directory
    :return: dict contains - part_number: file_name
    """
    filename_parts = {}
    for filename in os.listdir(audio_dir):
        sound = AudioSegment.from_file(os.path.join(audio_dir, filename))
        for i in range(len(time_codes) - 1):
            part = sound[time_codes[i]:time_codes[i + 1]]
            filename_parts[i] = f'Part{i} - {filename}'
            part.export(os.path.join(audio_dir, filename_parts[i]),
                        format='mp3')
        os.remove(os.path.join(audio_dir, filename))
    return filename_parts

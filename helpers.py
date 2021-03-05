import math
import datetime


def song_json_to_tuple(raw_json):
    album_name = raw_json['album']['name']
    artist_name = raw_json['artists'][0]['name']
    song_name = raw_json['name']
    song_duration = raw_json['duration_ms']
    return (song_name, artist_name, album_name, song_duration)


def items_to_ids(i):
    res = []
    for j in i:
        res.append(j["id"])
    return res


def items_to_songs(i):
    song_list = []
    for song_json in i:
        song_list.append(song_json_to_tuple(song_json))
    return song_list


def items_to_artists(i):
    artist_list = []
    for artist_json in i:
        artist_list.append(artist_json['name'])
    return artist_list


def get_date():
    return str(datetime.date.today())[2:].replace("-", "")


def format_date(original):
    MONTHS = {
        "01": "January",
        "02": "February",
        "03": "March",
        "04": "April",
        "05": "May",
        "06": "June",
        "07": "July",
        "08": "August",
        "09": "September",
        "10": "October",
        "11": "November",
        "12": "December"
    }
    year = "20" + original[0:2]
    day = original[-2:]
    month = MONTHS[original[2:4]]
    return month + " " + day + ", " + year


if __name__ == '__main__':
    pass

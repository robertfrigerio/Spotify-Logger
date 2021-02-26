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


if __name__ == '__main__':
    pass

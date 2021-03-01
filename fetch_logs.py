import spotipy
from spotipy.oauth2 import SpotifyOAuth
import datetime
import helpers
import os
from dotenv import load_dotenv


def check_date(t):
    log_file = open('./logs/completed_dates.txt', 'r')
    first_line = log_file.readline()
    date_from_file = first_line.split(";")[:-1][-1]
    # if date already in file, script will not execute, returns True
    return date_from_file == t


def setup():
    load_dotenv()
    try:
        os.makedirs("./logs/id/")
        os.mkdir("./logs/verbose")
    except:
        pass
    scope = "user-library-read user-top-read"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    frames = ['short_term', 'medium_term', 'long_term']
    return scope, sp, frames


if __name__ == "__main__":
    TODAY = str(datetime.date.today())
    if check_date(TODAY):
        print("Logs already contain data for today\t", TODAY,
              "\nTerminating...")
        exit()
    scope, sp, frames = setup()
    for frame in frames:
        t_list = sp.current_user_top_tracks(limit=50,
                                            time_range=frame)['items']
        a_list = sp.current_user_top_artists(limit=50,
                                             time_range=frame)['items']

        song_ids = helpers.items_to_ids(t_list)
        artist_ids = helpers.items_to_ids(a_list)

        id_t_res = TODAY + "|"
        for i, song in enumerate(song_ids):
            id_t_res += str(i + 1) + ";" + song + "|"
        id_t_res += "\n"
        id_f_t = open("./logs/id/{}_tracks_ids.txt".format(frame), "a")
        id_f_t.write(id_t_res)
        id_f_t.close()

        id_a_res = TODAY + "|"
        for i, artist in enumerate(artist_ids):
            id_a_res += str(i + 1) + ";" + artist + "|"
        id_a_res += "\n"
        id_f_a = open("./logs/id/{}_artists_ids.txt".format(frame), "a")
        id_f_a.write(id_a_res)
        id_f_a.close()

        song_list = helpers.items_to_songs(t_list)
        v_t_res = TODAY + "|"
        # (song_name, artist_name, album_name, song_duration, index)
        for i, song in enumerate(song_list):
            v_t_res += str(i+1) + ";" + song[1] + ";" + \
                song[0] + ";" + song[2] + "|"
        v_t_res += "\n"
        v_f_t = open("./logs/verbose/{}_tracks.txt".format(frame), "a")
        v_f_t.write(v_t_res)
        v_f_t.close()

        artist_list = helpers.items_to_artists(a_list)
        v_a_res = TODAY + "|"
        for i, artist in enumerate(artist_list):
            v_a_res += str(i + 1) + ";" + artist + "|"
        v_a_res += "\n"
        v_f_a = open("./logs/verbose/{}_artists.txt".format(frame), "a")
        v_f_a.write(v_a_res)
        v_f_a.close()
    with open('./logs/completed_dates.txt', "a") as d:
        d.write(TODAY + ";")
    print("Successfully updated all logs\t", TODAY)

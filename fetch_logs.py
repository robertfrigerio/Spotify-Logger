import spotipy
from spotipy.oauth2 import SpotifyOAuth
import datetime
import helpers
import os
from dotenv import load_dotenv


def check_date(t):
    log_file = open('./logs/completed_dates.txt', 'r')
    first_line = log_file.readline()
    date_from_file = first_line.split(",")[:-1][-1]
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
    TODAY = helpers.get_date()
    if check_date(TODAY):
        print("Logs already contain data for", helpers.format_date(TODAY),
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
        song_list = helpers.items_to_songs(t_list)
        artist_list = helpers.items_to_artists(a_list)
        n_artists = len(artist_ids)
        n_tracks = len(song_ids)

        # log artists
        id_a_res = TODAY + ","
        verbose_artists_res = TODAY + '|'
        id_f_a = open("./logs/id/{}_artists_ids.txt".format(frame), "a")
        verbose_a_f = open("./logs/verbose/{}_artists.txt".format(frame), "a")

        for i in range(n_artists):
            id_a_res += artist_ids[i] + ","
            verbose_artists_res += artist_list[i] + "|"

        id_a_res += "\n"
        verbose_artists_res += "\n"
        id_f_a.write(id_a_res)
        verbose_a_f.write(verbose_artists_res)

        id_f_a.close()
        verbose_a_f.close()
        # done artists

        # log tracks
        id_t_res = TODAY + ","
        verbose_tracks_res = TODAY + "|"
        id_f_t = open("./logs/id/{}_tracks_ids.txt".format(frame), "a")
        verbose_t_f = open("./logs/verbose/{}_tracks.txt".format(frame), "a")

        for j in range(n_tracks):
            id_t_res += song_ids[j] + ","
            verbose_tracks_res += str(j+1) + ";" + song_list[j][1] + ";" + \
                song_list[j][0] + ";" + song_list[j][2] + "|"

        id_t_res += "\n"
        verbose_tracks_res += "\n"
        id_f_t.write(id_t_res)
        verbose_t_f.write(verbose_tracks_res)
        id_f_t.close()
        verbose_t_f.close()
        # done tracks

    with open('./logs/completed_dates.txt', "a") as d:
        d.write(TODAY + ",")
    print("Successfully updated all logs\t", helpers.format_date(TODAY))

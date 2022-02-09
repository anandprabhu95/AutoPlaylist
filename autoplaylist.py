from bs4 import BeautifulSoup
import urllib.request
import spotipy
from spotipy.oauth2 import SpotifyOAuth
# import json
import re
import datetime

playlist_id = '1pk6JmatgEFQKDGY0cOMPw'

def authorize():
    scope = 'playlist-modify-public'
    username = '21wrhzneviibcick6tnquhp4i'
    token = SpotifyOAuth(scope=scope, username=username)
    return token

def setup_data():
    response = urllib.request.urlopen("http://www2.radioparadise.com/rp3-mx.php?n=Playlist")
    data = response.read()
    return data

def song_list(content):
    soup = BeautifulSoup(content, 'lxml')
    # print(soup.prettify())
    list_of_songs = []
    song_cards = soup.find_all('div', class_=['p-row1', 'p-row2'])
    for songs in song_cards:
        song = songs.a.text
        song = song[5:].replace("-", "").strip(' ')
        song = song[2:]
        song = re.sub("\s\s+", " ", song)
        list_of_songs.append(song)
    list_of_songs = list(reversed(list_of_songs))
    list_of_songs = list_of_songs[4:]
    return list_of_songs

# Find Songs
def find_and_add_songs(playlistid):
    list_of_songs = song_list(setup_data())
    result_list = []
    remove_track_id = remove_all_songs(playlistid)
    for song in list_of_songs:
        result = spotifyObject.search(q=song, market='US')
        # print(json.dumps(result, sort_keys=4, indent=4))
        if result['tracks']['total'] == 0:
            pass
        else:
            if result['tracks']['items'][0]['uri'] in remove_track_id:
                pass
            else:
                if result['tracks']['items'][0]['artists'][0]['name'] in song:
                    result_list.append(result['tracks']['items'][0]['uri'])
    spotifyObject.playlist_add_items(playlist_id=playlistid, items=result_list)
    spotifyObject.playlist_change_details(playlist_id=playlist_id, name='AutoPlaylist: Main Mix',
                                          description=description_update())

# Remove all songs from the playlist
def remove_all_songs(playlistid):
    remove_track_result = spotifyObject.playlist_tracks(playlist_id=playlistid)
    # print(json.dumps(remove_track_result,sort_keys=4,indent=4))
    remove_track_id = []
    for i in range(0, remove_track_result['total']):
        remove_track = remove_track_result['items'][i]['track']['uri']
        remove_track_id.append(remove_track)
    spotifyObject.playlist_remove_all_occurrences_of_items(playlist_id=playlistid,
                                                           items=remove_track_id)
    return remove_track_id

def description_update():
    uptime = datetime.datetime.now()
    last_update_time = str('Last updated: ' + uptime.strftime('%b') + ' ' + uptime.strftime('%d')
                           + ', ' + uptime.strftime('%I') + ':' + uptime.strftime('%M') + ' ' + uptime.strftime('%p'))
    track_src = 'Track source: RP Main Mix'
    playlist_description = str(last_update_time)
    # print(playlist_description)
    return playlist_description


spotifyObject = spotipy.Spotify(auth_manager=authorize())
find_and_add_songs(playlist_id)
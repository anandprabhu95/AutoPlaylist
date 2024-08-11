This script updates a spotify playlist with music from Radio Paradise: Main Mix.

How:
1) Setup a 'Spotify for Developers' account to get the client_id and client_secret_key.
2) Create a playlist on spotify. Note the playlist_id of the playlist(Can be viewed on the link to the playlist or can be obtained using the tools on Spotify for Developers).
3) Export spotify environment variables:
Create a file named as 'spotipy_creds.sh' in the root of the repo with the following contents: 
```
!/usr/bin/env bash
echo Exporting spotify credentials as environment variables
export SPOTIPY_CLIENT_ID='your client id'
export SPOTIPY_CLIENT_SECRET='your client secret key'
export SPOTIPY_REDIRECT_URI=http://localhost:8000/callback/
export SPOTIFY_USERNAME='your spotify username'
export PLAYLIST_ID='your playlist id'
```
4) Create a cronjob that runs ```jobs.sh``` every hour like this
   ```0 * * * * $path_to_Autoplaylist/jobs.sh > $path_to_Autoplaylist/log.txt```

#!/usr/bin/env python3
import spotipy
from spotipy.oauth2 import SpotifyOAuth

index = 0
nextId = ''
array = []

def main():
    try:
        import config
        client_id = config.client_id
        client_secret = config.client_secret
        skips = config.skips
        run(client_id, client_secret, skips)
    except ModuleNotFoundError:
        print('No config found, please enter the following')
        f = open('config.py', 'w')
        client_id = input('Client ID: ')
        f.write("client_id = '" + client_id + "'\n")
        client_secret = input('Client secret: ')
        f.write("client_secret = '" + client_secret + "'\n")
        skips = input('Skips: ')
        f.write("skips = [" + skips + "]")
        f.close()
        print('Config saved, starting...')
        main()
    except KeyboardInterrupt:
        sortAlbums()
        print('EXIT')

def run(client_id, client_secret, skips):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri='https://localhost:8080',
        scope='user-library-read, user-follow-read'))
    currentLimit = 0

    artists = sp.current_user_followed_artists(limit=50)
    total = artists['artists']['total']
    getAlbums(total, skips, sp, artists)

    while currentLimit < total:
        currentLimit += 50
        artists = sp.current_user_followed_artists(limit=50, after=nextId)
        getAlbums(total, skips, sp, artists)
    sortAlbums()

def getAlbums(total, skips, sp, artists):
    global index, nextId
    for artist in artists['artists']['items']:
        artistName = artist['name']
        index += 1
        print(f'{index}/{total}: {artist['name']}')
        nextId = artist['id']
        if (artistName not in skips):
            albums = sp.artist_albums(artist['uri'], album_type='album')
            for album in albums['items']:
                array.append(album['release_date'].ljust(10) + ' - ' + artistName.ljust(24) + ' - ' + album['name'])

def sortAlbums():
    print()
    array.sort()
    for item in array:
        print(item)

if __name__ == "__main__":
    main()

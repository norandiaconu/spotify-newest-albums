#!/usr/bin/env python3
from yaspin import yaspin
spinner = yaspin()
spinner.text = "Config loading..."
spinner.start()

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
        spinner.stop()
        print('ERROR')
    except KeyboardInterrupt:
        sortAlbums()
        print('EXIT')

def run(client_id, client_secret, skips):
    spinner.text = "Loading..."
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri='http://127.0.0.1:8080',
        scope='user-library-read, user-follow-read'))
    currentLimit = 0

    artists = sp.current_user_followed_artists(limit=50)['artists']
    total = artists['total']
    getAlbums(total, skips, sp, artists)

    while currentLimit < total:
        currentLimit += 50
        artists = sp.current_user_followed_artists(limit=50, after=nextId)['artists']
        getAlbums(total, skips, sp, artists)
    sortAlbums()

def getAlbums(total, skips, sp, artists):
    global index, nextId
    for artist in artists['items']:
        artistName = artist['name']
        index += 1
        spinner.text = f'{index / total * 100:.0f}% ({index}/{total}) | {artistName}'
        nextId = artist['id']
        if (artistName not in skips):
            albums = sp.artist_albums(artist['uri'], album_type='album')
            for album in albums['items']:
                array.append(
                    ' \x1b[0;31;40m' + album['release_date'].ljust(10) +
                    ' \x1b[0;32;40m' + artistName.ljust(28) +
                    ' \x1b[0;33;40m' + album['name'] + '\x1b[0m'
                )

def sortAlbums():
    spinner.stop()
    print()
    array.sort()
    for item in array:
        print(item)

if __name__ == "__main__":
    main()

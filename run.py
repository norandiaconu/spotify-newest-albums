#!/usr/bin/env python3
import spotipy
from spotipy.oauth2 import SpotifyOAuth
array = []

def main():
    try:
        import config
        client_id = config.client_id
        client_secret = config.client_secret
        redirect_uri = config.redirect_uri
        skips = config.skips
        run(client_id, client_secret, redirect_uri, skips)
    except ModuleNotFoundError:
        print('ERROR')
    except KeyboardInterrupt:
        sortAlbums()
        print('EXIT')

def run(client_id, client_secret, redirect_uri, skips):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope='user-library-read, user-follow-read'))

    currentLimit = 0
    index = 0

    artists = sp.current_user_followed_artists(limit=50)
    total = artists['artists']['total']
    for idx, artist in enumerate(artists['artists']['items']):
        artistName = artist['name']
        index = index + 1
        print(f'{index}/{total}: {artist['name']}')
        nextId = artist['id']
        if (nextId not in skips):
            albums = sp.artist_albums(artist['uri'], album_type='album')
            for idx, album in enumerate(albums['items']):
                array.append(album['release_date'] + ' - ' + artistName + ' - ' + album['name'])

    while currentLimit < total:
        currentLimit = currentLimit + 50
        artists = sp.current_user_followed_artists(limit=50, after=nextId)
        for idx, artist in enumerate(artists['artists']['items']):
            artistName = artist['name']
            index = index + 1
            print(f'{index}/{total}: {artist['name']}')
            nextId = artist['id']
            if (nextId not in skips):
                albums = sp.artist_albums(artist['uri'], album_type='album')
                for idx, album in enumerate(albums['items']):
                    array.append(album['release_date'] + ' - ' + artistName + ' - ' + album['name'])
    sortAlbums()

def sortAlbums():
    print()
    array.sort()
    for idx, item in enumerate(array):
        print(item)

if __name__ == "__main__":
    main()

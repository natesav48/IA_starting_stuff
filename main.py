import spotipy
from spotipy.oauth2 import SpotifyOAuth

# These are my Spotify app credentials, they let me access Spotify API through PyCharm
CLIENT_ID = ''
CLIENT_SECRET = ''
REDIRECT_URI = ''

# This line will authenticate my program with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope='user-library-read'))
current_user = sp.current_user()
print(f"Authenticated as: {current_user['display_name']}")

# This is my function to find similar songs based on user input
def find_similar_songs(track_name, genre):
    # Here you can search for the track on Spotify
    results = sp.search(q=f'track:{track_name} genre:{genre}', type='track', limit=10)

    similar_songs = []
    for item in results['tracks']['items']:
        # Append only the name and artist to the similar_songs list
        similar_songs.append({
                'name': item['name'],
                'artist': item['artists'][0]['name']  # changed 'artists' key to 'artist'
            })
    return similar_songs

# Take user input for track name and genre
track_name = input("Enter the track name: ")
genre = input("Enter the genre: ")

# Find similar songs
songs = find_similar_songs(track_name, genre)

# Print only the song name and artist
for song in songs:
    print(f"{song['name']} by {song['artist']}")

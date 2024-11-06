# Button to fetch recommendations
import tkinter as tk
from tkinter import ttk, messagebox
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify API credentials
CLIENT_ID = ''
CLIENT_SECRET = ''
REDIRECT_URI = ''

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope='user-library-read'))
current_user = sp.current_user()
print("Authenticated as:", current_user['display_name'])


# Function to find similar songs based on user input and audio features
def find_similar_songs(track_name, genre, danceability, energy, valence):
    results = sp.search(q=f'track:{track_name} genre:{genre}', type='track', limit=1)
    if not results['tracks']['items']:
        messagebox.showerror("Error", "Track not found.")
        return []

    track_id = results['tracks']['items'][0]['id']
    recommendations = sp.recommendations(seed_tracks=[track_id], limit=10,
                                         target_danceability=danceability,
                                         target_energy=energy,
                                         target_valence=valence)

    similar_songs = []
    for item in recommendations['tracks']:
        similar_songs.append({
            'name': item['name'],
            'artist': item['artists'][0]['name']
        })
    return similar_songs


# Function to get user input and display recommended songs
def get_recommendations():
    track_name = track_entry.get()
    genre = genre_entry.get()
    danceability = danceability_slider.get() / 100  # Scale to 0-1 range
    energy = energy_slider.get() / 100
    valence = valence_slider.get() / 100

    if not track_name or not genre:
        messagebox.showerror("error, please enter trackname or genre")
        return

    # Find similar songs based on the input values
    songs = find_similar_songs(track_name, genre, danceability, energy, valence)
    if songs:
        results_text.delete(1.0, tk.END)  # Clear previous results
        for song in songs:
            results_text.insert(tk.END, f"{song['name']} by {song['artist']}\n")
    else:
        results_text.delete(1.0, tk.END)
        results_text.insert(tk.END, "No similar songs found.")


# Tkinter UI setup
root = tk.Tk()
root.title("Spotify Song Recommender")
root.geometry("400x500")

# Track name input
tk.Label(root, text="Track Name:").pack(pady=5)
track_entry = tk.Entry(root, width=30)
track_entry.pack(pady=5)

# Genre input
tk.Label(root, text="Genre:").pack(pady=5)
genre_entry = tk.Entry(root, width=30)
genre_entry.pack(pady=5)

# Danceability slider
tk.Label(root, text="Danceability (0-100):").pack(pady=5)
danceability_slider = ttk.Scale(root, from_=0, to=100, orient="horizontal")
danceability_slider.pack(pady=5)

# Energy slider
tk.Label(root, text="Energy (0-100):").pack(pady=5)
energy_slider = ttk.Scale(root, from_=0, to=100, orient="horizontal")
energy_slider.pack(pady=5)

# Valence slider
tk.Label(root, text="Valence (0-100):").pack(pady=5)
valence_slider = ttk.Scale(root, from_=0, to=100, orient="horizontal")
valence_slider.pack(pady=5)

# Button to fetch recommendations
recommend_button = tk.Button(root, text="Get Recommendations", command=get_recommendations)
recommend_button.pack(pady=20)

# Text area to display recommended songs
results_text = tk.Text(root, height=10, width=40)
results_text.pack(pady=5)

# Start Tkinter event loop
root.mainloop()

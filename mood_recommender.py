# mood_recommender.py

import requests
from spotify_auth import get_access_token

# Mood to Spotify playlist ID mapping
MOOD_PLAYLISTS = {
    "happy": ["73imqYV25BRmzQbt5qVhsT", "1U4Y990QEGFY104mNFVxlJ",],
    "sad": ["2uEODdOqnVjn2I7hFyam6C", "4bRQf8bwAIVgCb6Lcoursx",],        # "Sad Vibes"
    "chill": ["0k0WKMaoZs46MFTYHwZku5","55PVuXcePN1SJUh8yczGuR", ],      # "Chill Hits"
    "romantic": ["7sjpGZfJZ8SkQ2NQtdFciM","1qf2SGnCWGUlAVv23iuimi",],    # "Love Pop"
    "energetic": ["3mSm688yR6UeaAJNf93Ydr","3WYmyXrEqRL1UnV3ep13ie",],    # "Workout Twerkout"
}


def get_playlist_tracks(playlist_id, token, limit=20):
    url = url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"limit": limit}
    res = requests.get(url, headers=headers, params=params)
    data = res.json()

    tracks = []

    for item in data.get("items", []):
        track = item.get("track")
        if not track:
            continue

        # Some tracks might not have preview URLs
        name = track.get("name")
        artist = track["artists"][0]["name"] if track.get("artists") else "Unknown Artist"
        url = track.get("external_urls", {}).get("spotify", "")
        preview = track.get("preview_url")

        if name and artist and url:
            tracks.append({
                "name": name,
                "artist": artist,
                "url": url,
                "preview": preview
            })
    # print("Raw playlist response:", data)
    return tracks


def recommend_songs_by_mood(mood):
    mood = mood.lower()
    if mood not in MOOD_PLAYLISTS:
        print("Mood not recognized. Try: happy, sad, energetic, chill, romantic")
        return

    token = get_access_token()
    print(f"\n🔍 Fetching {mood}-themed songs from curated Spotify playlist...")

    playlist_ids = MOOD_PLAYLISTS[mood]
    songs = []

    for pid in playlist_ids:
        try:
            fetched = get_playlist_tracks(pid, token)
            if fetched:
                songs.extend(fetched)
        except Exception as e:
            print(f"⚠️ Error fetching from playlist {pid}: {e}")

    return songs

    if songs:
        print(f"\n🎵 Recommended songs for mood: {mood}\n")
        for song in songs[:40]:
            print(f"{song['name']} - {song['artist']}")
            print(f"▶ {song['url']}")
            if song['preview']:
                print(f"🔊 Preview: {song['preview']}")
            print("---")
    else:
        print("No songs found in the playlist 😔")

# Run it
if __name__ == "__main__":
    user_mood = input("Enter a mood (happy, sad, energetic, chill, romantic): ")
    recommend_songs_by_mood(user_mood)

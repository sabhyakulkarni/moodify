import streamlit as st
from mood_recommender import recommend_songs_by_mood

st.set_page_config(
    page_title="Mood Song Recommender",
    page_icon="🎧",
    layout="wide"
)

# CSS Styling for colors, fonts, and layout
st.markdown("""
    <style>
    body {
        background-color: #fffdf7;
    }
    .main {
        font-family: 'Segoe UI', sans-serif;
    }
    .title {
        background: linear-gradient(to right, #ff7e5f, #feb47b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3em;
        font-weight: bold;
    }
    .song-card {
        background-color: #f0f9ff;
        border-left: 5px solid #1DB954;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .song-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #222;
    }
    .artist {
        font-size: 1.1rem;
        color: #444;
        margin-bottom: 5px;
    }
    .link {
        font-size: 0.9rem;
        color: #1DB954;
        font-weight: 500;
    }
    .preview-title {
        font-size: 0.85rem;
        color: #888;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 class='title'>🎧 Mood-Based Song Recommender</h1>", unsafe_allow_html=True)
st.markdown("##### Discover Spotify tracks based on how you're feeling 🌈")

# Mood dropdown
mood = st.selectbox(
    "🌟 What's your current mood?",
    ["😊 Happy", "😢 Sad", "🧊 Chill", "❤️ Romantic", "🔥 Energetic"]
)

clean_mood = mood.split()[1].lower()

if st.button("🎶 Show Recommendations"):
    with st.spinner("Contacting Spotify's vibe servers... 🧠"):
        songs = recommend_songs_by_mood(clean_mood)

    if songs:
        st.success(f"✨ Songs for your *{clean_mood}* mood:")
        for song in songs[:12]:
            st.markdown(f"""
                <div class='song-card'>
                    <div class='song-title'>{song['name']}</div>
                    <div class='artist'>by {song['artist']}</div>
                    <a class='link' href='{song['url']}' target='_blank'>🔗 Listen on Spotify</a><br>
            """, unsafe_allow_html=True)
            if song["preview"]:
                st.audio(song["preview"], format="audio/mp3")
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.error("Oops! No songs found for this mood. Try another one!")

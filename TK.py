import streamlit as st
import pandas as pd
import os
import random
import math
import urllib.parse


csv_path = os.path.join("TK", "TMKOC_episodes.csv")

try:
    df = pd.read_csv(csv_path)
except FileNotFoundError:
    st.error(f"CSV file not found! Make sure it exists at: {csv_path}")
    st.stop()



# Load the dataset
try:
    df = pd.read_csv(csv_path)
except FileNotFoundError:
    st.error(f"CSV file not found at: {csv_path}")
    st.stop()

# Assign seasons automatically (every 200 episodes)
def assign_season(ep, size=200):
    start = ((math.ceil(ep / size) - 1) * size) + 1
    end = math.ceil(ep / size) * size
    return f"{start}-{end}"

df["Season"] = df["episode_number"].apply(assign_season)


st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://i0.wp.com/deadant.co/wp-content/uploads/2023/07/TMKOC.png?fit=1366%2C768&ssl=1");
        background-size: cover;
        background-position: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit UI
st.title("📺 Taarak Mehta Episode Recommender")

# Dropdown for season
season_order = sorted(df["Season"].unique(), key=lambda x: int(x.split('-')[0]))
selected_season = st.selectbox("Choose Episode range:", season_order)

# Filter dataset by selected season
season_df = df[df['Season'] == selected_season]

# Recommend random episode
if st.button("🎲 Recommend Random Episode"):
    random_index = random.randint(0, len(season_df) - 1)
    episode = season_df.iloc[random_index]

    st.subheader(f"🎬 {episode['Episode_title']}")
    st.write(f"📝 {episode['description']}")
    st.write(f"📅 Episode Number: {episode['episode_number']}")

    # YouTube search link
    query = f"Taarak Mehta Episode {episode['episode_number']}"
    search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
    


    st.markdown(f"""
        <a href="{search_url}" target="_blank">
            <button style="
                background-color:#FF0000;
                color:white;
                padding:12px 24px;
                font-size:16px;
                border-radius:8px;
                border:none;
                cursor:pointer;">
                ▶️ Watch on YouTube
            </button>
        </a>
        """, unsafe_allow_html=True)

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

# Streamlit UI
st.title("📺 Taarak Mehta Episode Recommender")

# Dropdown for season
season_order = sorted(df["Season"].unique(), key=lambda x: int(x.split('-')[0]))
selected_season = st.selectbox("Choose a Season:", season_order)

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
    st.markdown(f"[▶️ Watch on YouTube]({search_url})", unsafe_allow_html=True)

import google.generativeai as genai
import streamlit as st
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
import pandas as pd

key = st.secrets["key"]
genai.configure(api_key=key)

model = genai.GenerativeModel("gemini-2.5-flash")

st.title("Gemini NBA Comparison Report")

st.write(
    "Compare two NBA players using Gemini API!!"
)

nba = players.get_players()
nba_names = [p["full_name"] for p in nba]
tab1, tab2 = st.tabs(["Select Players", "View Analysis"])

with tab1:
    request_data = False
    st.subheader("Choose two nba players to compare")

    p1 = st.selectbox("Player 1", nba_names, index=0)
    p2 = st.selectbox("Player 2", nba_names, index=1)


    st.caption("Select a focus for the comparison")
    focus = st.selectbox("Main focus",["Completeness", "Scoring", "Playmaking", "Defense", "Rebounding"])


    submit = st.button("Submit")

    if submit:
        request_data = True
        if p1 == p2:
            st.warning("Please use two different players to compare")
        p1_id = [p for p in nba if p['full_name'] == p1][0]['id']
        p2_id = [p for p in nba if p['full_name'] == p2][0]['id']

        p1_stats = playercareerstats.PlayerCareerStats(player_id=p1_id)
        df_p1 = p1_stats.get_data_frames()[0]

        p2_stats = playercareerstats.PlayerCareerStats(player_id=p2_id)
        df_p2 = p2_stats.get_data_frames()[0]


with tab2:
    if request_data:
        response = model.generate_content(f"Compare two NBA players based on their stats from their career and our main focus {focus}. The two players we want to compare are {p1} and {p2}. The career stats for {p1} are {df_p1} and the career stats for {p2} are {df_p2}. Try your best to be unbiased and try to adjust for different eras of play and pace if two players are from different times.")
        st.subheader("The analysis:")
        st.write(response.text)
        
    else:
        st.write("Go back and pick players and focus!")
import streamlit as st
import pandas as pd

from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats

import google.generativeai as genai

# Using Streamlit Secrets for API key
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

st.title("NBA Stats Chatbot (Phase 4)")

st.write(
    "Chat with a bot that knows about NBA stats from the live NBA API.\n"
    "Pick players and ask questions like 'Who is the better scorer?' or "
    "'Explain this player's strengths to a beginner.'"
)

st.divider()

all_players = players.get_players()
player_names = [p["full_name"] for p in all_players]

col1, col2 = st.columns(2)

with col1:
    main_player = st.selectbox("Main player", player_names)
    focus = st.selectbox(
        "Main topic",
        ["Overall", "Scoring", "Passing", "Rebounding"],
    )

with col2:
    compare_player = st.selectbox(
        "Optional comparison player (or None)",
        ["None"] + player_names,
    )
    num_seasons = st.slider(
        "Recent seasons to use",
        min_value=1,
        max_value=10,
        value=5,
    )

if main_player == compare_player and compare_player != "None":
    st.warning("For a comparison, pick two different players.")

st.divider()

def stats_summary(player_name, seasons_to_keep):
    """Return one line of text with simple averages for a player."""
    player_id = None
    for p in all_players:
        if p["full_name"] == player_name:
            player_id = p["id"]
            break

    if player_id is None:
        return f"Could not find stats for {player_name}."

    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    df = career.get_data_frames()[0]
    recent = df.tail(seasons_to_keep)

    avg_pts = recent["PTS"].mean()
    avg_ast = recent["AST"].mean()
    avg_reb = recent["REB"].mean()

    text = (
        f"{player_name}: about {avg_pts:.1f} points, {avg_ast:.1f} assists, "
        f"{avg_reb:.1f} rebounds per season over the last {len(recent)} seasons."
    )
    return text


if "messages" not in st.session_state:
    st.session_state.messages = []  
if "history_text" not in st.session_state:
    st.session_state.history_text = ""  

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Ask the NBA chatbot a question:")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.history_text += "User: " + user_input + "\n"

    with st.chat_message("user"):
        st.write(user_input)

    main_text = stats_summary(main_player, num_seasons)
    if compare_player != "None":
        compare_text = stats_summary(compare_player, num_seasons)
    else:
        compare_text = "No comparison player was selected."

    if focus == "Scoring":
        focus_hint = "Focus more on scoring and shooting."
    elif focus == "Passing":
        focus_hint = "Focus more on passing and playmaking."
    elif focus == "Rebounding":
        focus_hint = "Focus more on rebounding and inside play."
    else:
        focus_hint = "Look at overall impact."

    context = (
        "Here are stats from the live NBA API:\n"
        + main_text
        + "\n"
        + compare_text
        + "\n\nFocus instructions: "
        + focus_hint
        + "\n"
    )

    prompt = (
        "You are an NBA stats chatbot. Use the stats I give you and explain things "
        "simply for a beginner fan. Do not make up random numbers.\n\n"
        + context
        + "\nConversation so far:\n"
        + st.session_state.history_text
        + "\nAnswer the last user question in a friendly way.\n"
    )

    try:
        response = model.generate_content(prompt)
        answer = response.text
    except Exception as e:
        answer = (
            "Sorry, something went wrong while talking to Gemini. "
            "Please wait a bit and try again."
        )
        st.error("Gemini error: " + str(e))

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.session_state.history_text += "Bot: " + answer + "\n"

    with st.chat_message("assistant"):
        st.write(answer)
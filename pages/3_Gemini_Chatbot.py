import streamlit as st
import google.generativeai as genai
from nba_api.stats.endpoints import leaguedashlineups
from nba_api.stats.endpoints import leaguedashptstats

st.title("Chat with specialized Gemini chatbot about the 2025-2026 season.")
key = st.secrets["key"]
genai.configure(api_key=key)

chatPrompt = st.chat_input("Type prompt here")
model = genai.GenerativeModel("gemini-2.5-flash")

if "nba_data" not in st.session_state:
    st.session_state.nba_data = [leaguedashptstats.LeagueDashPtStats(season='2025-26').get_data_frames()[0]]
if "messages" not in st.session_state:
    st.session_state.messages = []


user = st.chat_message("user")
if chatPrompt:
    try:
        user.write(chatPrompt)
        ai = st.chat_message("ai")
        response = model.generate_content(f"You are a specialized nba expert on the 2025-2026 season. Respond to the prompt {chatPrompt} briefly, with a maximum response of 150-200 words. Past conversations: {", ".join(st.session_state.messages)}. Use information from the 2025-2026 season: {st.session_state.nba_data}")
        ai.write(response.text)
        st.session_state.messages.append(chatPrompt, response.text)
    except:
        ai.write("The Gemini API has errored. This is likely due to a rate error, so please wait for requests to reload.")
import streamlit as st

# Title of App
st.title("Web Development Lab03")

# Assignment Data 
# TODO: Fill out your team number, section, and team members

st.header("CS 1301")
st.subheader("Team 60, Web Development - Section C")
st.subheader("Panav Kalra, Winston Wu")

# https://github.com/swar/nba_api
# Introduction
# TODO: Write a quick description for all of your pages in this lab below, in the form:
#       1. **API Analysis**: Fetch and visualize data from our chosen web API.
#       2. **Page Name**: Description
#       3. **Gemini Chatbot**: Chatbot that answers questions using API-backed context.
#       4. **Page Name**: Description


st.write("""
1. **API Analysis**: Getting and visualize our NBA API.
2. **Gemini Processing** Using Gemini to process NBA API data and output LLM messages
""")

st.markdown("Links to pages")
st.page_link("pages/1_API_Analysis.py", label="Go to: API Analysis")
st.page_link("pages/2_Gemini_Processing.py", label="Go to: Gemini Generation")
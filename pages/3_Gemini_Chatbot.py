import streamlit as st
import google.generativeai as genai
st.title("Chat with specialized Gemini chatbot")
key = st.secrets["key"]
genai.configure(api_key=key)
chatPrompt = st.chat_input("Type prompt here")
model = genai.GenerativeModel("gemini-2.5-flash")
with st.chat_message("user"):
    if chatPrompt:
        try:
            st.write(chatPrompt)
            ai = st.chat_message("ai")
            response = model.generate_content(f"You are a specialized nba expert. Respond to the prompt {chatPrompt} briefly, with a maximum response of 150-200 words.")
            ai.write(response.text)
        except:
            ai.write("The Gemini API has errored. This is likely due to a rate error. Please wait for requests to reload.")
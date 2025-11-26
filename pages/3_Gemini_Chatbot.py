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
            response = model.generate_content(f"You are a specialized nba expert. Respond to the prompt {chatPrompt} briefly, in about 150-200 words.")
            st.write(response.text)
        except:
            st.write("The Gemini API has errored. This is likely due to a rate error. Please wait for requests to reload.")
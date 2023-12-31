import streamlit as st

st.set_page_config(
    page_title="Baby Owl",
    page_icon=":gear:",
    layout="wide",
    initial_sidebar_state="auto"
)

# create session state if it doesn't exist
if 'session_state' not in st.session_state:
    st.session_state['session_state'] = {}
# --- set api keys---
st.title("Settings")
st.info("Keys are only stored during the length of your session. For security and privacy reasons, we do not persistently store your API keys. Refreshing or exiting the window will delete your keys.")
st.subheader("Enter your API keys.")
st.write("API Keys for OpenAI and SerpAPI are required to use this service")
st.write("If you need either key, you can sign up for an account to get access using the links below:")
st.write("SERP API: https://serpapi.com/users/sign_up")
st.write("OPENAI API: https://platform.openai.com/signup?launch")

if 'openai_api_key' in st.session_state['session_state']:
    openai_key_state = st.session_state['session_state']['openai_api_key']
else:
    openai_key_state = ''

if 'serp_api_key' in st.session_state['session_state']:
    serp_key_state = st.session_state['session_state']['serp_api_key']
else:
    serp_key_state = ''
# user input
open_ai_key = st.text_input("OpenAI API Key", openai_key_state)
# input submit button
if st.button(key="open_ai_key_submit_btn", label="Enter Key"):
    st.session_state['session_state']['openai_api_key'] = open_ai_key
    st.info('API key saved!')
# user input
serpAPI_key = st.text_input("Serp API Key", serp_key_state)
# input submit button
if st.button(key="serp_api_key_submit_btn", label="Enter Key"):
    st.session_state['session_state']['serp_api_key'] = serpAPI_key
    st.info('API key saved!')



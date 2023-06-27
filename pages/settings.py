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
# # add blank serp api key to session state before user provides key.
# if 'serp_api_key' not in st.session_state:
#     st.session_state['session_state']['serp_api_key'] = ''
# if 'openai_api_key' not in st.session_state:
#     st.session_state['session_state']['openai_api_key'] = ''
# --- set api keys---
st.title("Settings")
st.subheader("Enter your API keys and choose your language model.")
# user input
open_ai_key = st.text_input("OpenAI API Key", st.session_state['session_state']['openai_api_key'])
# input submit button
if st.button(key="open_ai_key_submit_btn", label="Enter Key"):
    st.session_state['session_state']['openai_api_key'] = open_ai_key
    st.info('API key saved!')
# user input
serpAPI_key = st.text_input("Serp API Key", st.session_state['session_state']['serp_api_key'])
# input submit button
if st.button(key="serp_api_key_submit_btn", label="Enter Key"):
    st.session_state['session_state']['serp_api_key'] = serpAPI_key
    st.info('API key saved!')



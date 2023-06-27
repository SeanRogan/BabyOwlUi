import streamlit as st
import util.datastore as store
from agent.baby_owl import BabyOwlAgent

st.set_page_config(
    page_title="The Owlery",
    page_icon=":owl:",
    layout="wide",
    initial_sidebar_state="auto"
)

if 'session_state' not in st.session_state:
    st.session_state['session_state'] = {}

state = st.session_state['session_state']
st.title("🧠 Baby Owl AGI 🦉")
st.header("An autonomous research assistant to help with the boring bits")

# email sign up
st.subheader("Enter Your Research Goal Below:")
st.write('Describe the research you\'d like the owl to do for you. Remember, the owl is just a baby, so be as exact as you can. For example, you might say \'research the topic of nuclear fusion advancements in the last 5 years. Collect at least 5 research papers related to the subject of nuclear fusion, summarize them and return a report on the findings of the papers, with citations for each one.\'')
research_topic = st.text_input(label='user_input', label_visibility='hidden', key='research_goal_input_field')
# button for submit
if st.button(label='Submit', key='research_goal_submit_btn'):
    if 'openai_api_key' not in state or 'serp_api_key' not in state:
        st.warning('Please enter your API keys in the settings window to use the agent.')
    else:
        st.write(str(state))
        agent = BabyOwlAgent(state['openai_api_key'], state['serp_api_key'], research_topic)
        agent.fly()
st.subheader("Owl work station")

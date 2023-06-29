import streamlit as st
import util.datastore as store
from agent.baby_owl import BabyOwlAgent
import os

st.set_page_config(
    page_title="The Owlery",
    page_icon=":owl:",
    layout="wide",
    initial_sidebar_state="auto"
)

storage_dir = os.path.dirname(os.path.curdir) + 'stored_files/'


def start_agent(agent: BabyOwlAgent):
    task_list = agent.create_task_list()
    tasks_completed = []
    summary_report = []
    next_task_msg = "\n#####" + "\n*****NEXT TASK*****\n" + "\n#####"
    st.write("\nInitializing...\n")
    st.write("Analyzing objective...\n")
    st.write("Running task creation agent...\n")
    while len(tasks_completed) < len(task_list):
        for task in task_list:
            task_info_msg = str(task['id']) + ": " + str(task['task']) + " [" + str(task['tool'] + "]")
            st.write(next_task_msg)
            st.write(task_info_msg)
            summary_report.append(next_task_msg)
            summary_report.append(task_info_msg)
            task_output = agent.execute_task(task)
            summary_report.append(task_output)
            st.write(task_output)
            st.write(agent.print_task_list())
            tasks_completed.append(task)
    return summary_report


if 'session_state' not in st.session_state:
    st.session_state['session_state'] = {}

state = st.session_state['session_state']
st.title("🧠 Baby Owl AGI 🦉")
st.header("An autonomous research assistant to help with the boring bits")
st.warning("Disclaimer: This is an experimental project, development is still in progress. Behavior may be unexpected, or the program may break entirely. Use at your own risk.")

# email sign up
st.subheader("Enter Your Research Goal Below:")
st.write('Describe the research you\'d like the owl to do for you. Remember, the owl is just a baby, so be as exact as you can. For example, you might say \'research the topic of nuclear fusion advancements in the last 5 years. Collect at least 5 research papers related to the subject of nuclear fusion, summarize them and return a report on the findings of the papers, with citations for each one.\' When the Owl is finished you will have the option to download its findings as a text file. The owl currently only flies one mission at a time')
research_topic = st.text_input(label='user_input', label_visibility='hidden', key='research_goal_input_field')
# button for submit
if st.button(label='Submit', key='research_goal_submit_btn'):
    report = ''
    if 'openai_api_key' not in state or 'serp_api_key' not in state:
        st.warning('Please enter your API keys in the settings window to use the agent.')
    else:
        owl = BabyOwlAgent(state['openai_api_key'], state['serp_api_key'], research_topic)
        report = start_agent(owl)
    try:
        with open(storage_dir + 'research_report.txt', 'x') as file:
            file.write(str(report))
    except FileNotFoundError:
        pass
f = 'research_report.txt'
try:
    with open(storage_dir + f, 'rb') as file:
        data = file.read()
        # todo this is broken, it wont send the f variable as an arguement to the on_click function that cleans up the file from the dir after the user downloads it to their computer.
        st.download_button(label='Download the Owl\'s Findings', file_name=f, data=data)
except FileNotFoundError:
    pass

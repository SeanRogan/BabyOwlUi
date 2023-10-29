import io
import os
import streamlit as st
#
# import chromadb
# from chromadb import Settings
# from chromadb.utils import embedding_functions

from agent.baby_owl import BabyOwlAgent

st.set_page_config(
    page_title="The Owlery",
    page_icon=":owl:",
    layout="wide",
    initial_sidebar_state="auto"
)


storage_dir = '../util/stored_files/'
# ef = embedding_functions.OpenAIEmbeddingFunction(
#                 api_key="YOUR_API_KEY",
#                 model_name="text-embedding-ada-002"
#            )
# chroma = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="../stored_files/chroma"))
# todo add user session id to document/collection metadata once implemented
# vdb = chroma.get_or_create_collection(name="uploaded_documents", embedding_function=ef)


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
            st.write(agent.print_task_list())
            task_info_msg = str(task['id']) + ": " + str(task['task']) + " [" + str(task['tool'] + "]")
            st.write(next_task_msg)
            st.write(task_info_msg)
            summary_report.append(next_task_msg)
            summary_report.append(task_info_msg)
            task_output = agent.execute_task(task)
            summary_report.append(task_output)
            # vdb.add(ids=f'', metadatas={'task': task['task'], 'goal': agent.OBJECTIVE}, documents=task_output)
            st.write(task_output)
            tasks_completed.append(task)
            # todo there need to be a summary formatting func to make the report look better.
    return summary_report


if 'session_state' not in st.session_state:
    st.session_state['session_state'] = {}

state = st.session_state['session_state']
st.title("🧠 Baby Owl AGI 🦉")
st.header("An autonomous research assistant to help with the boring bits")
st.warning("Disclaimer: This is an experimental project, development is still in progress. Behavior may be unexpected, or the program may break entirely. Use at your own risk.")

st.subheader("Enter Your Research Goal Below:")
st.write('Describe the research you\'d like the owl to do for you. Remember, the owl is just a baby, so be as exact as you can. For example, you might say: \n\n\'research the topic of nuclear fusion advancements in the last 5 years. Collect at least 5 research papers related to the subject of nuclear fusion, summarize them and return a report on the findings of the papers, with citations for each one.\'\n\n When the Owl is finished you will have the option to download its findings as a text file.')
research_topic = st.text_input(label='user_input', label_visibility='hidden', key='research_goal_input_field')

# button for submit
if st.button(label='Submit', key='research_goal_submit_btn'):
    if research_topic is not None and research_topic != '':
        # if os.path.exists(storage_dir + 'report.txt'):
        #     os.remove(storage_dir + 'report.txt')
        report = ''
        if 'openai_api_key' not in state or 'serp_api_key' not in state:
            st.warning('Please enter your API keys in the settings window to use the agent.')
        else:
            owl = BabyOwlAgent(state['openai_api_key'], state['serp_api_key'], research_topic)
            report = start_agent(owl)
        # try:
        #     #this needs to change
        #     with open(storage_dir + 'report.txt', 'x') as file:
        #         file.write(str(report))
        # except FileNotFoundError:
        #     pass
        report_buffer = io.BytesIO()
        report_buffer.write(str(report).encode())
    else:
        st.write('Please enter a topic for the owl to research for you.')
f = 'report.txt'
if 'report_buffer' in locals():
    report_buffer.seek(0)
    st.download_button(label='Download the Owl\'s Findings', file_name='owl report.txt', data=report_buffer.getvalue())
## this needs to change
# report_path = storage_dir + f
# try:
#     with open(report_path, 'rb') as file:
#         data = file.read()
#         st.download_button(label='Download the Owl\'s Findings', file_name=f, data=data)
#
# except FileNotFoundError:
#     pass

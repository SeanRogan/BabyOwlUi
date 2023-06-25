import os.path

import streamlit as st
import util.file_reader as fr

# need a file upload section and a section to show what files have been uploaded already.
st.set_page_config(
    page_title='Upload Your Documents',
    page_icon=':open_file_folder:',
    layout='wide',
    initial_sidebar_state='auto'
)


def get_all_files(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]


stored_file_dir = '/stored_files'


col1, col2 = st.columns(2)

with col1:
    st.header('Upload your documents')
    st.write('support for .txt, .csv, .pdf, and .docx')
    file = ''
    upload = st.file_uploader('Upload your files below', type=['pdf', 'docx', 'txt', 'csv'])
    if st.button(label='Upload', key='file_upload_btn'):
        if upload is not None:
            file_details = {'file_name': upload.name, 'file_type': upload.type, 'file_size': upload.size}
            if upload.type == 'text/plain':
                file = fr.read_txt_file(upload)
            elif upload.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                file = fr.read_docx_file(upload)
            elif upload.type == 'application/pdf':
                file = fr.read_pdf(upload)


with col2:
    st.header('Uploads')
    st.write('Your uploaded files will appear here')
    files = get_all_files(os.path.join(os.getcwd() + stored_file_dir))
    if files is not None:
        for f in files:
            st.download_button(f'Download File: {f}', f)



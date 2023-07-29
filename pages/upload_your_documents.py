import os

import streamlit as st
import util.file_reader as fr
import path
import sys

# need a file upload section and a section to show what files have been uploaded already.
st.set_page_config(
    page_title='Upload Your Documents',
    page_icon=':open_file_folder:',
    layout='wide',
    initial_sidebar_state='auto'
)
#
# directory = path.Path(__file__).abspath()
# sys.path.append(directory.parent.parent)

st.title('Give the owl something to read!')
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
            # elif upload.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            #     file = fr.read_docx_file(upload)
            elif upload.type == 'application/pdf':
                file = fr.read_pdf(upload)

with col2:
    storage_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stored_files')
    st.header('Your uploaded files will appear here')
    files = [f for f in os.listdir(storage_dir) if os.path.isfile(os.path.join(storage_dir, f))]
    if files is not None:
        for f in files:
            st.write(f)
            # download files button
            with open(storage_dir + f, 'rb') as opened_file:
                st.download_button(label=f'Download File: {f}', file_name=f, data=opened_file)

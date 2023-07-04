import os
from io import StringIO

import pandas as pd
from PyPDF2 import PdfReader, PdfWriter
import chromadb
from chromadb import Settings
from chromadb.utils import embedding_functions
from docx import document as docx

storage_dir = os.path.dirname(os.path.curdir) + 'stored_files/'
ef = embedding_functions.OpenAIEmbeddingFunction(
                api_key="YOUR_API_KEY",
                model_name="text-embedding-ada-002"
            )
chroma = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="../stored_files/chroma"))
collection = chroma.get_or_create_collection(name="uploaded_documents", embedding_function=ef)
# todo add user session id to document/collection metadata once implemented


def read_pdf_with_pypdf2(file):
    reader = PdfReader(file)
    writer = PdfWriter()
    text = ''
    for page in reader.pages:
        writer.add_page(page)
        text += page.extract_text() + ' '
    output_file_path = os.path.join(storage_dir + file.name)
    with open(output_file_path, 'wb') as file:
        writer.write(file)
    collection.add(ids=file.name, documents=text)
    return text


def read_pdf(file):
    try:
        pdf = read_pdf_with_pypdf2(file)
        return pdf
    except RuntimeWarning as err:
        print('There was a problem reading the file' + str(err))


def read_txt_file(file):

    sio = StringIO(file.getvalue().decode('utf-8'))
    text = sio.read()
    with open(storage_dir + file.name, 'w') as f:
        f.write(text)
    collection.add(documents=text, ids=file.name)
    return text


def read_docx_file(file):
    doc = docx.Document(file)
    content = []
    for paragraph in doc.paragraphs:
        content.append(paragraph.text)
    joined_file = '\n'.join(content)
    # save file to file system, and vectorize and send to vector db


# todo implement csv support

def read_csv(file):
    df = pd.read_csv(file)
    pass
    # save file to file system, and vectorize and send to vector db

import fitz
import pandas as pd
# import pdfplumber as pdfp
from docx import document as docx
from PyPDF2 import PdfReader, PdfWriter
import os


def read_pdf_with_pypdf2(file):

    reader = PdfReader(file)
    writer = PdfWriter()
    print(file.name)
    text = ''
    for page in reader.pages:
        writer.add_page(page)
        text += page.extract_text() + ' '

    output_file_path = os.path.join(os.path.dirname(os.path.curdir) + 'stored_files/' + file.name)
    with open(output_file_path, 'wb') as file:
        writer.write(file)
    print(text)
    return text


def read_pdf(file):
    try:
        pdf = read_pdf_with_pypdf2(file)
        return pdf
    except RuntimeWarning as err:
        print('There was a problem reading the file' + str(err))

# save file to file system, and vectorize and send to vector db


def read_txt_file(file):
    return file
    # save file to file system, and vectorize and send to vector db


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


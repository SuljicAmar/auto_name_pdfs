import pymupdf
import os
import json
from glob import glob
from .llm import ModelWrapper


def get_all_pdfs(directory):
    return glob(os.path.join(directory, "*.pdf"))


def load_document(path):
    return pymupdf.open(path)


def set_num_pages(document):
    num_pages = document.page_count
    if num_pages > 5:
        num_pages = 5
    return num_pages


def get_content(document, num_pages):
    content = ""
    for iPage in range(num_pages):
        content += document[iPage].get_text()
    return content


def get_title_and_authors(content, model):
    model_response = json.loads(model.run(content))
    # For last names to be included:
    # return model_response["title"] + " " + " ".join(model_response["authors"]) + ".pdf"
    return f'{model_response["title"]}.pdf'.replace("/", "")


def rename_document(original_path, new_path):
    os.rename(original_path, new_path)
    print(f"Renamed {original_path.split('/')[-1]} to {new_path.split('/')[-1]}")


def rename_bulk(directory):
    model = ModelWrapper()
    all_documents = get_all_pdfs(directory)
    for iPath in all_documents:
        document = load_document(iPath)
        num_pages = set_num_pages(document)
        content = get_content(document, num_pages)
        new_file_name = directory + get_title_and_authors(content, model)
        rename_document(iPath, new_file_name)

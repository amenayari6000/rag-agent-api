import os
import tempfile
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader

load_dotenv()


def load_text_file():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
        temp_file.write(
            b"Hello, this is a sample text file.\n"
            b"This file is used to demonstrate the TextLoader."
        )
        temp_file_path = temp_file.name

    try:
        loader = TextLoader(temp_file_path)
        documents = loader.load()

        for doc in documents:
            print("Document Content:")
            print(doc)
            print(doc.page_content)
    finally:
        os.remove(temp_file_path)


if __name__ == "__main__":
    load_text_file()

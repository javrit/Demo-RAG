import logging
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import Language
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders.parsers.pdf import extract_from_images_with_rapidocr
from langchain.schema import Document


def process_pdf(source): 
    """Function to load a PDF document, and to keep only the pages with content. 

    Args:
        source : PDF document to be processed

    Raises:
        ValueError: if the PDF contains only empty pages

    Returns:
        processed pdf
    """
    loader = PyPDFLoader(source) #loads a pdf
    documents = loader.load()
    unscanned_documents = [doc for doc in documents if doc.page_content.strip() != ""] #filters empty pages
    scanned_pages = len(documents) - len(unscanned_documents)
    if scanned_pages > 0:
        logging.info(f'Omitted {scanned_pages} scanned page(s) from the PDF')
    if not unscanned_documents:
        raise ValueError("All pages in the PDF appear to be scanned. Please use a PDF with text content")
    print(type(split_documents(unscanned_documents)))
    return split_documents(unscanned_documents)

def process_image(source): 
    
    with open(source, "rb") as image_file:
        image_bytes = image_file.read()
        extracted_text = extract_from_images_with_rapidocr([image_bytes])
        documents = [Document(page_content=extracted_text, metadata = {"source":source})]
        print('type process image', type(split_documents(documents)))
    return split_documents(documents)
    
    
    
def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter.from_language(language=Language.PYTHON, chunk_size=1000, chunk_overlap=200)
    return text_splitter.split_documents(documents)


def process_document(source):
    """Process the document according to the source type (PDF or image)

    Args:
        source : PDF file or image

    Raises:
        ValueError: if source is not a PDF file or an image (jpg, jpeg, png)

    Returns:
        processed document
    """
    if source.lower().endswith('.pdf'):
        return process_pdf(source)
    elif source.lower().endswith((".png",".jpg",".jpeg")):
        return process_image(source)
    else:
        raise ValueError(f"Unsupported file type")

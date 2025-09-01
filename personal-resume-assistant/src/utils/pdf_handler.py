import os
from pathlib import Path
from typing import List, Dict
from pypdf import PdfReader

def extract_all_pdf(dir_path: str) -> Dict[str, str]:
    extracted_texts = {}
    
    directory = Path(dir_path)
    
    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {dir_path}")
    
    if not directory.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {dir_path}")
    
    pdf_files = list(directory.glob("*.pdf"))
    
    for pdf_file in pdf_files:
        try:
            text = extract_pdf(str(pdf_file))
            extracted_texts[pdf_file.name] = text
        except Exception as e:
            print(f"Error extracting text from {pdf_file.name}: {str(e)}")
            extracted_texts[pdf_file.name] = ""
    
    return extracted_texts


def extract_pdf(file_path: str) -> str:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF file not found: {file_path}")
    
    if not file_path.lower().endswith('.pdf'):
        raise ValueError(f"File is not a PDF: {file_path}")
    
    try:
        reader = PdfReader(file_path)
        
        text = ""
        for page_num, page in enumerate(reader.pages):
            try:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            except Exception as e:
                print(f"Error extracting text from page {page_num + 1}: {str(e)}")
                continue
        
        return text.strip()
    
    except Exception as e:
        raise Exception(f"Error reading PDF file {file_path}: {str(e)}")
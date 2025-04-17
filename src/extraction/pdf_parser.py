import pdfplumber
from pathlib import Path

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts raw text from a PDF resume using pdfplumber.
    
    Args:
        pdf_path (str): Path to the resume PDF file.
    
    Returns:
        str: Extracted plain text from the resume.
    """
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def save_extracted_text(text: str, output_path: str):
    """
    Saves the extracted text to a .txt file for review or debugging.
    
    Args:
        text (str): Extracted resume text.
        output_path (str): Path to save the text file.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

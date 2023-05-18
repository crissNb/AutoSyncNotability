import sys
from src.pdfconverter import PDFConverter

pdf_file_path = sys.argv[1]
reference_path = sys.argv[2]

converter = PDFConverter(pdf_file_path, reference_path)
converter.convert()

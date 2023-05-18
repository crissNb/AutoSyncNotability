import sys
import re
from src.pdfconverter import PDFConverter
from src.configreader import ConfigReader
from pathlib import Path

pdf_file_path = sys.argv[1]
changed = sys.argv[2]

pdf_file_name = pdf_file_path.split('/')[-1]

config = ConfigReader().load_config()

# loop through config and check if pdf_file_name matches regex_match
for section in config:
    if re.match(config[section]['regex_match'], pdf_file_name):
        # pdf_file_name matches regex_match
        if not Path(config[section]['reference_path']).expanduser().is_file():
            print("reference path for " + section + " is invalid!")
            break

        pdfconverter = PDFConverter(pdf_file_path, config[section]['reference_path'])
        pdfconverter.convert()

        # check if pdfconverter converted by checking if the file exists
        if not Path('converted').is_file():
            print("PDFConverter failed to convert!")
            break
        break

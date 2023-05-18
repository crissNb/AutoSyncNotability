import sys
import re
from src.pdfconverter import PDFConverter
from src.configreader import ConfigReader
from src.syncer import Syncer
from pathlib import Path

pdf_file_path = sys.argv[1]
changed = sys.argv[2]

pdf_file_name = pdf_file_path.split('/')[-1]

config = ConfigReader().load_config()

# loop through config and check if pdf_file_name matches regex_match
for section in config:
    # skip auth section
    if section == 'AUTH':
        continue

    if re.match(config[section]['regex_match'], pdf_file_name):
        # pdf_file_name matches regex_match
        if not Path(config[section]['reference_path']).expanduser().is_dir():
            print("reference path for " + section + " is invalid!")
            break

        pdfconverter = PDFConverter(pdf_file_path, config[section]['reference_path'])
        pdfconverter.convert()

        # check if pdfconverter converted by checking if the file exists
        if not Path('converted').is_dir():
            print("PDFConverter failed to convert!")
            break

        # rename converted file to pdf_file_name + ".nbn"
        # remove pdf extension and add .nbn extension
        converted_file_name = pdf_file_name.split('.')[0] + ".nbn"
        Path('converted').rename(converted_file_name)
        
        # sync converted file
        syncer = Syncer(config['AUTH']['id'], converted_file_name, config['AUTH']['destination_name']).sync(changed)
        break

import sys
import re
from src.pdfconverter import PDFConverter, shutil
from src.configreader import ConfigReader
from src.syncer import Syncer
from pathlib import Path
from icloudpy import ICloudPyService

pdf_file_path = sys.argv[1]
changed = sys.argv[2]

pdf_file_name = pdf_file_path.split('/')[-1]

config = ConfigReader().load_config()

api = ICloudPyService(config['AUTH']['id'])

if api.requires_2fa:
    print("Two-factor authentication required.")
    code = input("Enter the code you received of one of your approved devices: ")
    result = api.validate_2fa_code(code)
    print("Code validation result: %s" % result)

    if not result:
        print("Failed to verify security code")
        sys.exit(1)

    if not api.is_trusted_session:
        print("Session is not trusted. Requesting trust...")
        result = api.trust_session()
        print("Session trust result %s" % result)

        if not result:
            print("Failed to request trust. You will likely be prompted for the code again in the coming weeks")
elif api.requires_2sa:
    import click
    print("Two-step authentication required. Your trusted devices are:")

    devices = api.trusted_devices
    for i, device in enumerate(devices):
        print("  %s: %s" % (i, device.get('deviceName',
            "SMS to %s" % device.get('phoneNumber'))))

    device = click.prompt('Which device would you like to use?', default=0)
    device = devices[device]
    if not api.send_verification_code(device):
        print ("Failed to send verification code")
        sys.exit(1)

    code = click.prompt('Please enter validation code')
    if not api.validate_verification_code(device, code):
        print ("Failed to verify verification code")
        sys.exit(1)

api.drive.params["clientId"] = api.client_id

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
        converted_file_name = pdf_file_name.split('.')[0]
        Path('converted').rename(converted_file_name)

        # sync converted file
        syncer = Syncer(api.drive, 
                        config['AUTH']['dump_folder'],
                        config['AUTH']['destination_name'], 
                        converted_file_name, 
                        ).sync(changed)

        shutil.rmtree(converted_file_name)
        break


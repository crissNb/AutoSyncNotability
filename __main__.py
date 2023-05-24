import sys
import re
import socket
import time
import threading
from src.pdfconverter import PDFConverter, shutil
from src.configreader import ConfigReader
from src.syncer import Syncer
from pathlib import Path
from icloudpy import ICloudPyService

files_queue = {}

# Create a server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8000))

def queue_file(data):
    # data has a format of PDF_FILE_PATH:::CHANGED;;;PDF_FILE_PATH:::CHANGED (CHANGED is a boolean)

    # split data into a list of files
    files = data.split(';;;')

    # iterate through files and add them to the queue
    for file in files:
        # split file into file path and changed
        splited = file.split(':::')
        if (len(splited) != 2):
            continue
        file_data = splited[0]
        changed = splited[1]
        files_queue[file_data] = changed

def listen_for_files():
    while True:
        # Listen for incoming connections
        server_socket.listen()
        print("Listening for connection...")

        client_socket, addr = server_socket.accept()

        # Receive data from client
        data = client_socket.recv(8192).decode('utf-8')

        queue_file(data)

        print("Received data: " + data)
        client_socket.send(b'Received data')
        client_socket.close()

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

# Start the thread to handle incoming connections
threading.Thread(target=listen_for_files).start()

# Main loop
while (True):
    if len(files_queue) == 0:
        # periodically check for files that are uploaded to icloud
        print("Checking for files...")
        files = api.drive[config['AUTH']['dump_folder']].dir()
        print(files)
        for file in files:
            # check if file has an nbn extension
            if file.endswith('.nbn'):
                print(file)
                # move the file to the correct location
                api.drive[config['AUTH']['dump_folder']][file].move("FOLDER::" + config['AUTH']['destination_name'] + "::documents")

                # remove .nbn from the file
                file = file[:-4]

                api.drive[config['AUTH']['dump_folder']][file].delete()
        
        time.sleep(5)
    elif len(files_queue) > 0:
        # get first file in queue
        pdf_file_path, changed = files_queue.popitem()
        pdf_file_name = pdf_file_path.split('/')[-1]

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

                print("Now handling: " + pdf_file_name)

                pdfconverter = PDFConverter(pdf_file_path, config[section]['reference_path'], pdf_file_name)
                pdfconverter.convert()

                # check if pdfconverter converted by checking if the file exists

                # remove .pdf from pdf_file_name
                pdf_file_name = pdf_file_name[:-4]
                converted_file_name = 'converted_' + pdf_file_name

                if not Path(converted_file_name).is_dir():
                    print("PDFConverter failed to convert!")
                    break

                # sync converted file
                syncer = Syncer(api.drive, 
                                config['AUTH']['dump_folder'],
                                config['AUTH']['destination_name'], 
                                converted_file_name, 
                                )
                try:
                    syncer.sync(changed)
                except Exception as e:
                    shutil.rmtree(converted_file_name)

                    # add file back to queue
                    files_queue[pdf_file_path] = changed
                    print(e)
                    print("job failed; continuing in 5")
                    time.sleep(5)
                    break

                shutil.rmtree(converted_file_name)
                print("finished job: " + converted_file_name)
                time.sleep(1)
                break
            print("skipping: " + pdf_file_name)

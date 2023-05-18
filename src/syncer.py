from icloudpy import ICloudPyService
import sys
import os

class Syncer:
    def __init__(self, auth_id, target_path, destination_name):
        self.auth_id = auth_id
        self.target_path = target_path
        self.destination_name = destination_name

    def sync(self, file_changed):
        api = ICloudPyService(self.auth_id)

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

        notabilityNode = api.drive.get_app_node(self.destination_name)

        if not notabilityNode:
            print("Notability folder not found. Abort.")
            return

        print(self.target_path)

        notabilityNode.mkdir(self.target_path)
        self.upload_files(notabilityNode, self.target_path)

    def upload_files(self, node, target_path):
        # recursively go through target_path folder and upload files
        for file in os.listdir(target_path):
            if os.path.isdir(os.path.join(target_path, file)):
                # file is a folder
                # TODO: folder creation respecting the path
                node.mkdir(file)
                self.upload_files(node, os.path.join(target_path, file))
            else:
                # file is a file
                with open(os.path.join(target_path, file), 'rb') as f:
                    node.upload(f)

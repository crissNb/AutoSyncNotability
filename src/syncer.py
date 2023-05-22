from icloudpy import ICloudPyService
import os
import time

class Syncer:
    sync_fail_count = 0

    def __init__(self, drive, dump_folder, destination_name, target_path):
        self.drive = drive
        self.dump_folder = dump_folder
        self.destination_name = destination_name
        self.target_path = target_path

    def sync(self, file_changed):
        print("uploading: " + self.target_path)
        self.drive[self.dump_folder].mkdir(self.target_path)
        time.sleep(1)

        self.drive[self.dump_folder].dir()
        time.sleep(1)

        # ensure the folders are created (cannot be done under recursion for 
        # some reason
        for file in os.listdir(self.target_path):
            if os.path.isdir(os.path.join(self.target_path, file)):
                self.drive[self.dump_folder].mkdir(self.target_path + '/' + file)
            time.sleep(1)

        print(self.drive[self.dump_folder][self.target_path].dir())

        self.upload_files(self.target_path)
        print("uploading done")

    def attempt_upload(self, target_file_location, destination_file_location):
        # self.drive[self.dump_folder][self.target_path].update_data()
        try:
            with open(target_file_location, 'rb') as f:
                if destination_file_location == self.target_path:
                    self.drive[self.dump_folder][self.target_path].upload(f)
                else:
                    self.drive[self.dump_folder][self.target_path][destination_file_location].upload(f)
        except Exception as e:
            if self.sync_fail_count > 5:
                print("upload failed too many times, trying entirely again...")
                self.drive[self.dump_folder][self.target_path].delete()
                raise e

            print(e)
            print("upload failed, retrying...")
            self.sync_fail_count += 1
            time.sleep(1)
            self.attempt_upload(target_file_location, destination_file_location)

    def upload_files(self, target_path):
        for file in os.listdir(target_path):
            print(file)
            self.drive[self.dump_folder][self.target_path].get_children()
            if os.path.isdir(os.path.join(target_path, file)):
                # file is a folder
                self.upload_files(os.path.join(target_path, file))
            else:
                # file is a file
                last_dir = target_path.split('/')[-1]
                if last_dir == self.target_path:
                    # last_dir is the same as target_path
                    self.attempt_upload(os.path.join(target_path, file), target_path)
                else:
                    self.attempt_upload(os.path.join(target_path, file), last_dir)
            time.sleep(1)

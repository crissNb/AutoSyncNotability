# AutoSyncNotability

# I'M NOT RESPONSIBLE FOR ANY DAMAGE/LOSS OF YOUR NOTABILITY FILES! This program is primarily made just for me, I cannot gauarentee it will work for an average joe

This project is a heavily hard coded hack designed to automatically sync PDF files to Notability. In other words, this program automatically converts a given PDF file (or files) to Notability format and imports it into Notability.
Works on all operating systems (including Linux) and doesn't deserialize NSKeyedArchive encoded files; instead, it directly modifies them (which is why it works on all operating systems).

## Motivation
This program proves to be exceptionally valuable if you frequently receive PDF files that you wish to annotate. Importing such files into Notability can often be quite tedious, involving multiple button presses and the hassle of navigating to locate the correct PDF file.

With a seamless integration between this program and Notability, you can completely forget about importing files you desire to annotate. All of the files will automatically be present in Notability, ready for you to annotate on.

## Context
Notability has its proprietary file format with the extensions of `.nbn`. When a PDF file is imported into Notability, the application creates an `.nbn` file. To the best of my knowledge, there are no tools available other than Notability itself that can convert a PDF file into the Notability proprietary format. Most of the data is stored in a file called `Session.xml`, which is serialized NSKeyedArchive. Unarchiving and archiving NSKeyedArchive can typically only be done on macOS operating systems (archiving, in particular, although there are software tools capable of decoding NSKeyedArchive on other operating systems). As a clever workaround, I have devised a hacky solution that involves directly modifying the archived XML file, which surprisingly yields excellent results.

## Requirements / Dependencies
- PyPDF2
- [My personal fork of iCloudPy](https://github.com/crissNb/icloudpy)

## Installation
It is recommended to install the dependencies in python virtual environment. A python virtual environment can be created via:
```bash
python3 -m venv venv
```
To activate the virtual environment, execute
```bash
source venv/bin/activate
```

Then install the requirements (see above).

Before running the application, you need to be signed into your iCloud account. This can be done via:
```bash
icloud --username=youremail@apple.com
```
It is recommended to store your password in the system keyring.

## Usage
Execute the program in a virtual environment
```bash
python .
```
This will start a process that runs indefinitely. The program creates a server socket on port `8000`, enabling communication with other software. In this way, other programs can notify AutoSyncNotability to convert specific PDF files located at a given path.

The communication message format follows the structure below:
```bash
PDF_FILE_PATH:::CHANGED;;;PDF_FILE_PATH:::CHANGED
```

...where `CHANGED` is a string representation of a boolean value.

Whenever AutoSyncNotability receives a file and successfully converts the PDF file to the corresponding `.nbn` file, it creates a `.zip` archive and stores it in the `dump_folder` (see [configuration](#configuration)). Then, the file must be manually extracted and place extracted `.nbn` file should be placed in the folder. This step is necessary, as uploading an `.nbn` file from a local machine to iCloud is more challenging and prone to errors compared to moving an `.nbn` file from one iCloud location to another.

To streamline this process, you can set up Apple Shortcuts to automatically unarchive the `.zip` file and rename the extracted folder to `.nbn`. Additionally, you can schedule this Shortcut to run multiple times a day to fully automate the process.

## Configuration
Prior to using the program, configuration must be done. All possible configurations of the program are made by modifying the `$XDG_CONFIG_HOME/AutoSyncNotability/config.ini` file.

- `id` represents your iCloud email.

- `destination_name` is a location in iCloud where all Notability files are stored. This path can be  found under `~/Library/Mobile \Documents/` on macOS device.

- `dump_folder` is a folder that will be used for communication between your Apple device and this program. The folder must be located directly under your iCloud Drive.

The program operates by copying a pre-created template in Notability and utilizing it as a foundation to generate other `.nbn` files. Therefore, it is necessary for you to create base templates. The program will subsequently determine the appropriate template to use based on the PDF file name, employing Regex for matching.

## Todo
- CHANGED implementation (when a provided PDF file is marked as changed, swap the PDF file in Notability)

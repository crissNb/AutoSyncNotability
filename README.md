# AutoSyncNotability

# I'M NOT RESPONSIBLE FOR ANY DAMAGE/LOSS OF YOUR NOTABILITY FILES! This program is primarily made just for me, I cannot gauarentee it will work for an average joe

This project is a heavily hard coded hack designed to automatically sync PDF files to Notability. In other words, this program automatically converts a given PDF file (or files) to Notability format and imports it into Notability.
Works on all operating systems (including Linux) and doesn't deserialize NSKeyedArchive encoded files; instead, it directly modifies them (which is why it works on all operating systems).

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
Execute the program in virtual environment
```bash
python .
```
This will start a process that will be indefinitely run.

## Configuration

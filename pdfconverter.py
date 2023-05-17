import os
import shutil
import PyPDF2
from distutils.dir_util import copy_tree
import FoundationPlist

class PDFConverter:
    def __init__(self, pdf_file_path, reference_path):
        self.reference_path = reference_path
        self.pdf_file_path = pdf_file_path

    def convert(self):
        # make own copy of reference folder in current working directory in a folder
        copy_tree(self.reference_path, 'converted')

        pdf_file_name = os.listdir('converted/PDFs')[0]
        shutil.copyfile(self.pdf_file_path, os.path.join('converted/PDFs', pdf_file_name))

        # get number of pages in pdf
        pdf_file = open(self.pdf_file_path, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        page_count = len(pdf_reader.pages)

        # update plist file
        print(page_count)
        self.updatePlist(page_count)

    def updatePlist(self, page_count):
        plist_file_path = os.path.join('converted', 'Session.plist')

        plist = FoundationPlist.readPlist(plist_file_path)


        # modify values
        plist['$objects'][1]['$class']['CF$UID'] = 999


        # save modified plist object back to the file
        FoundationPlist.writePlist(plist, plist_file_path)

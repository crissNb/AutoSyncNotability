import os
import shutil
import PyPDF2
from distutils.dir_util import copy_tree
import plistlib

class PDFConverter:
    def __init__(self, pdf_file_path, reference_path):
        self.reference_path = reference_path
        self.pdf_file_path = pdf_file_path

    def convert(self):
        # make own copy of reference folder in current working directory in a folder
        copy_tree(self.reference_path, 'converted')

        pdf_file_name = os.listdir('converted/PDFs')[0]

        reference_pdf_file = open(os.path.join('converted/PDFs', pdf_file_name), 'rb')
        referece_pdf_reader = PyPDF2.PdfReader(reference_pdf_file)
        reference_page_count = len(referece_pdf_reader.pages)
        reference_pdf_file.close()

        shutil.copyfile(self.pdf_file_path, os.path.join('converted/PDFs', pdf_file_name))

        # get number of pages in pdf
        pdf_file = open(self.pdf_file_path, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        page_count = len(pdf_reader.pages)
        pdf_file.close()

        # update plist file
        self.updatePlist(page_count, reference_page_count)

    def updatePlist(self, page_count, reference_page_count):
        if page_count > reference_page_count:
            print("this aint gonna work :(")
            return

        plist_file_path = os.path.join('converted', 'Session.plist')
        with open(plist_file_path, 'rb') as f:
            plist = plistlib.load(f, fmt=plistlib.FMT_BINARY)

        if page_count >= 3:
            object_1_class = 91 + 13 * (page_count - 2)
            creationDate = 60 + 7 * (page_count - 2)
            object_2_class = 58 + 7 * (page_count - 2)
        else:
            object_1_class = 80
            creationDate = 55
            object_2_class = 52

        plist['$objects'][1]['$class'] = plistlib.UID(object_1_class)
        plist['$objects'][1]['NBNoteTakingSessionBundleVersionNumberKey'] = plistlib.UID(object_1_class - 5)
        plist['$objects'][1]['creationDate'] = plistlib.UID(creationDate)
        plist['$objects'][1]['NBNoteTakingSessionDocumentPaperLayoutModelKey'] = plistlib.UID(creationDate + 2)
        plist['$objects'][1]['NBNoteTakingSessionHandwritingLanguageKey'] = plistlib.UID(object_1_class - 4)

        plist['$objects'][1]['contentPlaybackEventManager'] = plistlib.UID(object_1_class - 3)
        plist['$objects'][1]['kNBNoteTakingSessionNoteLinkStoreKey'] = plistlib.UID(object_1_class - 1)
        plist['$objects'][1]['name'] = plistlib.UID(creationDate - 1)
        plist['$objects'][1]['packagePath'] = plistlib.UID(creationDate - 1)
        plist['$objects'][1]['subject'] = plistlib.UID(object_1_class - 6)
        plist['$objects'][1]['tags'] = plistlib.UID(object_2_class + 1)

        plist['$objects'][2]['$class'] = plistlib.UID(object_2_class)
        plist['$objects'][2]['Handwriting Overlay'] = plistlib.UID(object_2_class - 24)
        plist['$objects'][2]['NBAttributedBackingString'] = plistlib.UID(object_2_class - 17)
        plist['$objects'][2]['attributedString'] = plistlib.UID(object_2_class - 6)
        plist['$objects'][2]['mediaObjects'] = plistlib.UID(object_2_class - 25)
        plist['$objects'][2]['recordingTimestampString'] = plistlib.UID(object_2_class - 3)
        plist['$objects'][2]['reflowState'] = plistlib.UID(object_2_class - 28)

        plist['$objects'][12]['$class'] = plistlib.UID(object_2_class - 29)

        # clear objects array before adding new ones in:
        plist['$objects'][12]['NS.objects'] = [None] * page_count

        for i in range(page_count):
            if i == 0:
                plist['$objects'][12]['NS.objects'][i] = plistlib.UID(13)
            elif i == 1:
                plist['$objects'][12]['NS.objects'][i] = plistlib.UID(23)
            elif i == 2:
                plist['$objects'][12]['NS.objects'][i] = plistlib.UID(29)
            else:
                plist['$objects'][12]['NS.objects'][i] = plistlib.UID(29 + ((i - 3) * 7))

        for i in range((reference_page_count - page_count) * 7 + 1, 2, -1):
            plist['$objects'].pop(23)

        object_3_class = object_2_class - 26
        plist['$objects'][24]['$class'] = plistlib.UID(object_3_class)
        plist['$objects'][24]['nativeLayoutDeviceStringKey'] = plistlib.UID(object_3_class - 1)

        plist['$objects'][28]['$class'] = plistlib.UID(object_3_class + 8)
        plist['$objects'][28]['SpatialHash'] = plistlib.UID(object_3_class + 3)

        plist['$objects'][29]['$class'] = plistlib.UID(object_3_class + 7)
        plist['$objects'][29]['bezierPathsDataDictionary'] = plistlib.UID(object_3_class + 4)
        plist['$objects'][29]['groupsArrays'] = plistlib.UID(object_3_class + 6)
        plist['$objects'][29]['numcurves'] = plistlib.UID(object_3_class + 5)
        plist['$objects'][29]['numfractionalwidths'] = plistlib.UID(object_3_class + 5)
        plist['$objects'][29]['numpoints'] = plistlib.UID(object_3_class + 5)

        plist['$objects'][32]['$class'] = plistlib.UID(object_3_class - 3)

        plist['$objects'][35]['$class'] = plistlib.UID(object_3_class + 19)
        plist['$objects'][35]['NBAttributedBackingStringCodingKey'] = plistlib.UID(object_3_class + 10)
        plist['$objects'][35]['NBAttributedLayoutStringCodingKey'] = plistlib.UID(object_3_class + 16)

        plist['$objects'][36]['NS.keys'][0] = plistlib.UID(object_3_class + 11)
        plist['$objects'][36]['NS.keys'][1] = plistlib.UID(object_3_class + 12)
        plist['$objects'][36]['NS.objects'][0] = plistlib.UID(object_3_class + 13)
        plist['$objects'][36]['NS.objects'][1] = plistlib.UID(object_3_class + 15)

        plist['$objects'][39]['$class'] = plistlib.UID(object_3_class + 14)

        plist['$objects'][41]['$class'] = plistlib.UID(object_3_class - 3)

        plist['$objects'][42]['NS.keys'][0] = plistlib.UID(object_3_class + 11)
        plist['$objects'][42]['NS.keys'][1] = plistlib.UID(object_3_class + 12)
        plist['$objects'][42]['NS.objects'][0] = plistlib.UID(object_3_class + 17)
        plist['$objects'][42]['NS.objects'][1] = plistlib.UID(object_3_class + 18)
        plist['$objects'][43]['$class'] = plistlib.UID(object_3_class + 14)
        plist['$objects'][44]['$class'] = plistlib.UID(object_3_class - 3)


        plist['$objects'][46]['NS.keys'][0] = plistlib.UID(object_3_class + 11)
        plist['$objects'][46]['NS.keys'][1] = plistlib.UID(object_3_class + 12)
        plist['$objects'][46]['NS.objects'][0] = plistlib.UID(object_3_class + 21)
        plist['$objects'][46]['NS.objects'][1] = plistlib.UID(object_3_class + 22)

        plist['$objects'][48]['$class'] = plistlib.UID(object_3_class - 3)

        plist['$objects'][49]['NS.keys'][0] = plistlib.UID(object_3_class + 11)
        plist['$objects'][49]['NS.keys'][1] = plistlib.UID(object_3_class + 12)
        plist['$objects'][49]['NS.objects'][0] = plistlib.UID(object_3_class + 24)
        plist['$objects'][49]['NS.objects'][1] = plistlib.UID(object_3_class + 25)

        plist['$objects'][50]['$class'] = plistlib.UID(object_3_class + 14)
        plist['$objects'][51]['$class'] = plistlib.UID(object_3_class - 3)

        plist['$objects'][55]['$class'] = plistlib.UID(creationDate + 1)

        plist['$objects'][57]['$class'] = plistlib.UID(object_1_class - 7)
        plist['$objects'][57]['documentPaperAttributes'] = plistlib.UID(creationDate + 3)
        plist['$objects'][57]['pageLayoutArray'] = plistlib.UID(creationDate + 10)

        plist['$objects'][58]['$class'] = plistlib.UID(creationDate + 9)
        plist['$objects'][58]['lineStyle2'] = plistlib.UID(creationDate + 4)
        plist['$objects'][58]['paperIdentifier'] = plistlib.UID(creationDate + 5)
        plist['$objects'][58]['paperOrientation'] = plistlib.UID(creationDate + 7)
        plist['$objects'][58]['paperSize'] = plistlib.UID(creationDate + 6)
        plist['$objects'][58]['paperSizingBehavior'] = plistlib.UID(creationDate + 8)

        # clear objects array before adding new ones in:
        plist['$objects'][65]['NS.objects'] = [None] * page_count

        for i in range(page_count):
            if i == 0:
                plist['$objects'][65]['NS.objects'][i] = plistlib.UID(creationDate + 11)
            elif i == 1:
                plist['$objects'][65]['NS.objects'][i] = plistlib.UID(creationDate + 11 + 7)
            else:
                plist['$objects'][65]['NS.objects'][i] = plistlib.UID(creationDate + 11 + 7 + ((i - 2) * 6))


        plist['$objects'][66]['$class'] = plistlib.UID(creationDate + 17)
        plist['$objects'][66]['NS.keys'][0] = plistlib.UID(creationDate + 12)
        plist['$objects'][66]['NS.keys'][1] = plistlib.UID(creationDate + 13)
        plist['$objects'][66]['NS.keys'][2] = plistlib.UID(creationDate + 14)
        plist['$objects'][66]['NS.keys'][3] = plistlib.UID(creationDate + 15)
        plist['$objects'][66]['NS.keys'][4] = plistlib.UID(creationDate + 16)

        for i in range((reference_page_count - page_count) * 6 + 2, 2, -1):
            plist['$objects'].pop(73)

        plist['$objects'][77]['$class'] = plistlib.UID(object_1_class - 2)

        with open(plist_file_path, 'wb') as f:
            plistlib.dump(plist, f, fmt=plistlib.FMT_BINARY)

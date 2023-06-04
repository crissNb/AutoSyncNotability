import os
import shutil
import PyPDF2
import plistlib

class PDFConverter:
    def __init__(self, pdf_file_path, reference_path, pdf_file_name):
        self.reference_path = reference_path
        self.pdf_file_path = pdf_file_path

        if pdf_file_name.endswith('.pdf'):
            self.pdf_file_name = 'converted_' + pdf_file_name[:-4]
        else:
            self.pdf_file_name = 'converted_' + pdf_file_name

    # generate unique uuid
    def generateUUID(self):
        import uuid
        return str(uuid.uuid4()).upper()

    def convert(self):
        # make own copy of reference folder in current working directory in a folder
        shutil.copytree(self.reference_path, self.pdf_file_name)

        pdf_file_name = os.listdir(os.path.join(self.pdf_file_name, 'PDFs'))[0]

        reference_pdf_file = open(os.path.join(self.pdf_file_name, 'PDFs', pdf_file_name), 'rb')
        referece_pdf_reader = PyPDF2.PdfReader(reference_pdf_file)
        reference_page_count = len(referece_pdf_reader.pages)
        reference_pdf_file.close()

        shutil.copyfile(self.pdf_file_path, os.path.join(self.pdf_file_name, 'PDFs', pdf_file_name))

        # get number of pages in pdf
        pdf_file = open(self.pdf_file_path, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        page_count = len(pdf_reader.pages)
        pdf_file.close()

        # update plist file
        self.updatePlist(page_count, reference_page_count)

        # update metadata file
        self.updateMetaData()

    def updateMetaData(self):
        with open(os.path.join(self.pdf_file_name, 'metadata.plist'), 'rb') as f:
            plist = plistlib.load(f, fmt=plistlib.FMT_BINARY)

        uuid = self.generateUUID()
        plist['$objects'][14] = self.pdf_file_name
        plist['$objects'][15] = self.pdf_file_name
        plist['$objects'][19] = uuid

        with open(os.path.join(self.pdf_file_name, 'metadata.plist'), 'wb') as f:
            plistlib.dump(plist, f, fmt=plistlib.FMT_BINARY)

    def updatePlist(self, page_count, reference_page_count):
        if page_count > reference_page_count:
            print("this aint gonna work :(")
            return

        plist_file_path = os.path.join(self.pdf_file_name, 'Session.plist')
        with open(plist_file_path, 'rb') as f:
            plist = plistlib.load(f, fmt=plistlib.FMT_BINARY)

        if page_count >= 3:
            object_1_class = 91 + 13 * (page_count - 2) + 1
            creationDate = 60 + 7 * (page_count - 2) + 1
            object_2_class = 58 + 7 * (page_count - 2)
        elif page_count == 2:
            object_1_class = 92
            creationDate = 61
            object_2_class = 58
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

        # individual page modifications
        if page_count == 1:
            deletion_cnt = 31 * 7 + 1
            start_index = 24
            for i in range(deletion_cnt, 2, -1):
                plist['$objects'].pop(23)

        elif page_count == 2:
            deletion_cnt = (reference_page_count - page_count) * 7 + 1
            start_index = 30

            for i in range(2, deletion_cnt, 1):
                plist['$objects'].pop((28+ deletion_cnt) - i)

            plist['$objects'].pop(29)
        else:
            deletion_cnt = (reference_page_count - page_count) * 7 + 1
            start_index = 30 + (page_count - 2) * 7

            for i in range(2, deletion_cnt):
                plist['$objects'].pop(start_index)
            plist['$objects'].pop(start_index - 1)

        object_3_class = object_2_class - 26
        plist['$objects'][start_index]['$class'] = plistlib.UID(object_3_class)
        plist['$objects'][start_index]['nativeLayoutDeviceStringKey'] = plistlib.UID(object_3_class - 1)

        plist['$objects'][start_index + 4]['$class'] = plistlib.UID(object_3_class + 8)
        plist['$objects'][start_index + 4]['SpatialHash'] = plistlib.UID(object_3_class + 3)

        plist['$objects'][start_index + 5]['$class'] = plistlib.UID(object_3_class + 7)
        plist['$objects'][start_index + 5]['bezierPathsDataDictionary'] = plistlib.UID(object_3_class + 4)
        plist['$objects'][start_index + 5]['groupsArrays'] = plistlib.UID(object_3_class + 6)
        plist['$objects'][start_index + 5]['numcurves'] = plistlib.UID(object_3_class + 5)
        plist['$objects'][start_index + 5]['numfractionalwidths'] = plistlib.UID(object_3_class + 5)
        plist['$objects'][start_index + 5]['numpoints'] = plistlib.UID(object_3_class + 5)

        plist['$objects'][start_index + 8]['$class'] = plistlib.UID(object_3_class - 3)

        plist['$objects'][start_index + 11]['$class'] = plistlib.UID(object_3_class + 19)
        plist['$objects'][start_index + 11]['NBAttributedBackingStringCodingKey'] = plistlib.UID(object_3_class + 10)
        plist['$objects'][start_index + 11]['NBAttributedLayoutStringCodingKey'] = plistlib.UID(object_3_class + 16)

        plist['$objects'][start_index + 12]['NS.keys'][0] = plistlib.UID(object_3_class + 11)
        plist['$objects'][start_index + 12]['NS.keys'][1] = plistlib.UID(object_3_class + 12)
        plist['$objects'][start_index + 12]['NS.objects'][0] = plistlib.UID(object_3_class + 13)
        plist['$objects'][start_index + 12]['NS.objects'][1] = plistlib.UID(object_3_class + 15)

        plist['$objects'][start_index + 15]['$class'] = plistlib.UID(object_3_class + 14)

        plist['$objects'][start_index + 17]['$class'] = plistlib.UID(object_3_class - 3)

        plist['$objects'][start_index + 18]['NS.keys'][0] = plistlib.UID(object_3_class + 11)
        plist['$objects'][start_index + 18]['NS.keys'][1] = plistlib.UID(object_3_class + 12)
        plist['$objects'][start_index + 18]['NS.objects'][0] = plistlib.UID(object_3_class + 17)
        plist['$objects'][start_index + 18]['NS.objects'][1] = plistlib.UID(object_3_class + 18)
        plist['$objects'][start_index + 19]['$class'] = plistlib.UID(object_3_class + 14)
        plist['$objects'][start_index + 20]['$class'] = plistlib.UID(object_3_class - 3)


        plist['$objects'][start_index + 22]['NS.keys'][0] = plistlib.UID(object_3_class + 11)
        plist['$objects'][start_index + 22]['NS.keys'][1] = plistlib.UID(object_3_class + 12)
        plist['$objects'][start_index + 22]['NS.objects'][0] = plistlib.UID(object_3_class + 21)
        plist['$objects'][start_index + 22]['NS.objects'][1] = plistlib.UID(object_3_class + 22)

        plist['$objects'][start_index + 24]['$class'] = plistlib.UID(object_3_class - 3)

        plist['$objects'][start_index + 25]['NS.keys'][0] = plistlib.UID(object_3_class + 11)
        plist['$objects'][start_index + 25]['NS.keys'][1] = plistlib.UID(object_3_class + 12)
        plist['$objects'][start_index + 25]['NS.objects'][0] = plistlib.UID(object_3_class + 24)
        plist['$objects'][start_index + 25]['NS.objects'][1] = plistlib.UID(object_3_class + 25)

        plist['$objects'][start_index + 26]['$class'] = plistlib.UID(object_3_class + 14)
        plist['$objects'][start_index + 27]['$class'] = plistlib.UID(object_3_class - 3)

        plist['$objects'][start_index + 30] = self.pdf_file_name

        plist['$objects'][start_index + 31]['$class'] = plistlib.UID(creationDate + 1)

        plist['$objects'][start_index + 33]['$class'] = plistlib.UID(object_1_class - 7)
        plist['$objects'][start_index + 33]['documentPaperAttributes'] = plistlib.UID(creationDate + 3)
        plist['$objects'][start_index + 33]['pageLayoutArray'] = plistlib.UID(creationDate + 10)

        plist['$objects'][start_index + 34]['$class'] = plistlib.UID(creationDate + 9)
        plist['$objects'][start_index + 34]['lineStyle2'] = plistlib.UID(creationDate + 4)
        plist['$objects'][start_index + 34]['paperIdentifier'] = plistlib.UID(creationDate + 5)
        plist['$objects'][start_index + 34]['paperOrientation'] = plistlib.UID(creationDate + 7)
        plist['$objects'][start_index + 34]['paperSize'] = plistlib.UID(creationDate + 6)
        plist['$objects'][start_index + 34]['paperSizingBehavior'] = plistlib.UID(creationDate + 8)

        # clear objects array before adding new ones in:
        plist['$objects'][start_index + 41]['NS.objects'] = [None] * page_count

        for i in range(page_count):
            if i == 0:
                plist['$objects'][start_index + 41]['NS.objects'][i] = plistlib.UID(creationDate + 11)
            elif i == 1:
                plist['$objects'][start_index + 41]['NS.objects'][i] = plistlib.UID(creationDate + 11 + 7)
            else:
                plist['$objects'][start_index + 41]['NS.objects'][i] = plistlib.UID(creationDate + 11 + 7 + ((i - 2) * 6))


        plist['$objects'][start_index + 42]['$class'] = plistlib.UID(creationDate + 17)
        plist['$objects'][start_index + 42]['NS.keys'][0] = plistlib.UID(creationDate + 12)
        plist['$objects'][start_index + 42]['NS.keys'][1] = plistlib.UID(creationDate + 13)
        plist['$objects'][start_index + 42]['NS.keys'][2] = plistlib.UID(creationDate + 14)
        plist['$objects'][start_index + 42]['NS.keys'][3] = plistlib.UID(creationDate + 15)
        plist['$objects'][start_index + 42]['NS.keys'][4] = plistlib.UID(creationDate + 16)

        if (page_count == 1):
            for i in range((reference_page_count - page_count) * 6 + 2, 2, -1):
                plist['$objects'].pop(start_index + 49)
        else:
            deletion_cnt = (reference_page_count - page_count) * 6 + 1
            old_start_index = start_index
            start_index += 56 + ((page_count - 2) * 6)
            for i in range(2, deletion_cnt):
                plist['$objects'].pop(start_index)
            plist['$objects'].pop(start_index - 1)

            # update data accordingly
            last_page_number = creationDate + 19
            for i in range(1, page_count):
                page_class_id = creationDate + 17
                plist['$objects'][old_start_index + 49 + ((i - 1) * 6)]['$class'] = plistlib.UID(page_class_id)

                for j in range(5):
                    plist['$objects'][old_start_index + 49 + ((i - 1) * 6)]['NS.keys'][j] = plistlib.UID(last_page_number)
                    last_page_number += 1
                if i == 0:
                    last_page_number += 2
                else:
                    last_page_number += 1

        with open(plist_file_path, 'wb') as f:
            plistlib.dump(plist, f, fmt=plistlib.FMT_BINARY)

        if page_count == 1:
            plist['$objects'][start_index + 53]['$class'] = plistlib.UID(object_1_class - 2)
        else:
            plist['$objects'][start_index + 3]['$class'] = plistlib.UID(object_1_class - 2)

        with open(plist_file_path, 'wb') as f:
            plistlib.dump(plist, f, fmt=plistlib.FMT_BINARY)

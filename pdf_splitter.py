from PyPDF2 import PdfFileReader, PdfFileWriter
import os
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p','--path', help="path to folder where files are located to be processed", required=False)

    args = vars(parser.parse_args())

    # setup initial variables
    path = args["path"]
    outPath = os.path.abspath(os.getcwd())

    # set directory where files are stored as either path passed as an argument or as a subdirectory called results where the file is contained
    if path:
        inPath = os.path.abspath(path)
    else:
        inPath = os.path.abspath(os.getcwd())

    # set directory where files will be written as either path passed in argument or as a subdirectory '/files'
    if not os.path.exists(outPath+'/files'):
        os.makedirs(outPath+'/files')
    outPath = outPath+'/files'



    for file in os.listdir(inPath):
        if file.endswith(".pdf"):

            print("Converting: ", os.path.join(inPath, file))

            file_name = os.path.splitext(file)[0]
            pdf_file = open(file, 'rb')
            pdf_reader = PdfFileReader(pdf_file)
            pageNumbers = pdf_reader.getNumPages()
            if not os.path.exists(outPath + '/' + file_name):
                os.makedirs(outPath + '/' + file_name)

            for i in range(pageNumbers):
                pdf_writer = PdfFileWriter()
                pdf_writer.addPage(pdf_reader.getPage(i))
                split_motive = open(outPath + "/" + file_name + "/" + file_name + "_" + str(i+1) + '.pdf','wb')
                pdf_writer.write(split_motive)
                split_motive.close()

            pdf_file.close()
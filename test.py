import PyPDF2
import os
import re

files = list()
def file_list():
    """Ordner in einer Schleife durchlaufen, alle Dateinamen extrahieren und in Liste speichern"""
    #https://stackoverflow.com/questions/10377998/how-can-i-iterate-over-files-in-a-given-directory
    directory = "rechnungen"
    for file in os.listdir(directory):
         filename = os.fsdecode(file)
         if filename.endswith(".pdf"):
             invoice_document = os.path.join(filename)
             files.append(invoice_document)
    print(files)
def pdf_text_extraction():
    """Extrahiert den Text einer PDF Datei mit dem Dateinamen aus Funktion folder_iteration()"""
    for item in files:
        working_directory = os.getcwd()
        file_path = working_directory + "\\" + item
        print(file_path)
        fhandler = open(file_path, "rb")
        pdfreader= PyPDF2.PdfFileReader(fhandler)
        x=pdfreader.numPages
        pageobj=pdfreader.getPage(x-1)
        text=pageobj.extractText() #hier können die regex angesetzt werd
        print(text)


file_list()
pdf_text_extraction()
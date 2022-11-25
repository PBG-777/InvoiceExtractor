import PyPDF2
import os
import re


files = list()
folder = "rechnungen" #vorerst fester Ordner
# folder = input("Bitte Ordnernamen angeben") variabler Ordner für Abfrage bei Programmstart von TKinter

def file_list():
    """Ordner in einer Schleife durchlaufen, alle Dateinamen extrahieren und in Liste speichern"""
    #https://stackoverflow.com/questions/10377998/how-can-i-iterate-over-files-in-a-given-directory
    directory = "rechnungen"
    for file in os.listdir(directory):
         filename = os.fsdecode(file)
         if filename.endswith(".pdf"):
             invoice_document = os.path.join(filename)
             files.append(invoice_document)


def pdf_text_extraction():
    """Extrahiert den Text aller PDF Dateien mit dem Dateinamen aus der Liste "files" mit einer for Schleife"""
    for item in files:
        working_directory = os.getcwd()
        file_path = working_directory + "\\" + folder + "\\" + item
        print(file_path)
        fhandler = open(file_path, "rb")
        pdfreader= PyPDF2.PdfFileReader(fhandler)
        x=pdfreader.numPages
        pageobj=pdfreader.getPage(x-1)
        text=pageobj.extractText() #hier können die regex angesetzt werd, wir erhalten hier Strings

        #Regex hier einsetzen / später als eigene Funktion definieren

        #Regex: Firmenname
        firmenname = re.findall("[A-z0-9]+@([A-z0-9]+).",text)
        if firmenname:
            firmenname = firmenname[0]             #Firmenname final(von Email Adresse extrahiert)

        #Regex: Datum
        datum = re.findall("([0-9]{2}\.[0-9]{2}\.[0-9]{2,4})",text)
        datum = min(datum)                          #Rechnungsdatum final/kleinstes Datum aus Rechnung



file_list()
pdf_text_extraction()


import PyPDF2
import os
import re

# Allgemeiner Programmteil / danach folgen die Funktionen
files = list()          #hier kommen die Dateinamen rein
folder = "rechnungen"   #vorerst fester Ordner, siehe eine Zeile darunter
# folder = input("Bitte Ordnernamen angeben") variabler Ordner für Abfrage bei Programmstart von TKinter

def file_list():
    """Ordner in einer Schleife durchlaufen, alle Dateinamen extrahieren und in Liste speichern"""
    #https://stackoverflow.com/questions/10377998/how-can-i-iterate-over-files-in-a-given-directory
    directory = "rechnungen"       #hier der Unterordnern Name einsetzen, Unterordner des laufenden Projekts
    for file in os.listdir(directory):
         filename = os.fsdecode(file)
         if filename.endswith(".pdf"):
             invoice_document = os.path.join(filename)
             files.append(invoice_document)


def pdf_text_extraction():
    """Extrahiert den Text aller PDF Dateien mit dem Dateinamen aus der Liste "files" mittels for Schleife"""
    for item in files:
        working_directory = os.getcwd()
        file_path = working_directory + "\\" + folder + "\\" + item
        print(file_path)
        fhandler = open(file_path, "rb")
        pdfreader= PyPDF2.PdfFileReader(fhandler)
        x=pdfreader.numPages
        pageobj=pdfreader.getPage(x-1)
        text=pageobj.extractText() #hier können die regex angesetzt werd, wir erhalten hier Strings


        #Regex: Firmenname
        firmenname = re.findall("[A-z0-9]+@([A-z0-9]+).",text)
        if firmenname:
            firmenname = firmenname[0]      #Firmenname final  (von Email Adresse extrahiert, Achtung aktuell enthält nur eine Rechnung eine Mailadresse, deswegen sind einige Listen leer)
            print(firmenname.title())

        #Regex: Datum
        datum = re.findall("([0-9]{2}\.[0-9]{2}\.[0-9]{2,4})",text)
        datum = min(datum)                    #Rechnungsdatum final  (vorerst kleinstes Datum aus Rechnung gewählt)
        print(datum)


#führt aus
file_list()
pdf_text_extraction()


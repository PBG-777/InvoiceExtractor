import PyPDF2
import os
import re
import datetime
import sqlite3

# Datenbank
conn = sqlite3.connect('file_name') # verbindung mit datenbank
c = conn.cursor()
c.execute('')

conn.close()
    
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
    all_datasets = list() # Hier werden die extrahierten Datensätze gesammelt
    """Extrahiert den Text aller PDF Dateien mit dem Dateinamen aus der Liste "files" mittels for Schleife"""
    for item in files:
        current_dataset = dict()
        working_directory = os.getcwd()
        file_path = working_directory + "\\" + folder + "\\" + item
        print(file_path)
        fhandler = open(file_path, "rb")
        pdfreader= PyPDF2.PdfFileReader(fhandler)
        x=pdfreader.numPages
        pageobj=pdfreader.getPage(x-1)
        text=pageobj.extractText() #hier können die regex angesetzt werd, wir erhalten hier Strings
        #print(text)

        # Bitte hier unten die Regex einsetzen (wird später als eigene Funktion definiert)
        # mit Print testen

        #Regex: Firmenname
        firmenname = re.findall("[A-z0-9]+@([A-z0-9]+).",text)
        if firmenname:
            firmenname = firmenname[0]      #Firmenname final  (von Email Adresse extrahiert, Achtung aktuell enthält nur eine Rechnung eine Mailadresse, deswegen sind einige Listen leer)
            current_dataset["firmenname"] = firmenname
            print(firmenname.title())

        #Regex: Datum
        datum = re.findall("([0-9]{2}\.[0-9]{2}\.[0-9]{2,4})",text)
        datum = min(datum)                    #Rechnungsdatum final  (vorerst kleinstes Datum aus Rechnung gewählt)
        current_dataset["Datum"] = datum
        print(datum)

        # Regex: IBAN
        # https://de.wikipedia.org/wiki/Internationale_Bankkontonummer#Zusammensetzung
        # Annahme: Kontoidentifikation 11..30 Ziffern (theoretisch auch Buchstaben, aber dann wirds schwierig)
        iban = re.findall(r"[a-zA-Z]{2}\d{2}\s?(?:\d\s?){11,30}", text)
        if iban:
            iban = re.sub(r"\s+","",iban[0])
            current_dataset["iban"] = iban
            print(iban)

        # Regex: Gesamtbetrag
        # Annahme: Komma als Dezimaltrennzeichen
        gesamtbetrag = re.findall(r"\d{1,3}(?:\s?\d\d\d)*,\d\d", text)
        gesamtbetrag = [float(i.replace(",",".").replace(" ","")) for i in gesamtbetrag]
        gesamtbetrag = max(gesamtbetrag)
        current_dataset["gesamtbetrag"] = gesamtbetrag
        print(gesamtbetrag)

        # Regex Telefonnummer and Zahlungsfrist
        text_new = re.split("\n", text)
        for lst in text_new:
            if 'Telefon:' in lst or 'Tel:' in lst:
                telefonnummer = re.findall("[0-9]{4}[ ][/][ ]+?(?:\d\s?){7,11}|(?:\d\s?){7,11}", lst)
                current_dataset["Telefonnummer"] = telefonnummer[0]
            if 'Der Gesamtbetrag ist bis zum'in lst or 'Fälligkeitsdatum:' in lst:
                zahlungsfrist = re.findall("([0-9]{2}\.[0-9]{2}\.[0-9]{2,4})",lst)
                current_dataset["Zahlungsfrist"] = zahlungsfrist[0]
            if 'Zahlbar innerhalb' in lst or 'Zahlungsbedingungen' in lst:
                tags = re.findall("[0-9]{2}",lst)
                datum_1 = datetime.datetime.strptime(datum, "%d.%m.%Y")
                zahlungsfrist = datum_1 + datetime.timedelta(int(tags[0]))
                current_dataset["Zahlungsfrist"] = str(zahlungsfrist).split()[0]
            if 'Rechnungsnummer' in lst or 'Rechnungs-Nr.:' in lst or 'Rechnung Nr.' in lst:
                rechungsnummer = re.findall('([0-9]{1,8})', lst)
                current_dataset["Rechungsnummer"] = rechungsnummer[0]



        all_datasets.append(current_dataset)
    return all_datasets

#führt aus
file_list()
print(pdf_text_extraction())


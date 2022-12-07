import PyPDF2
import os
import re
import datetime
import sqlite3

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
    all_datasets = list()  # Hier werden die extrahierten Datensätze gesammelt
    for item in files:
        working_directory = os.getcwd()
        file_path = working_directory + "\\" + folder + "\\" + item
        fhandler = open(file_path, "rb")
        pdfreader= PyPDF2.PdfFileReader(fhandler)
        x=pdfreader.numPages
        pageobj=pdfreader.getPage(x-1)
        text=pageobj.extractText() #hier können die regex angesetzt werd, wir erhalten hier Strings
        all_datasets.append(regex_apply(text))
    return all_datasets


def regex_apply(text):
    """Hier werden die Regex definiert und auf den Text aus der Fkt. pdf_text_extraction angewendet"""
    #Regex: Firmenname
    missing = 'missing'
    current_dataset = dict()
    firmenname = re.findall("[A-z0-9]+@([A-z0-9]+).",text)
    # Firmenname final  (von Email Adresse extrahiert, Achtung aktuell enthält nur eine Rechnung eine Mailadresse, deswegen sind einige Listen leer)
    if firmenname:
        firmenname = firmenname[0]
        current_dataset["FIRMENNAME"] = firmenname
    else:
        current_dataset["FIRMENNAME"] = missing

    #Regex: Datum
    datum = re.findall("([0-9]{2}\.[0-9]{2}\.[0-9]{2,4})",text)
    datum = min(datum)                    #Rechnungsdatum final  (vorerst kleinstes Datum aus Rechnung gewählt)
    if datum:
        current_dataset["DATUM"] = datum
    else:
        current_dataset["DATUM"] = missing

    # Regex: IBAN
    # https://de.wikipedia.org/wiki/Internationale_Bankkontonummer#Zusammensetzung
    # Annahme: Kontoidentifikation 11..30 Ziffern (theoretisch auch Buchstaben, aber dann wirds schwierig)
    iban = re.findall(r"[a-zA-Z]{2}\d{2}\s?(?:\d\s?){11,30}", text)
    if iban:
        iban = re.sub(r"\s+","",iban[0])
        current_dataset["IBAN"] = iban
    else:
        current_dataset["IBAN"] = missing

    # Regex: IBAN
    # https://de.wikipedia.org/wiki/Internationale_Bankkontonummer#Zusammensetzung
    # Annahme: Kontoidentifikation 11..30 Ziffern (theoretisch auch Buchstaben, aber dann wirds schwierig)
    iban = re.findall(r"[a-zA-Z]{2}\d{2}\s?(?:\d\s?){11,30}", text)
    if iban:
        iban = re.sub(r"\s+", "", iban[0])
        current_dataset["IBAN"] = iban
    else:
        current_dataset["IBAN"] = missing

    # Regex: Gesamtbetrag
    # Annahme: Komma als Dezimaltrennzeichen
    gesamtbetrag = re.findall(r"\d{1,3}(?:\s?\d\d\d)*,\d\d", text)
    gesamtbetrag = [float(i.replace(",",".").replace(" ","")) for i in gesamtbetrag]
    gesamtbetrag = max(gesamtbetrag)
    if gesamtbetrag:
        current_dataset["GESAMTBETRAG"] = str(gesamtbetrag)
    else:
        current_dataset["GESAMTBETRAG"] = missing

    # Regex: Gesamtbetrag
    # Annahme: Komma als Dezimaltrennzeichen
    gesamtbetrag = re.findall(r"\d{1,3}(?:\s?\d\d\d)*,\d\d", text)
    gesamtbetrag = [float(i.replace(",",".").replace(" ","")) for i in gesamtbetrag]
    gesamtbetrag = max(gesamtbetrag)
    if gesamtbetrag:
        current_dataset["GESAMTBETRAG"] = gesamtbetrag
    else:
        current_dataset["GESAMTBETRAG"] = missing

    # Regex Telefonnummer, Gesamtbetrag, Zahlungsfrist, Rechnungsnummer
    text_new = re.split("\n", text)
    for lst in text_new:
        if 'Telefon:' in lst or 'Tel:' in lst:
            telefonnummer = re.findall("[0-9]{4}[ ][/][ ]+?(?:\d\s?){7,11}|(?:\d\s?){7,11}", lst)
            if telefonnummer:
                current_dataset["TELEFONNUMMER"] = telefonnummer[0]
            else:
                current_dataset["TELEFONNUMMER"] = missing
    for lst in text_new:
        if 'Der Gesamtbetrag ist bis zum'in lst or 'Fälligkeitsdatum:' in lst:
            zahlungsfrist = re.findall("([0-9]{2}\.[0-9]{2}\.[0-9]{2,4})",lst)
            if zahlungsfrist:
                current_dataset["ZAHLUNGSFRIST"] = zahlungsfrist[0]
            else:
                current_dataset["ZAHLUNGSFRIST"] = missing
    for lst in text_new:
        if 'Zahlbar innerhalb' in lst or 'Zahlungsbedingungen' in lst:
            tags = re.findall("[0-9]{2}",lst)
            datum_1 = datetime.datetime.strptime(datum, "%d.%m.%Y")
            zahlungsfrist = datum_1 + datetime.timedelta(int(tags[0]))
            if zahlungsfrist:
                current_dataset["ZAHLUNGSFRIST"] = str(zahlungsfrist).split()[0]
            else:
                current_dataset["ZAHLUNGSFRIST"] = missing
    for lst in text_new:
        if 'Rechnungsnummer' in lst or 'Rechnungs-Nr.:' in lst or 'Rechnung Nr.' in lst:
            rechungsnummer = re.findall('([0-9]{1,8})', lst)
            if rechungsnummer:
                current_dataset["RECHNUNGSNUMMER"] = rechungsnummer[0]
            else:
                current_dataset["RECHNUNGSNUMMER"] = missing
    return(current_dataset)


#führt aus
file_list()
#print(pdf_text_extraction())



# Datenbank  / Ideensammlung
#conn = sqlite3.connect('file_name') # verbindung mit datenbank
#c = conn.cursor()
#c.execute('')
#conn.close()

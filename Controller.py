import PyPDF2
import os
import re
import datetime


# Allgemeiner Programmteil / danach folgen die Funktionen
files = list()          #hier kommen die Dateinamen rein
folder = "rechnungen"   #vorerst fester Ordner, siehe eine Zeile darunter
# folder = input("Bitte Ordnernamen angeben") variabler Ordner für Abfrage bei Programmstart von TKinter

class Controller_class:
    def __init__(self):
        """Konstruktor"""
        pass

    def file_list(self):
        """Ordner in einer Schleife durchlaufen, alle Dateinamen extrahieren und in Liste speichern"""
        #https://stackoverflow.com/questions/10377998/how-can-i-iterate-over-files-in-a-given-directory
        directory = "rechnungen_temp"       #hier der Unterordnern Name einsetzen, Unterordner des laufenden Projekts
        for file in os.listdir(directory):
             filename = os.fsdecode(file)
             if filename.endswith(".pdf"):
                 invoice_document = os.path.join(filename)
                 files.append(invoice_document)


    def pdf_text_extraction(self):
        """Extrahiert den Text aller PDF Dateien mit dem Dateinamen aus der Liste "files" mittels for Schleife"""
        all_datasets = list()  # Hier werden die extrahierten Datensätze gesammelt
        controller_build.file_list()
        for item in files:
            working_directory = os.getcwd()
            #file_path = working_directory + "\\" + folder + "\\" + item
            file_path = os.path.join(working_directory, folder, item)
            fhandler = open(file_path, "rb")
            pdfreader= PyPDF2.PdfFileReader(fhandler)
            x=pdfreader.numPages
            pageobj=pdfreader.getPage(x-1)
            text=pageobj.extractText() #hier können die regex angesetzt werd, wir erhalten hier Strings
            all_datasets.append(controller_build.regex_apply(text))
        return all_datasets


    def regex_apply(self, text):
        """Hier werden die Regex definiert und auf den Text aus der Fkt. pdf_text_extraction angewendet"""
        #Regex: Firmenname
        current_dataset = dict()
        # Firmenname final  (von Email Adresse extrahiert, Achtung aktuell enthält nur eine Rechnung eine Mailadresse, deswegen sind einige Listen leer)
        firmenname = re.findall("[A-z0-9]+@([A-z0-9]+).",text)
        if firmenname:
            firmenname = firmenname[0]
            current_dataset["FIRMENNAME"] = firmenname.title()
        else:
            current_dataset["FIRMENNAME"] = "none"

        #Regex: Datum
        datum = re.findall("([0-9]{2}\.[0-9]{2}\.[0-9]{2,4})",text)
        datum = min(datum)                    #Rechnungsdatum final  (vorerst kleinstes Datum aus Rechnung gewählt)
        if datum:
            current_dataset["DATUM"] = datum
        else:
            current_dataset["DATUM"] = "none"

        # Regex: IBAN
        # https://de.wikipedia.org/wiki/Internationale_Bankkontonummer#Zusammensetzung
        # Annahme: Kontoidentifikation 11..30 Ziffern (theoretisch auch Buchstaben, aber dann wirds schwierig)
        iban = re.findall(r"[a-zA-Z]{2}\d{2}\s?(?:\d\s?){11,30}", text)
        if iban:
            iban = re.sub(r"\s+","",iban[0])
            current_dataset["IBAN"] = iban
        else:
            current_dataset["IBAN"] = "none"

        # Regex: Gesamtbetrag
        # Annahme: Komma als Dezimaltrennzeichen
        alle_betraege = re.findall(r"\d{1,3}(?:\s?\d\d\d)* ?,\d\d", text)
        alle_betraege_float = [float(i.replace(",",".").replace(" ","")) for i in alle_betraege]
        gesamtbetrag = max(alle_betraege_float)
        if gesamtbetrag:
            current_dataset["GESAMTBETRAG"] = str(gesamtbetrag)
        else:
            current_dataset["GESAMTBETRAG"] = "none"

        # Regex Telefonnummer, Gesamtbetrag, Zahlungsfrist, Rechnungsnummer

        rechnung = re.findall('Rechnungsnummer:\s?[0-9]{1,8}|Rechnungs-Nr.:\s?[0-9]{1,8}|Rechnung Nr.\s?[0-9]{1,8}', text)
        rechungsnummer = re.findall('([0-9]{1,8})', str(rechnung))
        if rechungsnummer:
            current_dataset["RECHNUNGSNUMMER"] = rechungsnummer[0]
        else:
            current_dataset["RECHNUNGSNUMMER"] = "none"

        betrag = re.findall("Der Gesamtbetrag ist bis zum\s?[0-9]{2}\.[0-9]{2}\.[0-9]{2,4}|"
                            "Fälligkeitsdatum:\s?[0-9]{2}\.[0-9]{2}\.[0-9]{2,4}|"
                            "bis zum\s?[0-9]{2}\.[0-9]{2}\.[0-9]{2,4}",text)
        zahlungsfrist = re.findall("([0-9]{2}\.[0-9]{2}\.[0-9]{2,4})", str(betrag))
        if zahlungsfrist:
            current_dataset["ZAHLUNGSFRIST"] = zahlungsfrist[0]
        else:
            betrag = re.findall("Zahlbar innerhalb\s?[0-9]{2}|Zahlungsbedingungen:\s?[0-9]{2}",text)
            tag = re.findall("[0-9]{2}", str(betrag))
            datum_1 = datetime.datetime.strptime(datum, "%d.%m.%Y")
            zahlungsfrist = datum_1 + datetime.timedelta(int(tag[0]))
            if zahlungsfrist:
                current_dataset["ZAHLUNGSFRIST"] = str(zahlungsfrist).split()[0]
            else:
                current_dataset["ZAHLUNGSFRIST"] = "none"

        # print(text)
        telefonnummer = re.findall("Telefon:\s[0-9]{4}\s[/]\s+?(?:\d\s?){7,11}|Telefon\s?(?:\d\s?){9,13}|Tel:\s(?:\d\s?){7,11}|Mobil\s?(?:\d\s?){7,13}", text)
        tel = re.findall("[0-9]{4}\s[/]\s+?(?:\d\s?){7,11}|\s(?:\d\s?){7,11}", str(telefonnummer))
        if tel:
            current_dataset["TELEFONNUMMER"] = tel[0]
        else:
            current_dataset["TELEFONNUMMER"] = "none"


        return(current_dataset)

controller_build = Controller_class()

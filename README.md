## About

Mini-Projekt der Gruppe-B1-1 für das Fach Programmierung für KI - WiSe22/23

Fachhochschule Südwestfalen

Thema: Extrahieren von Informationen aus PDF Dokumenten

Autoren: Alaa Haboubi, Paul Martin Hippenstiel, Peter Vitus Kipfstuhl, Bista Tark Raj, Philipp Bergau, Tark Raj Bista 


## Bestandteile des Programmes

Das Programm besteht aus 3 Modulen:
- Extraction.py
- View.py
- db.py

Zusätzlich ist ein Ordner mit Beispielrechnungen vorhanden.

## Voraussetzungen

Das Programm benötigt eine Python Installation.
Zudem müssen folgende Bibliotheken installiert sein:
-tkinter
-PyPDF2
-matplotlib
-datetime 
-re
-os
-mysql.connector

Zudem muss einer lokale Datenbank installiert sein.
Die Installation kann von folgendem Link gestartet werden:

https://dev.mysql.com/downloads/installer/

Nachdem die Datenbank installiert wurde, müssen in der Datei view.py in Zeile 203 die Zugangsdaten für die DB angepasst werden.
Dafür muss einfach das lokal vergebene Passwort anstelle des zweiten "root" eingetragen werden.

## Funktiosnweise

Zum Programmstart muss das Modul view.py ausgeführt werden, welches die anderen beiden Module ausführt.

Extraction.py ist für die Extraktion der Daten aus den Rechnungen zuständig. Es verwendet die Bibliothekt PyPDF2.
Zunächst werden alle Dateien in einem Ordner, bei denen es sich um PDFs handelt,in einer Liste gespeichert.
Anhand dieser Liste werden dann Regex auf die Rechnung angwendet, um die gewünschten Daten zu erhalten.
Die extrahierten Daten werden in einer lokalen Datenbank abgelegt, wofür das Modul db.py zuständig ist (die Anbindung einer Cloud-DB wäre ebenso möglich).
View.py öffnet eine tabellarische, grafische Übersicht aller Rechnungen. Hierfür wird die Bibliothek tkinter genutzt.
Das sich öffnende Fenster beinhaltet zudem eine grafische Darstellung mit der Bibliothek Matplotlib.


## Folgende Daten werden aus den Rechnungen extrahiert:
Firmenname  
IBAN  
Telefonnummer  
Rechnungsnummer  
Rechnungsdatum 
Rechnungsbetrag  
Zahlungsfrist  


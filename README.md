## About

Mini-Projekt der Gruppe-B1-1 für das Fach 
Programmierung für KI - WiSe22/23
Fachhochschule Südwestfalen
Thema: Extrahieren von Informationen aus PDF Dokumenten
Autoren: Alaa Haboubi, Paul Martin Hippenstiel, Philipp Bergau,  Peter Vitus Kipfstuhl, Bista Tark Raj


## Bestandteile des Programmes

Das Programm besteht aus 3 Modulen:
- Extraction.py
- View.py
- db.py

Zusätzlich ist ein Ordner mit Beispielrechnungen vorhanden.

## Voraussetzungen

Folgende Bibliotheken müssen installiert sein:
-tkinter
-PyPDF2
-matplotlib
-datetime 
-re
-os
-mysql.connector

## Funktiosnweise

Extraction.py ist für die Extraktion der Daten aus den Rechnungen zuständig. Es verwendet die Bibliothekt PyPDF2.
Zunächst werden alle Dateien in einem Ordner, bei denen es sich um PDFs handelt, per Schleife ausgelesen und in einer Liste gespeichert.
Anhand dieser Liste werden dann mittels einer Schleifer sieben verschiedene Regex auf die Rechnung angwendet, um die gewünschten Daten zu erhalten.
Die extrahierten Daten werden in einer Datenbank abgelegt, wofür das Modul db.py zuständig ist. Hier haben wir uns für eine lokale Datenbank, die auf dem Rechner isntalliert sein muss entschieden. Die Installation kann von folgendem Link gestartet werden:

Nachdem die Datenbank installiert wurde, müssen in der Datei view.py in Zeile 203 die Zugangsdaten für die DB angepasst werden.
Dafür muss einfach das lokal vergebene Passwort anstelle des zweiten "root" eingetragen werden.
Anschliessend kann View.py ausgeführt werden und öffnet eine tabellarische Übersicht aller Rechnungen´.
Es beinhaltet zudem eine grafische Darstellung mit der Bibliothek Matplotlib.


## Folgende Daten werden aus den Rechnungen extrahiert:
Firmenname  
IBAN  
Telefonnummer  
Rechnungsnummer  
Rechnungsdatum 
Rechnungsbetrag  
Zahlungsfrist  


import PyPDF2

fhandler = open("rechnung.pdf", "rb")
pdfreader= PyPDF2.PdfFileReader(fhandler)
x=pdfreader.numPages
pageobj=pdfreader.getPage(x-1)
text=pageobj.extractText()
print(text)


# Daten aus Pdf extrahieren
# Ordner vielen mit PDFs durchlaufen/Schleife
# Reguläre Ausdrücke bauen
# Datenbank erstellen
# Daten ablegen
# Interface für Anwendung bauen mit tkinter
# Github Projekt anlegen
# Vortrag vorbereiten

''
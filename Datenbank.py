# Implementierung Datenbank via sqlite3:

import sqlite3
from Controller import pdf_text_extraction


conn = sqlite3.connect('rechnung_data.db')   # Verbindung mit Datenbank "rechnung_data.db". Wird erstellt falls nicht vorhanden.
cur = conn.cursor() # Vergleichbar mit open(). Ermöglicht Funktionen der Bibliothek sqlite3.

cur.execute('DROP TABLE IF EXISTS Database') # Löschen der vorhandenen Datenbank, damit neue Datenbank erstellt werden kann. (Clearing)
cur.execute('CREATE TABLE Database (Firmenname TEXT, Datum TEXT, Iban TEXT, Gesamtbetrag TEXT, Telefonnummer TEXT, Rechnungsnummer TEXT, Zahlungsfrist TEXT)')
# Erstellung der Datenbank "Database" mit den jeweiligen Spalten sowie den dazugehörigen Datentypen. Zunächst per Default auf TEXT gesetzt.
# Diskussionsbedarf inwieweit durch Regex Laufzeit- effizientere Datentypen ermöglicht werden können.

rechnungen_normiert = [{'firmenname': 'fswfaki', 'Datum': '01.12.2022', 'iban': 'DE051882000000001928', 'gesamtbetrag': 819.91, 'Telefonnummer': '0234 / 500 60 10', 'Rechungsnummer': '1234', 'Zahlungsfrist': '08.12.2022'}, {'firmenname': 'sds','Datum': '21.11.2022', 'iban': 'DE72432042034023', 'gesamtbetrag': 30.7, 'Rechungsnummer': '12345', 'Zahlungsfrist': '2022-12-05', 'Telefonnummer': '1213213'}, {'firmenname': 'muellertest', 'Datum': '21.11.2022', 'iban': 'DE051882000000001928', 'gesamtbetrag': 358.79, 'Telefonnummer': '0234 / 500 60 10', 'Rechungsnummer': '1234', 'Zahlungsfrist': '28.11.2022'}]
# Listen-Elemente auf 7 dictionaries normiert.
# Verbesserungsbedarf Data_input: Fehlende Dictionary inputs auf None o.ä. setzen.
# Verbesserungsbedarf Programmierstil: Einheitliche Groß- bzw. Kleinschreibung sowie korrekte Rechtschreibung beachten.
def get_Data():
    for element in pdf_text_extraction():         # Schleife durchläuft die Elemente der Liste, die Elemente enthalten die Dictionaries.
        cur.execute('INSERT INTO Database VALUES (?,?,?,?,?,?,?) ', (element['FIRMENNAME'], element['DATUM'], element['IBAN'], element['GESAMTBETRAG'], element['RECHNUNGSNUMMER'], element['ZAHLUNGSFRIST'], element['TELEFONNUMMER']))
        # Für jedes einzelne Dictionary innerhalb der Liste werden die zugehörigen Werte der Keys in die Datenbank Database als VALUES eingepflegt.

    cur.execute('SELECT * FROM Database')       # Es werden alle Inhalte der Datenbank "Database" ausgewählt
    inhalt = cur.fetchall()                     # Es werden entsprechende (hier im Beispiel alle) Daten aus der Datenbank geholt
    conn.commit()                               # Ausführung der sqlite3-Anweisungen
    return  inhalt
#print(inhalt)                               # Print der ausgeworfenen Werte der Datenbank, scheint alles richtig zu sein :)


import mysql.connector
from Controller import Extraction

class db:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.my_db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def create_Table(self):
        cur = self.my_db.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS rechnungen (Firmenname TEXT, Datum TEXT, Iban TEXT, Gesamtbetrag TEXT, Rechnungsnummer VARCHAR(10) PRIMARY KEY,  Zahlungsfrist TEXT, Telefonnummer TEXT)')

    def get_rechnungen_keys(self):
        keys = []
        cur = self.my_db.cursor()
        cur.execute('SELECT Rechnungsnummer FROM rechnungen')
        inhalt = cur.fetchall()
        keys = [item for t in inhalt for item in t]
        return keys

    def set_Data(self):
        self.create_Table()
        rechnungs_keys = self.get_rechnungen_keys()
        cur = self.my_db.cursor()
        var = Extraction()

        for element in var.pdf_text_extraction():  # Schleife durchläuft die Elemente der Liste, die Elemente enthalten die Dictionaries.
            if str(element['RECHNUNGSNUMMER']) not in rechnungs_keys:
                cur.execute('INSERT INTO rechnungen (FIRMENNAME,DATUM,IBAN,GESAMTBETRAG,RECHNUNGSNUMMER,ZAHLUNGSFRIST,TELEFONNUMMER) VALUES ( %s, %s, %s, %s, %s, %s, %s) ', (
                element['FIRMENNAME'], element['DATUM'], element['IBAN'], element['GESAMTBETRAG'],
                element['RECHNUNGSNUMMER'], element['ZAHLUNGSFRIST'], element['TELEFONNUMMER']))
            self.my_db.commit()
    def get_data(self, offset, limit):
        self.create_Table()
        self.set_Data()
        cur = self.my_db.cursor()
        cur.execute("SELECT * FROM rechnungen LIMIT "+ str(offset) +","+str(limit))
        inhalt = cur.fetchall()  # Es werden entsprechende (hier im Beispiel alle) Daten aus der Datenbank geholt
        #cur.commit()  # Ausführung der sqlite3-Anweisungen
        return inhalt

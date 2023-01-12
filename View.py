import tkinter as tk
from db import *
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure
import matplotlib.dates as mdates
from datetime import datetime

class View():
    def __init__(self, geometry, title, host, username, password, database):
        """Konstruktor der Klasse View"""
        self.root = tk.Tk()
        self.geometry = geometry
        self.title = title
        self.database = db(host, username, password, database)
        self.database.create_Table()
        self.database.set_Data()


    def __plot_gesambetrag(self):
        """Extrafenster fuer Plot Gesamtbetrag vs. Datum"""
        def plot_xy():
            """Unterfunktion zum Plotten des XY-Plots"""
            # Erstelle Vektoren
            x_values = []
            y_values = []
            
            # Daten traversieren und von String in Datetime-Typ und Gleitkommazahl umwandeln
            for set in rechnungen_content:
                try:
                    x_value = datetime.strptime(set[0], "%d.%m.%Y")
                    y_value = float(set[1])
                    x_values.append(x_value)
                    y_values.append(y_value)
                except: # Überspringe bei Fehler bei Umwandlung
                    pass
                
            # Datumsvektor in Matplotlib-Format umwandeln
            datesxy = mdates.date2num(x_values)
            
            # Plot löschen
            ax.cla()
            # XY-Daten plotten. 
            ax.plot_date(datesxy, y_values)
            
            # X-Achsen-Einheiten auf Monate stellen
            locator = mdates.MonthLocator()
            ax.xaxis.set_major_locator(locator)
            # Datum automatisch formatieren
            ax.xaxis.set_major_formatter(mdates.AutoDateFormatter(locator))
            fig.autofmt_xdate()
            
            # Achsenbeschriftung und Gitter
            ax.set_xlabel('Datum')
            ax.set_ylabel('Rechnungsbetrag in €')
            ax.set_ylim(bottom=0)
            ax.grid(True)
            fig.subplots_adjust(bottom=0.25, left=0.2)
            
            # Tkinter Fenster neu zeichnen
            canvas.draw()

        def plot_histo():
            """Unterfunktion zum plotten des Histogramms"""
            # Dictionary für Histogramm erstellen
            histo = dict()
            
            # Daten traversieren und zu Histogrammdaten summieren
            for set in rechnungen_content:
               try:
                    monat_jahr = '.'.join(set[0].split(".")[1:3])   # Nur Monate berücksichtigen
                    monat_jahr = datetime.strptime(monat_jahr, "%m.%Y") # In Datetime-Typ umwandeln
                    if monat_jahr in histo:
                        histo[monat_jahr] +=  float(set[1])
                    else:
                        histo[monat_jahr] =  float(set[1])
               except: # Überspringe bei Fehler bei Umwandlung
                   pass
            
            # Histogramm sortieren nach Datum
            histo = dict(sorted(histo.items()))
            
            # Erstelle Vektoren zum plotten
            x_histo = []
            y_histo = []
            
            # Vektoren mit Daten aus Dictionary füllen
            for monat in histo:
                x_histo.append(monat)
                y_histo.append(histo[monat])
            
            # Plot löschen
            ax.cla()
            # bar Graph plotten
            ax.bar(x_histo, y_histo, width=15)
            
            # X-Achsen-Einheiten auf Monate stellen
            locator = mdates.MonthLocator()
            ax.xaxis.set_major_locator(locator)
            # Datum automatisch formatieren
            ax.xaxis.set_major_formatter(mdates.AutoDateFormatter(locator))
            fig.autofmt_xdate()

            # Achsenbeschriftung und Gitter
            ax.set_xlabel('Monat')
            ax.set_ylabel('Monatsumsatz in €')
            ax.set_ylim(bottom=0)
            ax.grid(True)
            fig.subplots_adjust(bottom=0.25, left=0.2)

            canvas.draw()
        
        # Daten aus Datenbank abholen
        rechnungen_content = self.database.get_column("Datum, Gesamtbetrag")
        # Ergebnis: Liste von Tuplen (Datumsstring, Betragsstring)             

        # Erstelle Zeichnungsfenster: 5 Zoll breit und 3 Zoll hoch
        fig = Figure(figsize=(5, 3), dpi=200)

        # Subplot erstellen
        ax = fig.add_subplot(111)
        
        # TKinter Fenster erstellen
        matplot_window = tk.Toplevel(self.root)
        matplot_window.wm_title("Gesamtbetrag vs. Datum")

        # Buttons erstellen um zwischen den Plots zu wechseln
        # Dazu Frame erstellen, in das die beiden Buttons eingefügt werden
        # Es wird mit dem "Pack" Layout-Manager gearbeitet
        # Vgl.: https://www.studytonight.com/tkinter/python-tkinter-frame-widget
        topframe = tk.Frame(matplot_window) 
        topframe.pack(side = tk.BOTTOM)    # Frame am oberen Rand platzieren
        button = tk.Button(topframe, text='Zu XY-Plot wechseln', command=plot_xy)  
        button.pack(side = tk.LEFT)     # Buttons nebeneinander packen
        button2 = tk.Button(topframe, text='Zu Histogramm wechseln', command=plot_histo)
        button2.pack(side = tk.LEFT)    # Buttons nebeneinander packen

        # Matplotlib figure in TK-Fenster einbetten
        # Vgl.: https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_tk_sgskip.html
        canvas = FigureCanvasTkAgg(fig, master=matplot_window)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Standardmäßig soll das Histogramm geplottet werden
        plot_histo()


    def get_title(self, row_number,column_num, title, y):
        """eine Methode um den Titel der Spalten zu vergeben"""
        frame_head = tk.Frame(self.root, bd=1, highlightthickness=0, height=50)
        frame_head.grid(row=row_number, column=column_num)
        open_frame_head = tk.Frame(frame_head, bd=2)
        label_title = tk.Label(open_frame_head, text=title, fg='blue', justify='center',
                                       font=('Arial', 10, 'bold'))
        label_title.grid(row=0, column=0, padx=10, pady=y)
        open_frame_head.pack()


    def display(self, offset):
        """Erstellt das tkinter Anwendungsfenster"""
        limit = 8
        self.root.geometry(self.geometry)
        self.root.title(self.title)
        # Daten, die von Datenbank abgeholt in variable rechnung_content speichern
        rechnungen_content = self.database.get_data(offset, limit)
        pdf_number = self.database.count_entry()

        self.get_title(0, 3, 'Rechnungsdaten',  1)
        self.get_title(1, 0, f'Anzahl Einträge: {pdf_number}',  3)
        # Erstelle Ueberschriften aus Keys des Dictionaries
        header = ['FIRMENNAME', 'DATUM', 'IBAN', 'GESAMTBETRAG (€)', 'RECHNUNGSNUMMER', 'ZAHLUNGSFRIST', 'TELEFONNUMMER']

        # Erstelle Tabelle
        i = 0
        for i in range(len(rechnungen_content)):
            for k in range(len(header)):
                h = tk.Entry(self.root, width=21, fg='green', justify='center',
                          font=('Arial', 11, 'bold'))
                h.grid(row=2, column=k)
                h.insert(tk.END, f'{header[k]}')
                e = tk.Entry(self.root, width=21, fg='black', justify='center',
                          font=('Arial', 11))
                e.grid(row=i+3, column=k)
                e.insert(tk.END, f'{rechnungen_content[i][k]}')

        back = offset - limit
        next = offset + limit
        # next und prev Buttons
        next_button = tk.Button(self.root, text='Next >', command=lambda: self.display(next),
                                fg='green', justify='center', font=('Arial', 12, 'bold'))
        next_button.grid(row=limit+3, column=3, ipadx=50, pady=10)
        prev_button = tk.Button(self.root, text='< Prev', command=lambda: self.display(back),
                                fg='green', justify='center', font=('Arial', 12, 'bold'))
        prev_button.grid(row=limit+4, column=3, ipadx=50)

        if (pdf_number <= next):
            next_button["state"] = "disabled"  # deaktiviere next Button
        else:
            next_button["state"] = "active"  # aktiviere next Button

        if (back >= 0):
            prev_button["state"] = "active"  # aktiviere Prev Button
        else:
            prev_button["state"] = "disabled"  # deaktiviere Prev Button

        self.get_title(limit+6, 3, 'Grafische Darstellung',  10)
        b = tk.Button(self.root, width=21, text="Plot Gesamtbetrag / Datum", font=('Arial', 9, 'bold'), command=self.__plot_gesambetrag)
        b.grid(row=limit+7, column=3, pady=1)

        if __name__ == "__main__":
            self.root.mainloop()


m = View('1200x450', "PDFs extraction", 'localhost', 'root', '12345678', 'rechnung_data')
m.display(0)
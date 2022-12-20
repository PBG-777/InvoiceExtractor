import tkinter as tk
from tkinter import *
from Controller import Extraction
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure
import matplotlib.dates as mdates
from datetime import datetime

class View():
    def __init__(self, geometry, title):
        self.geometry = geometry
        self.title = title

    # Extrafenster fuer Plot Gesamtbetrag vs. Datum
    def __plot_gesambetrag(self):
        matplot_window = tk.Toplevel(self.root)
        matplot_window.wm_title("Gesamtbetrag vs. Datum")
        controller_build = Extraction()         #Klasse Extraction, neue Instanz erstellen
        pdf_data = controller_build.pdf_text_extraction()  # Daten aus PDFs einlesen Funktionsaufruf NEU

        # Erstelle Vektoren
        x_values = []
        y_values = []
        for set in pdf_data:
            if "GESAMTBETRAG" in set and "DATUM" in set:
                x_values.append(datetime.strptime(set["DATUM"], "%d.%m.%Y"))
                y_values.append(float(set["GESAMTBETRAG"]))

        # Zeichne
        fig = Figure(figsize=(5, 4), dpi=200)
        dates = mdates.date2num(x_values)
        ax = fig.add_subplot(111)

        ax.plot_date(dates, y_values)
        #ax.hist(dates, weights=y_values)

        # Achsenformatierung: Nur Monate auf X-Achse
        locator = mdates.AutoDateLocator()
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(mdates.AutoDateFormatter(locator))
        fig.autofmt_xdate()

        ax.set_xlabel('Datum')
        ax.set_ylabel('Rechnungsbetrag')
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=matplot_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # eine Methode, Titel zu vergaben
    def get_title(self, row_number, title, y):
        frame_head = tk.Frame(self.root, bd=1, highlightthickness=0, width=1650, height=50)
        frame_head.grid(row=row_number, column=3)
        open_frame_head = tk.Frame(frame_head, bd=2)
        label_title = tk.Label(open_frame_head, text=title, fg='blue', justify='center',
                                       font=('Arial', 14, 'bold'))
        label_title.grid(row=0, column=0, padx=10, pady=y)
        open_frame_head.pack()
    # def create_button(self):



    def display(self):
        self.root = tk.Tk()
        self.root.geometry(self.geometry)
        self.root.title(self.title)
        controller_build = Extraction()               #Klasse Extraction, neue Instanz erstellen
        pdf_data = controller_build.pdf_text_extraction()  #Klasse Extraction, Funktionsaufruf


        self.get_title(0, 'Rechnungsdaten', 1)
        # Daten fuer Tabellengenerierung umwandeln
        lst= []
        for num in range(len(pdf_data)):
            new_data = {i:v for i,(k,v) in enumerate(pdf_data[num].items(), 0)}    # Ersetze keys in den dictionaries durch Zahlen
            lst.append(new_data)

        # Erstelle Ueberschriften aus keys des Dictionary
        header = []
        for head in pdf_data[0].keys():
            header.append(head)

        # Erstelle Tabelle
        for i in range(len(pdf_data)):
            for k in range(len(pdf_data[0])):
                h = Entry(self.root, width=21, fg='green', justify='center',
                          font=('Arial', 14, 'bold'))
                h.grid(row=1, column=k)
                h.insert(END, f'{header[k]}')
                e = Entry(self.root, width=21, fg='black', justify='center',
                          font=('Arial', 14, 'bold'))

                e.grid(row=i+2, column=k)
                e.insert(END, f'{lst[i].get(k)}')

        next_button = tk.Button(self.root, text='Next >', fg='green', justify='center', font=('Arial', 12, 'bold'))
        next_button.grid(row=i+3, column=3, ipadx=50, pady=10)
        prev_button = tk.Button(self.root, text='< Prev', fg='green', justify='center', font=('Arial', 12, 'bold'))
        prev_button.grid(row=i+4, column=3, ipadx=50)

        self.get_title(i+5, 'Grafische Darstellung', 10)
        plot_button = tk.Button(self.root, text="Plot Gesamtbetrag vs. Datum", font=('Arial', 12, 'bold'), command=self.__plot_gesambetrag)
        plot_button.grid(row=i+6, column=3, pady=1)

        if __name__ == "__main__":
            self.root.mainloop()

m = View('1650x500', "PDFs extraction")
m.display()
import tkinter as tk
from tkinter import *
from Controller import pdf_text_extraction
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure
import matplotlib.dates
from datetime import datetime

class View():
    def __init__(self, geometry, title):
        self.geometry = geometry
        self.title = title

    # Extrafenster fuer Plot Gesamtbetrag vs. Datum
    def __plot_gesambetrag(self):
        matplot_window = tk.Toplevel(self.root)
        matplot_window.wm_title("Gesamtbetrag vs. Datum")

        pdf_data = pdf_text_extraction()  # Daten aus PDFs einlesen

        # Erstelle Vektoren
        x_values = []
        y_values = []
        for set in pdf_data:
            if "GESAMTBETRAG" in set and "DATUM" in set:
                x_values.append(datetime.strptime(set["DATUM"], "%d.%m.%Y"))
                y_values.append(set["GESAMTBETRAG"])

        # Zeichne
        fig = Figure(figsize=(5, 4), dpi=200)
        dates = matplotlib.dates.date2num(x_values)
        ax = fig.add_subplot(111)
        ax.plot_date(dates, y_values)

        # Achsenformatierung: Nur Monate auf X-Achse
        ax.xaxis.set_major_locator(matplotlib.dates.MonthLocator())
        #ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%m'))
        fig.autofmt_xdate()

        canvas = FigureCanvasTkAgg(fig, master=matplot_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


    def display(self):
        self.root = tk.Tk()
        self.root.geometry(self.geometry)
        self.root.title(self.title)

        pdf_data = pdf_text_extraction()   # Daten aus PDFs einlesen

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
                h.grid(row=0, column=k)
                h.insert(END, f'{header[k]}')
                e = Entry(self.root, width=21, fg='black', justify='center',
                          font=('Arial', 14, 'bold'))

                e.grid(row=i+1, column=k)
                e.insert(END, f'{lst[i].get(k)}')

        b = tk.Button(self.root, text="Plot Gesamtbetrag vs. Datum", command=self.__plot_gesambetrag)
        b.grid(row=i+2, column=3)

        if __name__ == "__main__":
            self.root.mainloop()

m = View('1650x600', "PDFs extraction")
m.display()
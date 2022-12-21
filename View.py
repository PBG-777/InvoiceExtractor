import tkinter as tk
from tkinter import *
from Controller import pdf_text_extraction
from db import *
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure
import matplotlib.dates
from datetime import datetime

class View():
    def __init__(self, geometry, title):
        self.root = tk.Tk()
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

    # eine Methode, Titel zu vergaben
    def get_title(self, row_number,column_num, title, y):
        frame_head = tk.Frame(self.root, bd=1, highlightthickness=0, width=1650, height=50)
        frame_head.grid(row=row_number, column=column_num)
        open_frame_head = tk.Frame(frame_head, bd=2)
        label_title = tk.Label(open_frame_head, text=title, fg='blue', justify='center',
                                       font=('Arial', 14, 'bold'))
        label_title.grid(row=0, column=0, padx=10, pady=y)
        open_frame_head.pack()
    # def create_button(self):



    def display(self, offset):
        limit = 2
        database = db('localhost', 'root', 'root', 'rechnung_data')
        rechnungen_content = database.get_data(offset, limit)

        pdf_data = pdf_text_extraction()   # Daten aus PDFs einlesen
        pdf_number = pdf_data.__len__()

        self.get_title(0, 3, 'Rechnungsdaten',  1)
        self.get_title(1, 0, f'Anzhal die Einträger:  {pdf_number}',  3)
        # Erstelle Ueberschriften aus keys des Dictionary
        header = []
        for head in pdf_data[0].keys():
            header.append(head)

        # Erstelle Tabelle
        i = 0
        for i in range(len(rechnungen_content)):
            for k in range(len(pdf_data[0])):
                h = Entry(self.root, width=21, fg='green', justify='center',
                          font=('Arial', 14, 'bold'))
                h.grid(row=2, column=k)
                h.insert(END, f'{header[k]}')
                e = Entry(self.root, width=21, fg='black', justify='center',
                          font=('Arial', 14, 'bold'))

                e.grid(row=i+3, column=k)
                e.insert(END, f'{rechnungen_content[i][k]}')

        back = offset - limit
        next = offset + limit
        next_button = tk.Button(self.root, text='Next >', command=lambda: self.display(next),
                                fg='green', justify='center', font=('Arial', 12, 'bold'))
        print(i)
        next_button.grid(row=i+4, column=3, ipadx=50, pady=10)
        prev_button = tk.Button(self.root, text='< Prev', command=lambda: self.display(back),
                                fg='green', justify='center', font=('Arial', 12, 'bold'))
        prev_button.grid(row=i+5, column=3, ipadx=50)

        if (pdf_number <= next):
            next_button["state"] = "disabled"  # disable next button
        else:
            next_button["state"] = "active"  # enable next button

        if (back >= 0):
            prev_button["state"] = "active"  # enable Prev button
        else:
            prev_button["state"] = "disabled"  # disable Prev button

        self.get_title(i+6, 3, 'Grafische Darstellung',  10)
        b = tk.Button(self.root, text="Plot Gesamtbetrag vs. Datum", font=('Arial', 12, 'bold'), command=self.__plot_gesambetrag)
        b.grid(row=i+7, column=3, pady=1)

        if __name__ == "__main__":
            self.root.mainloop()


m = View('1650x500', "PDFs extraction")
m.display(0)
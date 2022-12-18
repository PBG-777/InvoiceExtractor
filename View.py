import tkinter as tk
from tkinter import *
from Controller import pdf_text_extraction
from Datenbank import get_Data
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



    def display(self):
        self.root = tk.Tk()
        self.root.geometry(self.geometry)
        self.root.title(self.title)

        pdf_data = pdf_text_extraction()   # Daten aus PDFs einlesen
        pdf_number = pdf_data.__len__()

        self.get_title(0, 3, 'Rechnungsdaten',  1)
        self.get_title(1, 0, f'Anzhal die Einträger:  {pdf_number}',  3)
        # Daten fuer Tabellengenerierung umwandeln
        #lst= [('beer', '10.02.2022', 'DE49896921211468845544', '1394.06', '55482', '13.03.2022', ' 00155936827'), ('drub', '12.07.2022', 'DE94314562087091634579', '4656.78', '64728', '12.07.2022', 'none'), ('groettner', '17.08.2022', 'DE28913193442176104714', '535.44', '47039', '31.08.2022', ' 09007 54706'), ('troest', '03.09.2022', 'DE22660223450076279125', '3121.42', '56869', '28.09.2022', ' 0769930024'), ('hermighausen', '01.12.2022', 'DE81045093227175420355', '5628.9', '5946', '15.12.2022', 'none'), ('muellertest', '21.11.2022', 'DE051882000000001928', '358.79', '1234', '28.11.2022', '0234 / 500 60 10')]
        # for num in range(len(pdf_data)):
        #     new_data = {i:v for i,(k,v) in enumerate(pdf_data[num].items(), 0)}    # Ersetze keys in den dictionaries durch Zahlen
        #     lst.append(new_data)

        # Erstelle Ueberschriften aus keys des Dictionary
        header = []
        for head in pdf_data[0].keys():
            header.append(head)

        # Erstelle Tabelle
        for i in range(len(pdf_data)):
            for k in range(len(pdf_data[0])):
                h = Entry(self.root, width=21, fg='green', justify='center',
                          font=('Arial', 14, 'bold'))
                h.grid(row=2, column=k)
                h.insert(END, f'{header[k]}')
                e = Entry(self.root, width=21, fg='black', justify='center',
                          font=('Arial', 14, 'bold'))

                e.grid(row=i+3, column=k)
                e.insert(END, f'{get_Data()[i][k]}')

        next_button = tk.Button(self.root, text='Next >', fg='green', justify='center', font=('Arial', 12, 'bold'))
        next_button.grid(row=i+4, column=3, ipadx=50, pady=10)
        prev_button = tk.Button(self.root, text='< Prev', fg='green', justify='center', font=('Arial', 12, 'bold'))
        prev_button.grid(row=i+5, column=3, ipadx=50)

        self.get_title(i+6, 3, 'Grafische Darstellung',  10)
        b = tk.Button(self.root, text="Plot Gesamtbetrag vs. Datum", font=('Arial', 12, 'bold'), command=self.__plot_gesambetrag)
        b.grid(row=i+7, column=3, pady=1)

        if __name__ == "__main__":
            self.root.mainloop()


m = View('1650x500', "PDFs extraction")
m.display()
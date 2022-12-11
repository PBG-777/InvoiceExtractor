import tkinter  as tk
from tkinter import *
from Controller import pdf_text_extraction

class View():
    def __init__(self, geometry, title):
        self.geometry = geometry
        self.title = title

    def display(self):
        root = tk.Tk()
        root.geometry(self.geometry)
        root.title(self.title)
        lst= []

        for num in range(len(pdf_text_extraction())):
            new_data = {i:v for i,(k,v) in enumerate(pdf_text_extraction()[num].items(), 0)}
            lst.append(new_data)
        header = []
        for head in pdf_text_extraction()[0].keys():
            header.append(head)

        frame_head = tk.Frame(root, bd=1, highlightthickness=0, width=1650, height=50)
        frame_head.grid(row=0, column=0)
        open_frame_head = tk.Frame(frame_head, bd=2)
        label_oeffnen_liste = tk.Label(open_frame_head, text="Rechnungsdaten", fg='blue', justify='center',
                                       font=('Arial', 14, 'bold'))
        label_oeffnen_liste.grid(row=0, column=0, padx=10, pady=0)
        open_frame_head.pack()

        frameOben = tk.Frame(root, bd=1, highlightthickness=1, highlightbackground="light grey", width=1650, height=400)
        frameOben.grid(row=1, column=0, padx=2, pady=2)

        frame_head1 = tk.Frame(root, bd=2, highlightthickness=0, width=1650, height=50)
        frame_head1.grid(row=2, column=0)
        open_frame_head1 = tk.Frame(frame_head1, bd=2)
        label_oeffnen_liste1 = tk.Label(open_frame_head1, text="Rechnungsdaten im Grafische Darstellung", fg='blue', justify='center',
                                       font=('Arial', 14, 'bold'))
        label_oeffnen_liste1.grid(row=0, column=0, padx=10, pady=0)
        open_frame_head1.pack()

        frameUnten = tk.Frame(root, bd=1, highlightthickness=1, highlightbackground="light grey", width=1650,height=600)
        frameUnten.grid(row=3, column=0, padx=2, pady=2)

        for i in range(len(pdf_text_extraction())):
            for k in range(len(pdf_text_extraction()[0])):
                h = Entry(frameOben, width=21, fg='green', justify='center',
                          font=('Arial', 14, 'bold'))
                h.grid(row=0, column=k)
                h.insert(END, f'{header[k]}')
                e = Entry(frameOben, width=21, fg='black', justify='center',
                          font=('Arial', 14, 'bold'))

                e.grid(row=i+1, column=k)
                e.insert(END, f'{lst[i].get(k)}')

        if __name__ == "__main__":
            root.mainloop()

m = View('1650x600', "PDFs extraction")
m.display()
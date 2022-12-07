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

        for i in range(len(pdf_text_extraction())):
            for k in range(len(pdf_text_extraction()[0])):
                h = Entry(root, width=21, fg='green', justify='center',
                          font=('Arial', 14, 'bold'))
                h.grid(row=0, column=k)
                h.insert(END, f'{header[k]}')
                e = Entry(root, width=21, fg='black', justify='center',
                          font=('Arial', 14, 'bold'))

                e.grid(row=i+1, column=k)
                e.insert(END, f'{lst[i].get(k)}')

        if __name__ == "__main__":
            root.mainloop()

m = View('1650x600', "PDFs extraction")
m.display()
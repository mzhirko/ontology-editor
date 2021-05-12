import json
from tkinter import *
from tkinter import messagebox
from rdflib import Graph, Literal
from app import replace_triple, add_triple, remove_triple, get_all_triples, read_base_json, save_base_json

# creating widow
class Rem(Tk):
    def __init__(self):
        super().__init__()
        self.maxsize(400, 200)
        self.minsize(400, 200)
        self.title("Delete Triple")
        self.canvas = Canvas(width=1366, height=768, bg='pink')
        self.canvas.pack()
        self.heading = Label(text="Delete Triple", font=('Helvetica', 25, 'bold', 'italic'), bg='pink', fg='black')
        self.heading.place(x=100, y=0)
        self.g, self.data = read_base_json('data/dinos.json')
        self.triples = get_all_triples(self.g, self.data)
        self.triples = self.triples[1:]
        a = StringVar()

        def ent():
            triple = list()
            for item in self.triples:
                if str(item[0]) == a.get():
                    triple = item
                    break

            triple = triple[1:]
            if len(triple) == 0:
                messagebox.showinfo("Error", "Please Enter A Valid Id")
            else:
                d = messagebox.askyesno("Confirm", "Are you sure you want to delete the Triple?")
                if d:
                    remove_triple(self.g, triple)
                    messagebox.showinfo("Confirm", "Triple Deleted Successfully")
                    a.set("")
                    save_base_json(self.g, self.data, 'data/dinos.json')

        Label(self, text="Enter Triple Id: ", bg='pink', fg='black', font=('Helvetica', 15, 'bold')).place(x=5, y=40)
        Entry(self, textvariable=a, width=20).place(x=210, y=44)
        Button(self, text='Delete', width=15, font=('arial', 10), command=ent).place(x=200, y=90)


Rem().mainloop()

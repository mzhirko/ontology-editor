# import all the modules
from tkinter import *
import tkinter.messagebox
import json

from rdflib import Graph, Literal
from app import replace_triple, add_triple, remove_triple, get_all_triples, read_base_json, save_base_json


class Database:
    def __init__(self, master, *args, **kwargs):

        self.master = master
        self.canvas = Canvas(width=1366, height=768, bg='pink')
        self.canvas.pack()
        self.heading = Label(master, text="Update Triple", font=('Helvetica', 35, 'bold', 'italic'), bg='pink', fg='black')
        self.heading.place(x=100, y=0)

        # label and entry for id
        self.id_le = Label(master, text="Enter ID", font=('Helvetica', 10, 'bold'), bg='pink', fg='black')
        self.id_le.place(x=0, y=70)

        self.id_leb = Entry(master, font=('Helvetica', 10), width=10)
        self.id_leb.place(x=380, y=70)

        self.btn_search = Button(master, text="Search", width=8, height=0, bg='sky blue', command=self.search)
        self.btn_search.place(x=500, y=70)

        # lables  for the window
        self.first = Label(master, text="Enter Subject", font=('Helvetica', 10, 'bold'), bg='pink', fg='black')
        self.first.place(x=0, y=120)

        self.last = Label(master, text="Enter Type", font=('Helvetica', 10, 'bold'), bg='pink', fg='black')
        self.last.place(x=0, y=170)

        self.gender = Label(master, text="Enter Target ", font=('Helvetica', 10, 'bold'), bg='pink', fg='black')
        self.gender.place(x=0, y=220)

        # enteries for window

        self.first = Entry(master, width=25, font=('Helvetica', 10, 'bold'))
        self.first.place(x=380, y=120)

        self.last = Entry(master, width=25, font=('Helvetica', 10, 'bold'))
        self.last.place(x=380, y=170)

        self.gender = Entry(master, width=25, font=('Helvetica', 10, 'bold'))
        self.gender.place(x=380, y=220)

        # button to add to the database
        self.btn_add = Button(master, text='Update Triple', width=27, height=1, bg='sky blue', fg='black',
                              command=self.update)
        self.btn_add.place(x=380, y=420)

        self.g, self.data = read_base_json('data/dinos.json')

    def search(self, *args, **kwargs):
        triples = get_all_triples(self.g, self.data)
        triple = list()
        print(triples)
        for item in triples:
            if str(item[0]) == self.id_leb.get():
                triple = item
                break

        print(triple)

        self.n1 = triple[1]
        self.n2 = triple[2]
        self.n3 = triple[3]

        # inster into the enteries to update
        self.first.delete(0, END)
        self.first.insert(0, str(self.n1))

        self.last.delete(0, END)
        self.last.insert(0, str(self.n2))

        self.gender.delete(0, END)
        self.gender.insert(0, str(self.n3))

    def update(self, *args, **kwargs):
        triple_new = list()
        triple_new.append(self.first.get())
        triple_new.append(self.last.get())
        triple_new.append(self.gender.get())

        triple_old = list()
        triple_old.append(self.n1)
        triple_old.append(self.n2)
        triple_old.append(self.n3)
        print(triple_old, triple_new)

        replace_triple(self.g, triple_old, triple_new)

        tkinter.messagebox.showinfo("Success", "Updated Triple successfully")
        save_base_json(self.g, self.data, 'data/dinos.json')


root = Tk()
b = Database(root)
root.geometry("1000x760+0+0")
root.title("Update Triple Information")
root.mainloop()

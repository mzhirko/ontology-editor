from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from app import add_triple, read_base_json, save_base_json, get_all_triples
import os
import sys
from rdflib import Graph, Literal
import json

py = sys.executable

#creating window
class Add(Tk):
    def __init__(self):
        super().__init__()
        self.maxsize(500,417)
        self.minsize(500,417)
        self.title('Add Triple')
        self.canvas = Canvas(width=500, height=417, bg='pink')
        self.canvas.pack()
        self.heading = Label(text="Add Triple", font=('Helvetica', 25, 'bold', 'italic'), bg='pink', fg='black')
        self.heading.place(x=100, y=0)
        subject = StringVar()
        _type = StringVar()
        target = StringVar()
        _id = StringVar()
        self.data = dict()
        self.g, self.data = read_base_json('data/dinos.json')

#verifying input
        def asi():
            triple = list()
            triple.append(subject.get())
            triple.append(_type.get())
            triple.append(target.get())
            add_triple(self.g, triple)
            save_base_json(self.g, self.data, "data/dinos.json")

            messagebox.showinfo("Done", "Triple Inserted Successfully")
            ask = messagebox.askyesno("Confirm", "Do you want to add another triple?")
            if ask:
                self.destroy()
                os.system('%s %s' % (py, 'Add.py'))
            else:
                self.destroy()

        # label and input box
        Label(self, text='Triple Details',bg='pink', fg='white', font=('Helvetica', 25, 'bold')).pack()
        Label(self, text='Subject:', bg='pink', font=('Helvetica', 10, 'bold')).place(x=70, y=150)
        Entry(self, textvariable=subject, width=30).place(x=200, y=152)
        Label(self, text='Type:', bg='pink', font=('Helvetica', 10, 'bold')).place(x=70, y=200)
        Entry(self, textvariable=_type, width=30).place(x=200, y=202)
        Label(self, text='Target:', bg='pink', font=('Helvetica', 10, 'bold')).place(x=70, y=248)
        Entry(self, textvariable=target, width=30).place(x=200, y=250)
        Button(self, text="Save", bg='sky blue', width=15, command=asi).place(x=230, y=380)


g = read_base_json('data/dinos.json')

Add().mainloop()

from tkinter import *
from tkinter import messagebox
import os
import sys
from tkinter import ttk

py = sys.executable

import json

from rdflib import Graph, Literal
from tkinter import *
import tkinter as tk
import tkinter.font as tkFont


def read_base_json(path):
    graph = Graph()

    with open(path) as json_base:
        data = json.load(json_base)
        for entity in data:
            graph.add((Literal(entity['source']), Literal(entity['type']), Literal(entity['target'])))

    return graph, data


def save_base_json(graph, data, path):
    triples = list()

    for source, predicate, target in graph:
        triple = dict()
        f = False
        max_id = 0
        for item in data:
            if (item['source'] == source.split(r"'")[0]) & (item['type'] == predicate.split(r"'")[0]) & \
                    (item['target'] == target.split(r"'")[0]) & (not f):
                triple['id'] = item['id']
                f = True
            if item['id'] > max_id:
                max_id = item['id']
        if not f:
            triple['id'] = max_id + 1

        triple['source'] = source.split(r"'")[0]
        triple['type'] = predicate.split(r"'")[0]
        triple['target'] = target.split(r"'")[0]

        triples.append(triple)

    with open(path, "w") as json_base:
        json.dump(triples, json_base)



def add_triple(graph, triple):
    graph.add((Literal(triple[0]), Literal(triple[1]), Literal(triple[2])))


def remove_triple(graph, triple):
    graph.remove((Literal(triple[0]), Literal(triple[1]), Literal(triple[2])))


def replace_triple(graph, first, second):
    remove_triple(graph, first)
    add_triple(graph, second)


def get_subclasses(graph, class_name):
    subclasses = list()

    for subclass in graph.subjects(Literal('subclass'), Literal(class_name)):
        subclasses.append(subclass.split(r"'")[0])

    return subclasses


def get_instances(graph, class_name, answer):
    instances = list()

    for subclass in graph.subjects(Literal('subclass'), Literal(class_name)):
        get_instances(graph, subclass.split(r"'")[0], answer)

    for instance in graph.subjects(Literal('instance'), Literal(class_name)):
        answer.append(instance.split(r"'")[0])

    return instances


def get_objects_relationship(graph, relation_name, relation_value):
    answer = list()
    print(relation_name)
    print(relation_value)

    for source, predicate, target in graph:
        if predicate.split("'")[0] == relation_name:
            triple = dict()

            triple['source'] = source.split(r"'")[0]
            triple['type'] = predicate.split(r"'")[0]
            triple['target'] = target.split(r"'")[0]

            if relation_value == '' or relation_value == target.split(r"'")[0]:
                answer.append(source.split(r"'")[0])

    return answer


def get_objects_relationships(graph, relation_name, relation_values):
    answer = list()

    for relation_value in relation_values:
        answer.extend(get_objects_relationship(graph, relation_name, relation_value))

    return answer


def graph_query(graph, query, args):
    print('------', graph, query, args)

    answer = list()
    if query.upper() == 'Is a subclass of'.upper():
        answer = get_subclasses(graph, args[0])
    elif query.upper() == 'Is a instance of'.upper():
        get_instances(graph, args[0], answer)
    elif query.upper() == 'Has a relationship on'.upper():
        if args[1].upper() == 'has any value'.upper():
            answer = get_objects_relationship(graph, args[0], '')
        elif args[1].upper() == 'has a value equal to'.upper():
            answer = get_objects_relationship(graph, args[0], args[2])

    return sorted(answer)

def get_all_triples(graph, data):
    triples1 = list()
    for source, predicate, target in graph:
        triple = list()
        f = False
        max_id = 0
        for item in data:
            if (item['source'] == source.split(r"'")[0]) & (item['type'] == predicate.split(r"'")[0]) & \
                    (item['target'] == target.split(r"'")[0]) & (not f):
                triple.append(item['id'])
                f = True
            if item['id'] > max_id:
                max_id = item['id']
        if not f:
            triple.append(max_id + 1)

        triple.append(source.split(r"'")[0])
        triple.append(predicate.split(r"'")[0])
        triple.append(target.split(r"'")[0])

        triples1.append(triple)
    return triples1


# creating window
class MainWin(Tk):
    def __init__(self):
        super().__init__()
        self.configure(bg='pink')
        self.canvas = Canvas(width=1366, height=768, bg='pink')
        self.canvas.pack()
        self.maxsize(1320, 768)
        self.minsize(1320, 768)
#        self.state('zoomed')
        self.title('Ontology Development Tool')
        self.a = StringVar()
        self.b = StringVar()
        self.mymenu = Menu(self)

        # calling scripts

        def ib():
            os.system('%s %s' % (py, 'Update.py'))

        def ret():
            os.system('%s %s' % (py, 'Delete.py'))

        def sea():
            os.system('%s %s' % (py, 'Add.py'))

        def quarry():
            os.system('%s %s' % (py, 'Quarry.py'))
            print("executed")

        # creating table

        self.listTree = ttk.Treeview(self, height=14, columns=('Subject', 'Type', 'Target'))
        self.vsb = ttk.Scrollbar(self, orient="vertical", command=self.listTree.yview)
        self.hsb = ttk.Scrollbar(self, orient="horizontal", command=self.listTree.xview)
        self.listTree.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)
        self.listTree.heading("#0", text='ID')
        self.listTree.column("#0", width=50, minwidth=50, anchor='center')
        self.listTree.heading("Subject", text='Subject')
        self.listTree.column("Subject", width=200, minwidth=200, anchor='center')
        self.listTree.heading("Type", text='Type')
        self.listTree.column("Type", width=200, minwidth=200, anchor='center')
        self.listTree.heading("Target", text='Target')
        self.listTree.column("Target", width=200, minwidth=200, anchor='center')

        self.listTree.place(x=300, y=360)
        self.vsb.place(x=950, y=361, height=320)
        self.hsb.place(x=300, y=665, width=650)
        ttk.Style().configure("Treeview", font=('Times new Roman', 15))

        def ser():
            g, data = read_base_json('data/dinos.json')
            self.listTree.delete(*self.listTree.get_children())

            for row in get_all_triples(g, data):
                self.listTree.insert("", 'end', text=row[0], values=(row[1], row[2], row[3]))

        def check():
            # label and input box
            self.label3 = Label(self, text='Ontology Development Tool', fg='black', bg="pink", font=('Helvetica', 30, 'italic', 'bold'))
            self.label3.place(x=470, y=22)
            self.label6 = Label(self, text="Triple details", bg="pink", font=('Helvetica', 15, 'underline', 'bold', 'italic'))
            self.label6.place(x=570, y=300)
            self.button = Button(self, text='View Ontology', width=25, bg='sky blue', font=('Helvetica', 10),
                                 command=ser).place(x=1000, y=350)
            self.button = Button(self, text='Add Triple', width=25, bg='sky blue', font=('Helvetica', 10),
                                 command=sea).place(x=1000, y=400)
            self.brt = Button(self, text="Update Triple", width=15, bg='sky blue', font=('Helvetica', 10),
                              command=ib).place(x=1000, y=450)
            self.brt = Button(self, text="Delete Triple", width=15, bg='sky blue', font=('Helvetica', 10),
                              command=ret).place(x=1000, y=500)
            self.button = Button(self, text='Queries', width=15, bg='sky blue', font=('Helvetica', 10),
                                 command=quarry).place(x=1000, y=550)

        check()


if __name__ == "__main__":
    g, data = read_base_json('data/dinos.json')
    triples = get_all_triples(g, data)


    # find total number of rows and
    # columns in list
    total_rows = len(triples)
    total_columns = 4
    MainWin().mainloop()

import json
from tkinter import *
from tkinter import messagebox
from rdflib import Graph, Literal
from app import get_instances, get_objects_relationship, get_objects_relationships, get_subclasses, graph_query, read_base_json


# creating widow
class Rem(Tk):
    def __init__(self):
        super().__init__()
#        self.maxsize(400, 200)
#        self.minsize(400, 200)
        self.title("Query")
        self.geometry("500x500")
        self.heading = Label(text="Queries", font=('Helvetica', 25, 'bold', 'italic'), bg='pink', fg='black')
        self.heading.place(x=300, y=0)
        self.config(bg='pink')
        self.number_of_quarries = 0
        self.option_menu_list = list()
        self.entry_list = [StringVar(), StringVar(), StringVar(), StringVar()]
        self.clicked = StringVar()
        self.clicked_list = [StringVar()]
        self.clicked = StringVar()
        self.entry = StringVar()
        self.graph, self.data = read_base_json("data/dinos.json")
        a = StringVar()

        self.QuarriesList = ["Is a subclass of",
                             "Is a instance of",
                             "Has a relationship on",
                             "has any value",
                             "has a value equal to"]

        def execute_quarry():
            for item in self.entry_list:
                print(item)
            for item in self.clicked_list:
                print(item.get())

            ans = set()
            answer = set()
            for i in range(self.number_of_quarries + 1):
                print("----------------------------")
                tmp = list()
                tmp.append(self.entry_list[i].get())
                print("tmp - ", tmp, " clicked - ", self.clicked_list[i].get())
                if (self.clicked_list[i].get() == self.QuarriesList[0]) | (self.clicked_list[i].get() == self.QuarriesList[1]):
                    print("asdofuahofiuahsdofdsuhfosih")
                    answer = set(graph_query(self.graph, self.clicked_list[i].get(), tmp))
                if self.clicked_list[i].get() == self.QuarriesList[2]:
                    print("Has relation on")
                    tmp.append(self.clicked_list[i + 1].get())
                    tmp.append(self.entry_list[i + 1].get())
                    print("tmp : ", self.clicked_list[i].get(), tmp)
                    answer = set(graph_query(self.graph, self.clicked_list[i].get(), tmp))

                if (self.clicked_list[i].get == self.QuarriesList[3]) | (self.clicked_list[i].get == self.QuarriesList[4]):
                    continue

                print("==", answer)
                if len(ans) > 0:
                    ans = ans.intersection(answer)
                    print(ans)
                else:
                    ans = answer

                if len(ans) == 0:
                    ans.add("Nothing Found")
                lbox = Listbox(width=50, height=50)
                for i in ans:
                    lbox.insert(0, i)
                lbox.grid(column=1, row=10)

        def add_quarry():
            self.number_of_quarries += 1
            self.option_menu_list.append(
                OptionMenu(self,
                           self.clicked_list[self.number_of_quarries],
                           self.QuarriesList[0],
                           self.QuarriesList[1],
                           self.QuarriesList[2],
                           self.QuarriesList[3],
                           self.QuarriesList[4]).grid(row=(self.number_of_quarries + 1) * 2 + 2, column=0, sticky=W))
            self.clicked_list.append(StringVar())

            self.clicked_list.append(self.clicked)
            Entry(self, textvariable=self.entry_list[self.number_of_quarries], width=20).grid\
                (row=(self.number_of_quarries + 1) * 2 + 3, column=0, sticky=W)

            self.entry_list.append(self.entry.get())
            print("add_quarry", self.clicked.get())

        def delete_quarry():
            print(self.option_menu_list)
            self.option_menu_list[self.number_of_quarries].grid_remove()
            self.option_menu_list.pop(self.number_of_quarries)
            self.number_of_quarries -= 1

        self.option_menu_list.append(
            OptionMenu(self,
                       self.clicked_list[self.number_of_quarries],
                       self.QuarriesList[0],
                       self.QuarriesList[1],
                       self.QuarriesList[2],
                       self.QuarriesList[3],
                       self.QuarriesList[4]).grid(row=self.number_of_quarries + 3, column=0, sticky=W))
        self.clicked_list.append(StringVar())

        Entry(self, textvariable=self.entry_list[self.number_of_quarries], width=20).grid\
            (row=self.number_of_quarries + 4, column=0, sticky=W)

        # drop.pack()
        Button(self, text='Execute query', width=15, bg='sky blue', font=('arial', 10), command=execute_quarry).grid\
            (row=0, column=0, sticky=W)
        Button(self, text='Add query', width=15, bg='sky blue', font=('arial', 10), command=add_quarry).grid\
            (row=1, column=0, sticky=W)


Rem().mainloop()

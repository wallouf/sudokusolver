#!/usr/bin/python3
from tkinter import *

                
class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        
        # self.f1 = Frame(master)
        # self.f1.grid(row=0, column=0)
        
        self.pack()
        self.create_widgets()

    def update_entry_value(self, event, text):
        # value
        widgetvalue = event.widget.get()
        if not (widgetvalue.isdecimal() and 0 < int(widgetvalue) < 10):
            text.set("")
        # else:
        #     self.label["text"] = event.widget.get()

    def create_widgets(self, frame=None):
        self.entriesvalues={}
        self.entries={}
        self.entrycount = 1
        self.offsetx = 0
        self.offsety = 0

        # self.label = Label(self, text='Affichage')
        # self.label.grid(column=0, row=10)

        for self.iti1 in range(1,10):
            
            self.posx = self.offsetx
            self.posy = self.offsety
            
            for self.iti2 in range(0,9):
                # Each 3 slot, return x to 0 and offset
                if (self.posx % 3) == 0:
                    self.posx = self.offsetx
                    self.posy += 1
                
                # create text variable 
                self.text = StringVar()

                # Init entry value
                self.text.set(self.entrycount)

                self.entriesvalues["entryvalue{0}".format(self.entrycount)] = self.text
                # Create entries
                self.entry = Entry(self, width=4, textvariable=self.text)
                self.entry.grid(column=self.posx, row=self.posy)
                # self.entry.bind('<KeyRelease>', self.update_entry_value)
                self.entry.bind('<KeyRelease>', lambda event, v=self.text: self.update_entry_value(event, v))

                self.entries["entry{0}".format(self.entrycount)] = self.entry
                
                # Increment
                self.entrycount += 1
                self.posx += 1

            # Increment position for next 9 blocs
            if (self.iti1 % 3) == 0:
                self.offsetx = 0
                self.offsety += 3
            else:
                self.offsetx += 3



root = Tk()

root.title('Sudoku')
root.geometry("400x300+500+300")

app = Application(master=root)
app.mainloop()
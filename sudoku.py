#!/usr/bin/python3
from tkinter import *
                
class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.entries_generated={}

        self.entries={}
        self.entries_hori=[]
        self.entries_vert=[]

        for iti1 in range(1,10):
            self.entries_hori.append({})
            self.entries_vert.append({})
        
        # self.f1 = Frame(master)
        # self.f1.grid(row=0, column=0)

        self.generate_sudoku()
        
        self.pack()
        self.create_widgets()

    def generate_sudoku(self):
        self.entries_generated[2] = 5
        self.entries_generated[5] = 9
        
        self.entries_generated[13] = 1
        self.entries_generated[15] = 8
        self.entries_generated[17] = 6
        
        self.entries_generated[20] = 1
        self.entries_generated[23] = 2
        
        self.entries_generated[36] = 2
        
        self.entries_generated[37] = 4
        self.entries_generated[38] = 7
        self.entries_generated[39] = 3

        self.entries_generated[52] = 9
        
        self.entries_generated[55] = 7
        self.entries_generated[58] = 5
        self.entries_generated[60] = 9
        self.entries_generated[61] = 8
        
        self.entries_generated[65] = 3
        self.entries_generated[68] = 8
        
        self.entries_generated[75] = 5
        self.entries_generated[76] = 6
        self.entries_generated[78] = 3
        self.entries_generated[81] = 4
        return

    def check_sudoku_rule(self, entry, text, posx, posy):
        # calcul square
        posx +=1
        widgetvalue = entry.get()
        square=1

        offsetx = 0
        offsety = 0

        if posx > 6:
            square += 2
            offsetx = 6
        elif posx > 3:
            square += 1
            offsetx = 3

        if posy > 6:
            square += 6
            offsety = 6
        elif posy > 3:
            square += 3
            offsety = 3

        # Calculate position
        square_offset = ((square - 1) * 9)
        elem = square_offset + ((posy - offsety - 1) * 3) + (posx - offsetx)
            
        # print("Check rule...")
        # print(posx)
        # print(posy)
        # print("")
        # print("Element:")
        # print(elem)
        # print("")
        # print("Square:")
        # print(square)
        # print("")

        square_dict = {}
        range_min = square_offset + 1
        range_max = square_offset + 10

        for iti1 in range(range_min,range_max):
            if elem == iti1:
                continue
            actual_value = self.entries.get("entry{0}".format(iti1)).get()
            if actual_value.isdecimal():
                square_dict[actual_value] = ""
        
        # check for square
        if widgetvalue in square_dict:
            text.set("")
            return
        
        # check for lines H
        h_lines_dict = {}
        h_lines_entries = self.entries_hori[(posy-1)]

        for iti1 in range(0,9):
            if (posx-1) == iti1:
                continue
            actual_value = h_lines_entries.get("entry{0}".format(iti1)).get()
            if actual_value.isdecimal():
                h_lines_dict[actual_value] = ""
        
        if widgetvalue in h_lines_dict:
            text.set("")
            return
        
        # check for lines V
        v_lines_dict = {}
        v_lines_entries = self.entries_vert[(posx-1)]

        for iti1 in range(0,9):
            if (posy-1) == iti1:
                continue
            actual_value = v_lines_entries.get("entry{0}".format(iti1)).get()
            if actual_value.isdecimal():
                v_lines_dict[actual_value] = ""
        
        if widgetvalue in v_lines_dict:
            text.set("")
            return

    def search_good_values(self):
        entrycount = 1
        offsetx = 0
        offsety = 0

        cursor = 0
        tester = 0
        possible_values = []

        for cursor in range(0,81):
            possible_values.append([])

        for iti1 in range(1,10):
            
            posx = offsetx
            posy = offsety
            print("")
            print("")
            print("offsetX:")
            print(offsetx)
            print("offsetY:")
            print(offsety)
            print("")
            print("")
            
            for iti2 in range(0,9):
                # Each 3 slot, return x to 0 and offset
                modulo=((posx+1) % 3)
                
                if entrycount in self.entries_generated:
                    # Increment
                    entrycount += 1
                    posx += 1
                    
                    if modulo == 0:
                        posx = offsetx
                        posy += 1
                    
                    continue
                
                print("")
                print("")
                print("Nb:")
                print(entrycount)
                print("X:")
                print(posx)
                print("Y:")
                print(posy)
                print("Mod:")
                print(modulo)
                
                for tester in range(1,10):
                    # calcul square
                    square=1

                    if posx > 5:
                        square += 2
                    elif posx > 2:
                        square += 1

                    if posy > 5:
                        square += 6
                    elif posy > 2:
                        square += 3

                    # Calculate position
                    square_offset = ((square - 1) * 9)

                    square_dict = []
                    range_min = square_offset + 1
                    range_max = square_offset + 10

                    for iti3 in range(range_min,range_max):
                        if entrycount == iti3:
                            continue
                        actual_value = self.entries.get("entry{0}".format(iti3)).get()
                        if actual_value.isdecimal():
                            square_dict.append(int(actual_value))
                    
                    # check for lines H
                    h_lines_dict = []
                    h_lines_entries = self.entries_hori[(posy)]

                    for iti4 in range(0,9):
                        if (posx) == iti4:
                            continue
                        actual_value = h_lines_entries.get("entry{0}".format(iti4)).get()
                        if actual_value.isdecimal():
                            h_lines_dict.append(int(actual_value))
                    
                    # check for lines V
                    v_lines_dict = []
                    v_lines_entries = self.entries_vert[(posx)]

                    for iti5 in range(0,9):
                        if (posy) == iti5:
                            continue
                        actual_value = v_lines_entries.get("entry{0}".format(iti5)).get()
                        if actual_value.isdecimal():
                            v_lines_dict.append(int(actual_value))
                    
                    if not ((tester in square_dict) or (tester in v_lines_dict) or (tester in h_lines_dict)):
                        possible_values[(entrycount-1)].append(tester)
                
                print(possible_values[(entrycount-1)])
                if len(possible_values[(entrycount-1)]) == 1:
                    self.entries["text{0}".format((entrycount-1))].set(possible_values[(entrycount-1)][0])

                
                # Increment
                entrycount += 1
                posx += 1
                
                if modulo == 0:
                    posx = offsetx
                    posy += 1

            # Increment position for next 9 blocs
            if (iti1 % 3) == 0:
                offsetx = 0
                offsety += 3
            else:
                offsetx += 3

    def update_entry_value(self, event, text, posx, posy):
        # value
        widgetvalue = event.widget.get()
        if not (widgetvalue.isdecimal() and 0 < int(widgetvalue) < 10):
            text.set("")
        else:
            self.check_sudoku_rule(event.widget, text, posx, posy)

    def create_widgets(self, frame=None):
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
                self.modulo=(self.posx % 3)
                if self.modulo != 3 and self.modulo == 0:
                    self.posx = self.offsetx
                    self.posy += 1
                
                # create text variable 
                self.text = StringVar()

                # Create entries
                self.entry = Entry(self, width=4, textvariable=self.text)
                self.entry.grid(column=self.posx, row=self.posy)

                # Pre-load sudoku
                if self.entrycount in self.entries_generated:
                    self.text.set(self.entries_generated[self.entrycount])
                    self.entry.config(state='disabled')

                # self.entry.bind('<KeyRelease>', self.update_entry_value)
                self.entry.bind('<KeyRelease>', lambda event, v=self.text, posx=self.posx, posy=self.posy: self.update_entry_value(event, v, posx, posy))

                self.entries["entry{0}".format(self.entrycount)] = self.entry
                self.entries["text{0}".format(self.entrycount)] = self.text
                self.entries_hori[(self.posy-1)]["entry{0}".format(self.posx)] = self.entry
                self.entries_vert[self.posx]["entry{0}".format((self.posy-1))] = self.entry
                
                # Increment
                self.entrycount += 1
                self.posx += 1

            # Increment position for next 9 blocs
            if (self.iti1 % 3) == 0:
                self.offsetx = 0
                self.offsety += 3
            else:
                self.offsetx += 3

        self.search_good_values()


root = Tk()

root.title('Sudoku')
root.geometry("400x300+500+300")

app = Application(master=root)
app.mainloop()
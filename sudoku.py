#!/usr/bin/python3
from tkinter import *
import time

current_milli_time = lambda: int(round(time.time() * 1000))
                
class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.possible_values_square={}
        self.possible_values_line={}
        self.possible_values_col={}
        
        self.key_line={}
        self.key_col={}

        self.entries_generated={}

        self.entries={}
        self.entries_hori=[]
        self.entries_vert=[]

        for iti1 in range(1,10):
            self.entries_hori.append({})
            self.entries_vert.append({})
        
        self.generate_sudoku()
        
        self.pack()
        begin = current_milli_time()
        self.create_widgets()
        end = current_milli_time()

        print("Duration : ", (end-begin))

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
    
    def update_entry_value(self, event, text, posx, posy):
        # value
        widgetvalue = event.widget.get()
        if not (widgetvalue.isdecimal() and 0 < int(widgetvalue) < 10):
            text.set("")
        else:
            self.check_sudoku_rule(event.widget, text, posx, posy)

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
            # print("offsetX:")
            # print(offsetx)
            # print("offsetY:")
            # print(offsety)
            # print("")
            # print("")
            
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
                
                # print("")
                # print("")
                # print("Nb:")
                # print(entrycount)
                # print("X:")
                # print(posx)
                # print("Y:")
                # print(posy)
                # print("Mod:")
                # print(modulo)
                
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
                # if len(possible_values[(entrycount-1)]) == 1:
                #     self.entries["text{0}".format(entrycount)].set(possible_values[(entrycount-1)][0])
                #     possible_values[(entrycount-1)] = []
                    # Reinit and retry to find solution

                
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

        #Search for solution
        for square in range(0,9):
            self.get_square_solution(possible_values, square)


        for line in range(1,10):
            self.get_line_solution(possible_values, line)


        for col in range(1,10):
            self.get_col_solution(possible_values, col)


        # Deduct solution
        mvt = 0

        while True:
            mvt = 0
            # Loop
            mvt = self.iterate_full_solution(possible_values, mvt)
            
            print("")
            print("\tMouvement: ", mvt)

            if mvt == 0:
                break

    def get_square_solution(self, possible_values, square):
        sq_min = (square * 9)
        sq_max = (square * 9) + 9
        
        self.possible_values_square[square] = possible_values[sq_min:sq_max]

    def get_line_solution(self, possible_values, line):
        hori_values = []
        hori_key = []

        squareoffset = 0
        yoffset = 0

        if line > 6:
            squareoffset = 54
            yoffset = 6
        elif line > 3:
            squareoffset = 27
            yoffset = 3
        
        xoffset = (line - 1  - yoffset) * 3
        
        for index in range(1,4):
            xindex = index + xoffset + squareoffset
            hori_key.append(xindex)

            hori_values.append(possible_values[(xindex -1)])

        for index in range(1,4):
            xindex = index + xoffset + squareoffset + 9
            hori_key.append(xindex)

            hori_values.append(possible_values[(xindex -1)])

        for index in range(1,4):
            xindex = index + xoffset + squareoffset + 18
            hori_key.append(xindex)

            hori_values.append(possible_values[(xindex -1)])

        self.key_line[line] = hori_key
        self.possible_values_line[line] = hori_values

    def get_col_solution(self, possible_values, col):
        vert_values = []
        vert_key = []
        
        squareoffset = 0
        yoffset = 0

        if col > 6:
            squareoffset = 6
            yoffset = 18
        elif col > 3:
            squareoffset = 3
            yoffset = 9

        for index in range(1,4):
            xindex = ((index - 1) * 3) + (col - squareoffset) + yoffset
            print("\tcase: ", xindex)
            vert_key.append(xindex)

            vert_values.append(possible_values[(xindex -1)])

        for index in range(1,4):
            xindex = ((index - 1) * 3) + (col - squareoffset) + yoffset + 27
            print("\tcase: ", xindex)
            vert_key.append(xindex)

            vert_values.append(possible_values[(xindex -1)])

        for index in range(1,4):
            xindex = ((index - 1) * 3) + (col - squareoffset) + yoffset + 54
            print("\tcase: ", xindex)
            vert_key.append(xindex)

            vert_values.append(possible_values[(xindex -1)])

        self.key_col[col] = vert_key
        self.possible_values_col[col] = vert_values

    def update_possible_values_catalog(self, possible_values, case, value):
        print("Case: ", case)
        print("value to remove: ", value)

        # Update square
        square = int((case - 1) / 9)
        
        for item in self.possible_values_square[square]:
            if value in item:
                item.remove(value)
        
        # Update line
        line = int(((case-(square*9))-1)/3) + 1 + (int(square/3) * 3)

        for index in range(0,9):
            if value in self.possible_values_line[line][index]:
                self.possible_values_line[line][index].remove(value)

        # Update colonne
        col = (((case - 1) - (square * 9)) % 3) + 1 + ((square % 3) * 3)

        for index in range(0,9):
            if value in self.possible_values_col[col][index]:
                self.possible_values_col[col][index].remove(value)
        
    def iterate_full_solution(self, possible_values, mvt):
        print("Begin square loop")
        for square in range(0,9):
            if self.iterate_square_solution(square, possible_values, mvt) > 0:
                return 1

        print("Begin line hori loop")
        for line in range(1,10):
            if self.iterate_line_solution(line, possible_values, mvt) > 0:
                return 1
        
        print("Begin col vert loop")
        for col in range(1,10):
            if self.iterate_col_solution(col, possible_values, mvt) > 0:
                return 1

        return mvt

    def iterate_line_solution(self, line, possible_values, mvt):
        #retrieve values for the line
        print("")
        hori_values = self.possible_values_line[line]
        hori_key = self.key_line[line]

        #Check for solutions in the 9 cases of the line
        print("LINE: ", line)
        print("\t",hori_values)
        for index in range(0,9):
            values = hori_values[index]
            case_readed = hori_key[index]
            hori_others_values = []
            
            if len(values) == 1:
                value = values[0]
                
                self.entries["text{0}".format(case_readed)].set(value)

                self.update_possible_values_catalog(possible_values, case_readed, value)
                
                return 1

            for index2 in range(0,9):
                if index == index2 or len(hori_values[index2]) == 0:
                    continue

                hori_others_values = hori_others_values + hori_values[index2]

            hori_others_values = set(hori_others_values)
            hori_unique_value = set(hori_values[index]) - hori_others_values
            
            if len(hori_unique_value) > 0:
                print("Unique line value:")
                print(hori_unique_value)

                value = hori_unique_value.pop()
                
                self.entries["text{0}".format(case_readed)].set(value)

                self.update_possible_values_catalog(possible_values, case_readed, value)

                return 1


        return mvt

    def iterate_col_solution(self, col, possible_values, mvt):
        #retrieve values for the line
        vert_values = self.possible_values_col[col]
        vert_key = self.key_col[col]

        #Check for solutions in the 9 cases of the col
        print("COL: ", col)
        print("\t",vert_values)
        for index in range(0,9):
            values = vert_values[index]
            case_readed = vert_key[index]
            vert_others_values = []
            
            if len(values) == 1:
                value = values[0]
                
                self.entries["text{0}".format(case_readed)].set(value)

                self.update_possible_values_catalog(possible_values, case_readed, value)

                return 1

            for index2 in range(0,9):
                if index == index2 or len(vert_values[index2]) == 0:
                    continue

                vert_others_values = vert_others_values + vert_values[index2]

            vert_others_values = set(vert_others_values)
            vert_unique_value = set(vert_values[index]) - vert_others_values
            
            if len(vert_unique_value) > 0:
                print("Unique col value:")
                print(vert_unique_value)

                value = vert_unique_value.pop()
                
                self.entries["text{0}".format(case_readed)].set(value)

                self.update_possible_values_catalog(possible_values, case_readed, value)

                return 1


        return mvt

    def iterate_square_solution(self, square, possible_values, mvt):
        square_values = self.possible_values_square[square]
        sq_min = (square * 9)
        sq_max = (square * 9) + 9

        print("SQUARE: ", square)
        print("\t",square_values)

        for index1 in range(0,9):
            square_others_values = []
            # Single result -> Set value and retry
            if len(square_values[index1]) == 1:
                value = square_values[index1][0]
                entrycount = sq_min + index1 + 1
                
                self.entries["text{0}".format(entrycount)].set(value)

                self.update_possible_values_catalog(possible_values, entrycount, value)
                
                return 1

            for index2 in range(0,9):
                if index1 == index2 or len(square_values[index2]) == 0:
                    continue

                square_others_values = square_others_values + square_values[index2]

            square_others_values = set(square_others_values)
            square_unique_value = set(square_values[index1]) - square_others_values
            
            if len(square_unique_value) > 0:
                print("Unique square value:")
                print(square_unique_value)

                value = square_unique_value.pop()
                entrycount = sq_min + index1 + 1
                
                self.entries["text{0}".format(entrycount)].set(value)

                self.update_possible_values_catalog(possible_values, entrycount, value)

                return 1

        return mvt


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
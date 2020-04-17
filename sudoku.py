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
        
        self.generate_sudoku_lvl_30()
        self.pack()
        self.create_sudoku_grid()
        
        begin = current_milli_time()
        self.get_all_possible_values()
        self.loop_apply_strategies()
        end = current_milli_time()

        print("Duration : ", (end-begin))

    def create_sudoku_grid(self, frame=None):
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

    def generate_sudoku_lvl_29(self):
        self.entries_generated[6] = 7
        self.entries_generated[7] = 8
        self.entries_generated[9] = 5

        self.entries_generated[13] = 1
        self.entries_generated[14] = 4
        self.entries_generated[15] = 9
        
        self.entries_generated[22] = 3
        self.entries_generated[25] = 9
        self.entries_generated[27] = 6
        
        self.entries_generated[29] = 1
        
        self.entries_generated[37] = 6
        self.entries_generated[38] = 8
        self.entries_generated[39] = 4
        self.entries_generated[44] = 3
        
        self.entries_generated[47] = 7
        
        self.entries_generated[55] = 9
        self.entries_generated[59] = 6
        
        self.entries_generated[70] = 9
        self.entries_generated[71] = 2
        self.entries_generated[72] = 5
        
        self.entries_generated[75] = 4
        self.entries_generated[77] = 8

    def generate_sudoku_lvl_30(self):
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

    def get_all_possible_values(self):
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
            vert_key.append(xindex)

            vert_values.append(possible_values[(xindex -1)])

        for index in range(1,4):
            xindex = ((index - 1) * 3) + (col - squareoffset) + yoffset + 27
            vert_key.append(xindex)

            vert_values.append(possible_values[(xindex -1)])

        for index in range(1,4):
            xindex = ((index - 1) * 3) + (col - squareoffset) + yoffset + 54
            vert_key.append(xindex)

            vert_values.append(possible_values[(xindex -1)])

        self.key_col[col] = vert_key
        self.possible_values_col[col] = vert_values

    def update_possible_values_catalog(self, case, value):
        print("Case: ", case)
        print("value to remove: ", value)

        # Update square
        square = int((case - 1) / 9)
        line = int(((case-(square*9))-1)/3) + 1 + (int(square/3) * 3)
        col = (((case - 1) - (square * 9)) % 3) + 1 + ((square % 3) * 3)
        
        square_item = case - 1 - (square * 9)
        line_item = col - 1
        col_item = line - 1

        # reset values to 0 for this case
        self.possible_values_square[square][square_item] = []
        self.possible_values_line[line][line_item] = []
        self.possible_values_col[col][col_item] = []
        
        for item in self.possible_values_square[square]:
            if value in item:
                item.remove(value)
        
        # Update line
        for index in range(0,9):
            if value in self.possible_values_line[line][index]:
                self.possible_values_line[line][index].remove(value)

        # Update colonne
        for index in range(0,9):
            if value in self.possible_values_col[col][index]:
                self.possible_values_col[col][index].remove(value)

    def loop_apply_strategies(self):
        # Deduct solution
        full_count = 0

        while True:
            print("")
            print("")
            print("Values:")
            for square in range(0,9):
                for values in range(len(self.possible_values_square[square])):
                    print("\t ",self.possible_values_square[square][values])
                print("")
            print("")
            print("")
            # Loop
            mvt = self.iterate_all_strategies()
            
            print("")
            print("\tMouvement: ", mvt)
            full_count += mvt

            if mvt == 0:
                break
        
        print("")
        print("END OF DEDUCT")
        print("")
        print("Mouvement: ", full_count)
        
    def iterate_all_strategies(self):
        # S1 - Unique choice scan
        if self.strategie_1_unique_choice():
            return 1
        # S2 - Hidden unique choice for line or col or square
        if self.strategie_2_hidden_unique_choice():
            return 1
        # S3 - Exclusive number for square
        if self.strategie_3_exclusive_region():
            return 1
        # S4 - Exclusive pair for line or col or square
        if self.strategie_4_exclusive_pairs():
            return 1
        # S5 - Exclusive number of line or col
        if self.strategie_5_exclusive_number_in_line_or_col():
            return 1

        print("")
        return 0

    def strategie_1_unique_choice(self):
        print("")
        print("#### S1 - Unique choice")
        for square in range(0,9):
            square_values = self.possible_values_square[square]
            sq_min = (square * 9)
            sq_max = (square * 9) + 9

            for index1 in range(0,9):
                # Single result -> Set value and retry
                if len(square_values[index1]) == 1:
                    value = square_values[index1][0]
                    entrycount = sq_min + index1 + 1
                    
                    self.entries["text{0}".format(entrycount)].set(value)
                    self.update_possible_values_catalog(entrycount, value)
                    print("\t\t ------------ Found ! ------------", entrycount)
                    return True

        return False

    def strategie_2_hidden_unique_choice(self):
        print("")
        print("#### S2 - Hidden unique choice")
        
        print("")
        print("\t Square part...")

        for square in range(0,9):
            square_values = self.possible_values_square[square]
            sq_min = (square * 9)

            for index1 in range(0,9):
                square_others_values = []

                for index2 in range(0,9):
                    if index1 == index2 or len(square_values[index2]) == 0:
                        continue

                    square_others_values = square_others_values + square_values[index2]

                square_others_values = set(square_others_values)
                square_unique_value = set(square_values[index1]) - square_others_values
                
                if len(square_unique_value) > 0:
                    entrycount = sq_min + index1 + 1
                    print("\t\t ------------ Found ! ------------")
                    print("\t\t Unique square value: ", entrycount, square_unique_value)

                    value = square_unique_value.pop()
                    
                    self.entries["text{0}".format(entrycount)].set(value)
                    self.update_possible_values_catalog(entrycount, value)

                    return True
        print("")
        print("\t Line part...")

        for line in range(1,10):
            #retrieve values for the line
            hori_values = self.possible_values_line[line]
            hori_key = self.key_line[line]

            #Check for solutions in the 9 cases of the line
            for index in range(0,9):
                values = hori_values[index]
                case_readed = hori_key[index]
                hori_others_values = []

                for index2 in range(0,9):
                    if index == index2 or len(hori_values[index2]) == 0:
                        continue

                    hori_others_values = hori_others_values + hori_values[index2]

                hori_others_values = set(hori_others_values)
                hori_unique_value = set(hori_values[index]) - hori_others_values
                
                if len(hori_unique_value) > 0:
                    print("\t\t ------------ Found ! ------------")
                    print("\t\t Unique line value: ", case_readed, hori_unique_value)

                    value = hori_unique_value.pop()
                    
                    self.entries["text{0}".format(case_readed)].set(value)
                    self.update_possible_values_catalog(case_readed, value)

                    return True

        print("")
        print("\t Col part...")

        for col in range(1,10):
            #retrieve values for the line
            vert_values = self.possible_values_col[col]
            vert_key = self.key_col[col]
            
            for index in range(0,9):
                values = vert_values[index]
                case_readed = vert_key[index]
                vert_others_values = []

                for index2 in range(0,9):
                    if index == index2 or len(vert_values[index2]) == 0:
                        continue

                    vert_others_values = vert_others_values + vert_values[index2]

                vert_others_values = set(vert_others_values)
                vert_unique_value = set(vert_values[index]) - vert_others_values
                
                if len(vert_unique_value) > 0:
                    print("\t\t ------------ Found ! ------------")
                    print("\t\t Unique col value: ", case_readed, vert_unique_value)

                    value = vert_unique_value.pop()
                    
                    self.entries["text{0}".format(case_readed)].set(value)
                    self.update_possible_values_catalog(case_readed, value)

                    return True

        return False

    def strategie_3_exclusive_region(self):
        print("")
        print("#### S3 - Exclusive region")

        for square in range(0,9):
            sq_min = (square * 9)

            # Search with exclu number tech
            for value_to_check in range(1,10):
                case_to_check = []
                for case in range(0,9):
                    if value_to_check in self.possible_values_square[square][case]:
                        case_to_check.append(case)

                case_to_check = set(case_to_check)

                if len(case_to_check) < 2:
                    continue

                # Scan each line or col
                for case in case_to_check:
                    line_found = False
                    col_found = False

                    absolute_case = sq_min + case + 1
                    absolute_line = int(((absolute_case-(square*9))-1)/3) + 1 + (int(square/3) * 3)
                    absolute_col = (((absolute_case - 1) - (square * 9)) % 3) + 1 + ((square % 3) * 3)

                    for line_index in range(len(self.possible_values_line[absolute_line])):
                        # Check if already present in other case in other square
                        # Calcul
                        line_values_to_check = self.possible_values_line[absolute_line][line_index]
                        # Get case from the line
                        squareoffset = 0
                        yoffset = 0
                        case_from_the_line = 0

                        if absolute_line > 6:
                            squareoffset = 54
                            yoffset = 6
                        elif absolute_line > 3:
                            squareoffset = 27
                            yoffset = 3
                        
                        xoffset = (absolute_line - 1  - yoffset) * 3

                        if line_index > 5:
                            case_from_the_line = line_index - 5 + xoffset + squareoffset + 18
                        elif line_index > 2:
                            case_from_the_line = line_index - 2 + xoffset + squareoffset + 9
                        else:
                            case_from_the_line = line_index + 1 + xoffset + squareoffset

                        square_from_line_to_check = int(case_from_the_line / 9)
                        # Check if found
                        if square_from_line_to_check != square and value_to_check in line_values_to_check:
                            line_found = True
                            break
                    
                    # If found in another square
                    if not line_found:
                        print("\t\t [S3] Values only possible in this square. LINE")
                        if self.clean_line_possible_values_for_ce_technique(square, absolute_line, value_to_check) > 0:
                            print("\t\t ------------ Found ! ------------")
                            print("\t\t Square: ", square)
                            print("\t\t Case: ", absolute_case)
                            print("\t\t Value: ", value_to_check)
                            return True

                    for col_index in range(len(self.possible_values_col[absolute_col])):
                        # Check if already present in other case in other square
                        # Calcul
                        col_values_to_check = self.possible_values_col[absolute_col][col_index]
                        # Get case from the col
                        case_from_the_col = 0
                        squareoffset = 0
                        yoffset = 0

                        if absolute_col > 6:
                            squareoffset = 6
                            yoffset = 18
                        elif absolute_col > 3:
                            squareoffset = 3
                            yoffset = 9

                        if col_index > 5:
                            case_from_the_col = ((col_index - 6) * 3) + (absolute_col - squareoffset) + yoffset + 54
                        elif col_index > 2:
                            case_from_the_col = ((col_index - 3) * 3) + (absolute_col - squareoffset) + yoffset + 27
                        else:
                            case_from_the_col = ((col_index) * 3) + (absolute_col - squareoffset) + yoffset
                        
                        square_from_line_to_check = int(case_from_the_col / 9)

                        # Check if found
                        if square_from_line_to_check != square and value_to_check in col_values_to_check:
                            col_found = True
                            break
                    
                    # If found in another square
                    if not col_found:
                        print("\t\t [S3] Values only possible in this square. COL")
                        if self.clean_col_possible_values_for_ce_technique(square, absolute_col, value_to_check) > 0:
                            print("\t\t ------------ Found ! ------------")
                            print("\t\t Square: ", square)
                            print("\t\t Case: ", absolute_case)
                            print("\t\t Value: ", value_to_check)
                            return True

        return False

    def strategie_4_exclusive_pairs(self):
        print("")
        print("#### S4 - Exclusive pairs")
        #Exclusive pairs

        for square in range(0,9):
            exclusive_pairs = {}
            for index1 in range(0,9):
                if len(self.possible_values_square[square][index1]) == 2:
                    exclusive_pairs[index1] = self.possible_values_square[square][index1]
            
            if len(exclusive_pairs) > 0:
                print("\t\t EXCLUSIVE PAIRS TO CHECK. square: ", square)
                for key1 in exclusive_pairs.keys():
                    for key2 in exclusive_pairs.keys():
                        if key2 == key1:
                            continue

                        if exclusive_pairs[key1] == exclusive_pairs[key2]:
                            print("\t\t ------------ Found ! ------------")
                            print("\t\t case found.")
                            print("\t\t\t ",exclusive_pairs[key1])
                            print("\t\t\t ",exclusive_pairs[key2])

        return False

    def strategie_5_exclusive_number_in_line_or_col(self):
        print("")
        print("#### S5 - Exclusive number in line / col")

        for square in range(0,9):
            for index1 in range(0,9):
                item1_case = index1 + 1 + (square * 9)
                item1_line = int(((item1_case-(square*9))-1)/3) + 1 + (int(square/3) * 3)
                item1_col = (((item1_case - 1) - (square * 9)) % 3) + 1 + ((square % 3) * 3)
                item1_posx = item1_col - 1
                item1_posy = item1_line - 1
                
                for tested_value in range(1,10):
                    if tested_value not in self.possible_values_square[square][index1]:
                        continue
                    

                    found_aligned_line_index = []
                    found_aligned_col_index = []

                    found_aligned_line_index.append(item1_posx)
                    found_aligned_col_index.append(item1_posy)
                    
                    found_line_aligned = False
                    found_col_aligned = False
                    # Check other case
                    for index2 in range(0,9):
                        if index2 == index1:
                            continue
                        # If the tested value is in this case too -> Check line
                        if tested_value in self.possible_values_square[square][index2]:
                            item2_case = index2 + 1 + (square * 9)
                            item2_line = int(((item2_case-(square*9))-1)/3) + 1 + (int(square/3) * 3)
                            item2_col = (((item2_case - 1) - (square * 9)) % 3) + 1 + ((square % 3) * 3)
                            item2_posx = item2_col - 1
                            item2_posy = item2_line - 1

                            if item1_line == item2_line and not found_col_aligned:
                                found_line_aligned = True
                                found_aligned_line_index.append(item2_posx)

                            elif item1_col == item2_col and not found_line_aligned:
                                found_col_aligned = True
                                found_aligned_col_index.append(item2_posy)

                            else:
                                found_line_aligned = False
                                found_col_aligned = False
                                break


                    #Not found or not in the same line or col
                    if not found_line_aligned and not found_col_aligned:
                        print("\t\t\t Not aligned")
                        continue
                    else:
                        print("\t\t\t Aligned. Line / Col", found_line_aligned, found_col_aligned)

                    cleaning_required = False
                    
                    # Browse line in other square to clean
                    if found_line_aligned:
                        for line_index in range(0,9):
                            if line_index in found_aligned_line_index:
                                continue
                            if tested_value in self.possible_values_line[item1_line][line_index]:
                                cleaning_required = True
                                self.possible_values_line[item1_line][line_index].remove(tested_value)
                                print("\t\t ------------ Found LINE ! ------------")
                                print("\t\t Choice to remove:")
                                print("\t\t Value", tested_value)

                                # lelelele
                                squareoffset = 0
                                yoffset = 0

                                if item1_line > 6:
                                    squareoffset = 54
                                    yoffset = 6
                                elif item1_line > 3:
                                    squareoffset = 27
                                    yoffset = 3
                                
                                xoffset = (item1_line - 1  - yoffset) * 3
                                index_to_clean = 0
                                
                                if line_index > 5:
                                    index_to_clean = 18 + line_index - 5
                                elif line_index > 2:
                                    index_to_clean = 9 + line_index - 2
                                else:
                                    index_to_clean = line_index + 1
                                
                                xindex_to_clean = index_to_clean + xoffset + squareoffset
                                self.s5_clean_col_and_square(tested_value, item1_line, xindex)

                    # Browse col in other square to clean
                    if found_col_aligned:
                        for col_index in range(0,9):
                            if col_index in found_aligned_col_index:
                                continue
                            if tested_value in self.possible_values_col[item1_col][col_index]:
                                cleaning_required = True
                                self.possible_values_col[item1_col][col_index].remove(tested_value)
                                print("\t\t ------------ Found COL ! ------------")
                                print("\t\t Choice to remove:")
                                print("\t\t Value", tested_value)

                                # From colonne & col_index -> Get square / square index / line / line index
                                squareoffset = 0
                                yoffset = 0

                                if item1_col > 6:
                                    squareoffset = 6
                                    yoffset = 18
                                elif item1_col > 3:
                                    squareoffset = 3
                                    yoffset = 9
                                
                                index_to_clean = 0
                                offset_to_add = 0
                                
                                if col_index > 5:
                                    index_to_clean = col_index - 5
                                    offset_to_add = 54
                                elif col_index > 2:
                                    index_to_clean = col_index - 2
                                    offset_to_add = 27
                                else:
                                    index_to_clean = col_index + 1

                                xindex = ((index_to_clean - 1) * 3) + (item1_col - squareoffset) + yoffset + offset_to_add


                                self.s5_clean_line_and_square(tested_value, item1_col, xindex)

                    if cleaning_required:
                        return True

        return False

    def s5_clean_col_and_square(self, tested_value, line, xindex_to_clean):
        square_to_clean = int((xindex_to_clean - 1) / 9)
        col_to_clean = (((xindex_to_clean - 1) - (square_to_clean * 9)) % 3) + 1 + ((square_to_clean % 3) * 3)
        
        square_item_to_clean = xindex_to_clean - 1 - (square_to_clean * 9)
        col_item_to_clean = line - 1
        
        if tested_value in self.possible_values_col[col_to_clean][col_item_to_clean]:
            self.possible_values_col[col_to_clean][col_item_to_clean].remove(tested_value)
        
        if tested_value in self.possible_values_square[square_to_clean][square_item_to_clean]:
            self.possible_values_square[square_to_clean][square_item_to_clean].remove(tested_value)

    def s5_clean_line_and_square(self, tested_value, col, xindex_to_clean):
        square_to_clean = int((xindex_to_clean - 1) / 9)
        line_to_clean = int(((xindex_to_clean-(square_to_clean*9))-1)/3) + 1 + (int(square_to_clean/3) * 3)
        
        square_item_to_clean = xindex_to_clean - 1 - (square_to_clean * 9)
        line_item_to_clean = col - 1
        
        if tested_value in self.possible_values_line[line_to_clean][line_item_to_clean]:
            self.possible_values_line[line_to_clean][line_item_to_clean].remove(tested_value)
        
        if tested_value in self.possible_values_square[square_to_clean][square_item_to_clean]:
            self.possible_values_square[square_to_clean][square_item_to_clean].remove(tested_value)


    def clean_line_possible_values_for_ce_technique(self, square, absolute_line, value_to_check):
        deleted = 0
        # Clean the case of the square that are not in this line of this value
        for ite in range(0,9):
            case_to_clean = (square * 9) + ite
            line_to_clean = int(((case_to_clean - (square*9)))/3) + 1 + (int(square/3) * 3)
            col_to_clean = ((case_to_clean - (square * 9)) % 3) + 1 + ((square % 3) * 3)
            posx_to_clean = col_to_clean - 1
            posy_to_clean = line_to_clean - 1
            
            if absolute_line != line_to_clean:
                # clean
                if value_to_check in self.possible_values_square[square][ite]:
                    self.possible_values_square[square][ite].remove(value_to_check)
                    deleted += 1
                # clean
                if value_to_check in self.possible_values_line[line_to_clean][posx_to_clean]:
                    self.possible_values_line[line_to_clean][posx_to_clean].remove(value_to_check)
                    deleted += 1
                # clean
                if value_to_check in self.possible_values_col[col_to_clean][posy_to_clean]:
                    self.possible_values_col[col_to_clean][posy_to_clean].remove(value_to_check)
                    deleted += 1

        return deleted

    def clean_col_possible_values_for_ce_technique(self, square, absolute_col, value_to_check):
        deleted = 0
        # Clean the case of the square that are not in this line of this value
        for ite in range(0,9):
            case_to_clean = (square * 9) + ite
            line_to_clean = int(((case_to_clean - (square*9)))/3) + 1 + (int(square/3) * 3)
            col_to_clean = ((case_to_clean - (square * 9)) % 3) + 1 + ((square % 3) * 3)
            posx_to_clean = col_to_clean - 1
            posy_to_clean = line_to_clean - 1
            
            if absolute_col != col_to_clean:
                # clean
                if value_to_check in self.possible_values_square[square][ite]:
                    self.possible_values_square[square][ite].remove(value_to_check)
                    deleted += 1
                # clean
                if value_to_check in self.possible_values_line[line_to_clean][posx_to_clean]:
                    self.possible_values_line[line_to_clean][posx_to_clean].remove(value_to_check)
                    deleted += 1
                # clean
                if value_to_check in self.possible_values_col[col_to_clean][posy_to_clean]:
                    self.possible_values_col[col_to_clean][posy_to_clean].remove(value_to_check)
                    deleted += 1

        return deleted


root = Tk()

root.title('Sudoku')
root.geometry("400x300+500+300")

app = Application(master=root)
app.mainloop()
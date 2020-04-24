#!/usr/bin/python3
import time

current_milli_time = lambda: int(round(time.time() * 1000))
possible_values_square={}
possible_values_line={}
possible_values_col={}

key_line={}
key_col={}

entries_readed={}

entries={}
entries_hori=[]
entries_vert=[]


def solve_sudoku(values_readed):
    global possible_values_square
    global possible_values_line
    global possible_values_col

    global key_line
    global key_col
    global entries_readed

    global entries
    global entries_hori
    global entries_vert
    
    possible_values_square={}
    possible_values_line={}
    possible_values_col={}
    
    key_line={}
    key_col={}

    entries_readed={}

    entries={}
    entries_hori=[]
    entries_vert=[]

    for iti1 in range(1,10):
        entries_hori.append({})
        entries_vert.append({})
    
    read_sudoku_grid(values_readed)
    
    begin = current_milli_time()
    get_all_possible_values()
    
    values_readed = loop_apply_strategies(values_readed)
    end = current_milli_time()

    print("Duration : ", (end-begin))
    return values_readed

def read_sudoku_grid(values_readed):
    global entries
    global entries_hori
    global entries_vert
    
    entrycount = 1
    offsetx = 0
    offsety = 0


    for iti1 in range(1,10):
        
        posx = offsetx
        posy = offsety
        
        for iti2 in range(0,9):
            # Each 3 slot, return x to 0 and offset
            modulo=(posx % 3)
            if modulo != 3 and modulo == 0:
                posx = offsetx
                posy += 1
            
            # Create entries
            entry = values_readed[entrycount]

            # Pre-load sudoku
            if entry != 0:
                entries_readed[entrycount] = entry

            entries[entrycount] = entry
            entries_hori[(posy-1)][posx] = entry
            entries_vert[posx][(posy-1)] = entry
            
            # Increment
            entrycount += 1
            posx += 1

        # Increment position for next 9 blocs
        if (iti1 % 3) == 0:
            offsetx = 0
            offsety += 3
        else:
            offsetx += 3

def check_sudoku_rule(widgetvalue, posx, posy):
    global entries
    global entries_hori
    global entries_vert
    # calcul square
    posx +=1
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
        actual_value = entries.get(iti1)
        if actual_value != 0:
            square_dict[actual_value] = ""
    
    # check for square
    if widgetvalue in square_dict:
        return False
    
    # check for lines H
    h_lines_dict = {}
    h_lines_entries = entries_hori[(posy-1)]

    for iti1 in range(0,9):
        if (posx-1) == iti1:
            continue
        actual_value = h_lines_entries.get(iti1)
        if actual_value != 0:
            h_lines_dict[actual_value] = ""
    
    if widgetvalue in h_lines_dict:
        return False
    
    # check for lines V
    v_lines_dict = {}
    v_lines_entries = entries_vert[(posx-1)]

    for iti1 in range(0,9):
        if (posy-1) == iti1:
            continue
        actual_value = v_lines_entries.get(iti1)
        if actual_value != 0:
            v_lines_dict[actual_value] = ""
    
    if widgetvalue in v_lines_dict:
        return False

    return True

def get_all_possible_values():
    global entries_readed

    global entries
    global entries_hori
    global entries_vert

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
        
        for iti2 in range(0,9):
            # Each 3 slot, return x to 0 and offset
            modulo=((posx+1) % 3)
            
            if entrycount in entries_readed:
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
                    actual_value = entries.get(iti3)
                    if actual_value != 0:
                        square_dict.append(int(actual_value))
                
                # check for lines H
                h_lines_dict = []
                h_lines_entries = entries_hori[(posy)]

                for iti4 in range(0,9):
                    if (posx) == iti4:
                        continue
                    actual_value = h_lines_entries.get(iti4)
                    if actual_value != 0:
                        h_lines_dict.append(int(actual_value))
                
                # check for lines V
                v_lines_dict = []
                v_lines_entries = entries_vert[(posx)]

                for iti5 in range(0,9):
                    if (posy) == iti5:
                        continue
                    actual_value = v_lines_entries.get(iti5)
                    if actual_value != 0:
                        v_lines_dict.append(int(actual_value))
                
                if not ((tester in square_dict) or (tester in v_lines_dict) or (tester in h_lines_dict)):
                    possible_values[(entrycount-1)].append(tester)
            
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
        get_square_solution(possible_values, square)


    for line in range(1,10):
        get_line_solution(possible_values, line)


    for col in range(1,10):
        get_col_solution(possible_values, col)


def get_square_solution(possible_values, square):
    global possible_values_square

    sq_min = (square * 9)
    sq_max = (square * 9) + 9
    
    possible_values_square[square] = possible_values[sq_min:sq_max]

def get_line_solution(possible_values, line):
    global possible_values_line
    global key_line

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

    key_line[line] = hori_key
    possible_values_line[line] = hori_values

def get_col_solution(possible_values, col):
    global possible_values_col
    global key_col

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

    key_col[col] = vert_key
    possible_values_col[col] = vert_values

def update_possible_values_catalog(case, value):
    global possible_values_square
    global possible_values_line
    global possible_values_col
    
    # Update square
    square = int((case - 1) / 9)
    line = int(((case-(square*9))-1)/3) + 1 + (int(square/3) * 3)
    col = (((case - 1) - (square * 9)) % 3) + 1 + ((square % 3) * 3)
    
    square_item = case - 1 - (square * 9)
    line_item = col - 1
    col_item = line - 1

    # reset values to 0 for this case
    possible_values_square[square][square_item] = []
    possible_values_line[line][line_item] = []
    possible_values_col[col][col_item] = []
    
    for item in possible_values_square[square]:
        if value in item:
            item.remove(value)
    
    # Update line
    for index in range(0,9):
        if value in possible_values_line[line][index]:
            possible_values_line[line][index].remove(value)

    # Update colonne
    for index in range(0,9):
        if value in possible_values_col[col][index]:
            possible_values_col[col][index].remove(value)

def loop_apply_strategies(values_readed):
    global possible_values_square

    # Deduct solution
    full_count = 0

    remaining_size = 0

    while True:
        remaining_size = 0
        for square in range(0,9):
            for values in range(len(possible_values_square[square])):
                remaining_size += len(possible_values_square[square][values])
        # Loop
        mvt = iterate_all_strategies(values_readed)
        
        print("")
        print("\tMouvement: ", mvt)
        full_count += mvt

        if mvt == 0:
            break
    
    print("")
    print("END OF DEDUCT")
    print("")
    print("Mouvement: ", full_count)
    if remaining_size == 0:
        print("")
        print("\t SUCCESSFULLY SOLVED !")
    else:
        print("")
        print("\t CAN'T BE SOLVED !")
    
    print("")
    print("Recheck solution:")
    
    if recheck_all_results():
        print("Solution verified ! ")
        return values_readed
    else:
        print("Error with the solution when re-checking ! ")
        return None

def recheck_all_results():
    global entries

    entrycount = 1
    offsetx = 0
    offsety = 0

    # label = Label(text='Affichage')
    # label.grid(column=0, row=10)

    for iti1 in range(1,10):
        
        posx = offsetx
        posy = offsety
        
        for iti2 in range(0,9):
            # Each 3 slot, return x to 0 and offset
            modulo=(posx % 3)
            if modulo != 3 and modulo == 0:
                posx = offsetx
                posy += 1

            if not check_sudoku_rule(entries.get(entrycount), posx, posy):
                return False

            # Increment
            entrycount += 1
            posx += 1

        # Increment position for next 9 blocs
        if (iti1 % 3) == 0:
            offsetx = 0
            offsety += 3
        else:
            offsetx += 3

    return True
            

    
def iterate_all_strategies(values_readed):
    # S1 - Unique choice scan
    if strategie_1_unique_choice(values_readed):
        return 1
    # S2 - Hidden unique choice for line or col or square
    if strategie_2_hidden_unique_choice(values_readed):
        return 1
    # S3 - Exclusive number for square
    if strategie_3_exclusive_region():
        return 1
    # S4 - Exclusive pair for line or col or square
    if strategie_4_exclusive_pairs():
        return 1
    # S5 - Exclusive number of line or col
    if strategie_5_exclusive_number_in_line_or_col():
        return 1

    return 0

def strategie_1_unique_choice(values_readed):
    global possible_values_square
    global entries

    for square in range(0,9):
        square_values = possible_values_square[square]
        sq_min = (square * 9)
        sq_max = (square * 9) + 9

        for index1 in range(0,9):
            # Single result -> Set value and retry
            if len(square_values[index1]) == 1:
                value = square_values[index1][0]
                entrycount = sq_min + index1 + 1
                
                values_readed[entrycount] = value
                update_possible_values_catalog(entrycount, value)
                return True

    return False

def strategie_2_hidden_unique_choice(values_readed):
    global possible_values_square
    global possible_values_line
    global possible_values_col

    global entries

    for square in range(0,9):
        square_values = possible_values_square[square]
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

                value = square_unique_value.pop()
                
                values_readed[entrycount] = value
                update_possible_values_catalog(entrycount, value)

                return True

    for line in range(1,10):
        #retrieve values for the line
        hori_values = possible_values_line[line]
        hori_key = key_line[line]

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

                value = hori_unique_value.pop()
                
                values_readed[case_readed] = value
                update_possible_values_catalog(case_readed, value)

                return True

    for col in range(1,10):
        #retrieve values for the line
        vert_values = possible_values_col[col]
        vert_key = key_col[col]
        
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

                value = vert_unique_value.pop()
                
                values_readed[case_readed] = value
                update_possible_values_catalog(case_readed, value)

                return True

    return False

def strategie_3_exclusive_region():
    global possible_values_square
    global possible_values_line
    global possible_values_col

    global key_line
    global key_col


    for square in range(0,9):
        sq_min = (square * 9)

        # Search with exclu number tech
        for value_to_check in range(1,10):
            case_to_check = []
            for case in range(0,9):
                if value_to_check in possible_values_square[square][case]:
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

                for line_index in range(len(possible_values_line[absolute_line])):
                    # Check if already present in other case in other square
                    # Calcul
                    line_values_to_check = possible_values_line[absolute_line][line_index]
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
                    if clean_line_possible_values_for_ce_technique(square, absolute_line, value_to_check) > 0:
                        return True

                for col_index in range(len(possible_values_col[absolute_col])):
                    # Check if already present in other case in other square
                    # Calcul
                    col_values_to_check = possible_values_col[absolute_col][col_index]
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
                    if clean_col_possible_values_for_ce_technique(square, absolute_col, value_to_check) > 0:
                        return True

    return False

def strategie_4_exclusive_pairs():
    global possible_values_square
    global possible_values_line
    global possible_values_col
    
    # Exclusive pairs
    # Search in square

    for square in range(0,9):
        exclusive_pairs = {}
        for index1 in range(0,9):
            if len(possible_values_square[square][index1]) == 2:
                exclusive_pairs[index1] = possible_values_square[square][index1]
        
        if len(exclusive_pairs) > 0:
            for key1 in exclusive_pairs.keys():
                for key2 in exclusive_pairs.keys():
                    if key2 == key1:
                        continue

                    if exclusive_pairs[key1] == exclusive_pairs[key2]:
                        cleaning_required = False

                        # Search in this square if other case has those numbers -> If yes: clean and mvt + 1
                        for value in exclusive_pairs[key1]:
                            for index_to_clean in range(0,9):
                                if index_to_clean == key1 or index_to_clean == key2:
                                    continue
                                if value in possible_values_square[square][index_to_clean]:
                                    # Clean
                                    possible_values_square[square][index_to_clean].remove(value)

                                    case_to_clean = index_to_clean + 1 + (square * 9)
                                    line_to_clean = int(((case_to_clean-(square*9))-1)/3) + 1 + (int(square/3) * 3)
                                    col_to_clean = (((case_to_clean - 1) - (square * 9)) % 3) + 1 + ((square % 3) * 3)
                                    
                                    line_item = col_to_clean - 1
                                    col_item = line_to_clean - 1
                                    possible_values_line[line_to_clean][line_item].remove(value)
                                    possible_values_col[col_to_clean][col_item].remove(value)
                                    cleaning_required = True

                        if cleaning_required:
                            return True


    return False

def strategie_5_exclusive_number_in_line_or_col():
    global possible_values_square
    global possible_values_line
    global possible_values_col


    for square in range(0,9):
        for index1 in range(0,9):
            item1_case = index1 + 1 + (square * 9)
            item1_line = int(((item1_case-(square*9))-1)/3) + 1 + (int(square/3) * 3)
            item1_col = (((item1_case - 1) - (square * 9)) % 3) + 1 + ((square % 3) * 3)
            item1_posx = item1_col - 1
            item1_posy = item1_line - 1
            
            for tested_value in range(1,10):
                if tested_value not in possible_values_square[square][index1]:
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
                    if tested_value in possible_values_square[square][index2]:
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
                    continue

                cleaning_required = False
                
                # Browse line in other square to clean
                if found_line_aligned:
                    for line_index in range(0,9):
                        if line_index in found_aligned_line_index:
                            continue
                        if tested_value in possible_values_line[item1_line][line_index]:
                            cleaning_required = True
                            possible_values_line[item1_line][line_index].remove(tested_value)

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
                            s5_clean_col_and_square(tested_value, item1_line, xindex_to_clean)

                # Browse col in other square to clean
                if found_col_aligned:
                    for col_index in range(0,9):
                        if col_index in found_aligned_col_index:
                            continue
                        if tested_value in possible_values_col[item1_col][col_index]:
                            cleaning_required = True
                            possible_values_col[item1_col][col_index].remove(tested_value)

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


                            s5_clean_line_and_square(tested_value, item1_col, xindex)

                if cleaning_required:
                    return True

    return False

def s5_clean_col_and_square(tested_value, line, xindex_to_clean):
    global possible_values_square
    global possible_values_col

    square_to_clean = int((xindex_to_clean - 1) / 9)
    col_to_clean = (((xindex_to_clean - 1) - (square_to_clean * 9)) % 3) + 1 + ((square_to_clean % 3) * 3)
    
    square_item_to_clean = xindex_to_clean - 1 - (square_to_clean * 9)
    col_item_to_clean = line - 1
    
    if tested_value in possible_values_col[col_to_clean][col_item_to_clean]:
        possible_values_col[col_to_clean][col_item_to_clean].remove(tested_value)
    
    if tested_value in possible_values_square[square_to_clean][square_item_to_clean]:
        possible_values_square[square_to_clean][square_item_to_clean].remove(tested_value)

def s5_clean_line_and_square(tested_value, col, xindex_to_clean):
    global possible_values_square
    global possible_values_line

    square_to_clean = int((xindex_to_clean - 1) / 9)
    line_to_clean = int(((xindex_to_clean-(square_to_clean*9))-1)/3) + 1 + (int(square_to_clean/3) * 3)
    
    square_item_to_clean = xindex_to_clean - 1 - (square_to_clean * 9)
    line_item_to_clean = col - 1
    
    if tested_value in possible_values_line[line_to_clean][line_item_to_clean]:
        possible_values_line[line_to_clean][line_item_to_clean].remove(tested_value)
    
    if tested_value in possible_values_square[square_to_clean][square_item_to_clean]:
        possible_values_square[square_to_clean][square_item_to_clean].remove(tested_value)


def clean_line_possible_values_for_ce_technique(square, absolute_line, value_to_check):
    global possible_values_square
    global possible_values_line
    global possible_values_col

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
            if value_to_check in possible_values_square[square][ite]:
                possible_values_square[square][ite].remove(value_to_check)
                deleted += 1
            # clean
            if value_to_check in possible_values_line[line_to_clean][posx_to_clean]:
                possible_values_line[line_to_clean][posx_to_clean].remove(value_to_check)
                deleted += 1
            # clean
            if value_to_check in possible_values_col[col_to_clean][posy_to_clean]:
                possible_values_col[col_to_clean][posy_to_clean].remove(value_to_check)
                deleted += 1

    return deleted

def clean_col_possible_values_for_ce_technique(square, absolute_col, value_to_check):
    global possible_values_square
    global possible_values_line
    global possible_values_col

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
            if value_to_check in possible_values_square[square][ite]:
                possible_values_square[square][ite].remove(value_to_check)
                deleted += 1
            # clean
            if value_to_check in possible_values_line[line_to_clean][posx_to_clean]:
                possible_values_line[line_to_clean][posx_to_clean].remove(value_to_check)
                deleted += 1
            # clean
            if value_to_check in possible_values_col[col_to_clean][posy_to_clean]:
                possible_values_col[col_to_clean][posy_to_clean].remove(value_to_check)
                deleted += 1

    return deleted

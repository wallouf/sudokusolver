#!/usr/bin/python3

import sudoku



dict_values_readed = dict()

for case in range(1,82):
    dict_values_readed[case] = 0


dict_values_readed[6] = 7
dict_values_readed[7] = 8
dict_values_readed[9] = 5

dict_values_readed[13] = 1
dict_values_readed[14] = 4
dict_values_readed[15] = 9

dict_values_readed[22] = 3
dict_values_readed[25] = 9
dict_values_readed[27] = 6

dict_values_readed[29] = 1

dict_values_readed[37] = 6
dict_values_readed[38] = 8
dict_values_readed[39] = 4
dict_values_readed[44] = 3

dict_values_readed[47] = 7

dict_values_readed[55] = 9
dict_values_readed[59] = 6

dict_values_readed[70] = 9
dict_values_readed[71] = 2
dict_values_readed[72] = 5

dict_values_readed[75] = 4
dict_values_readed[77] = 8


print(dict_values_readed)
dict_values_readed = sudoku.solve_sudoku(dict_values_readed)
print(dict_values_readed)
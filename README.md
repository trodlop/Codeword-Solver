# Codeword-Solver
A Python program that lets you input a codeword as a matrix, and then solves that codeword using a english language dictionary .csv file

Use data.py to input the board matrix and the provided key for the puzzle, tyhen just run solver.py and watch as it solves the puzzle. 

NOTE: There is a major problem with that dictionary file that is provided, where conjugated words are not included in the dictionary and hence the program will not recognize them. For example, run is a "valid" word as it appears in the dictionary, but runs, running, ran, etc. are "not valid" as they do not appear in the dictionary.

import numpy as np
import data

board_rotated = np.rot90(data.board)

global words
words = {}

global n
n = 0
global count
count = 0

# print(np.array(data.board))
# print("------------------------------------------------")
# print(np.array(board_rotated))

def horizontal_words():
    global n
    global num_list
    global words
    global count
    
    for i in range(len(data.board)):  # Loop through rows of the board
        row = data.board[i]
        num_list = []
        
        for j in range(len(row)):  # Loop through elements in the row
            square = row[j]
            
            if square != 0:
                num_list.append(square)  # Append non-zero squares to num_list
                count += 1
            else:
                if count >= 3:  # Check if we have a word
                    n += 1  # Increment word identifier
                    words[f'word {n}'] = []
                    words[f'word {n}'].append(num_list)  # Store the word in dictionary
                num_list = []  # Reset num_list
                count = 0  # Reset count
    
        # Check at the end of the row
        if count >= 3:
            n += 1
            words[f'word {n}'] = []
            words[f'word {n}'].append(num_list)
        num_list = []  # Reset for next row
        count = 0

def vertical_words():
    global n
    global num_list
    global words
    global count
    
    for i in range(len(board_rotated)):  # Loop through rows of the board
        row = board_rotated[i]
        num_list = []
        
        for j in range(len(row)):  # Loop through elements in the row
            square = row[j]
            
            if square != 0:
                num_list.append(square)  # Append non-zero squares to num_list
                count += 1
            else:
                if count >= 3:  # Check if we have a word
                    n += 1  # Increment word identifier
                    words[f'word {n}'] = []
                    words[f'word {n}'].append(num_list)  # Store the word in dictionary
                num_list = []  # Reset num_list
                count = 0  # Reset count
    
        # Check at the end of the row
        if count >= 3:
            n += 1
            words[f'word {n}'] = []
            words[f'word {n}'].append(num_list)
        num_list = []  # Reset for next row
        count = 0

if __name__ == "__main__"  :
    horizontal_words()
    vertical_words()

    for key, value in words.items():
        print(f"{key}: {value}")
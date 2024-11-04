import numpy as np
import csv

global dictionary
dictionary = []

with open("D:\coding\python\interview resources\codeword solver\OPTED-Dictionary.csv", mode='r', newline='') as file:
        csv_reader = csv.reader(file)
        
        for row in csv_reader:
            # Loop through each row in the CSV file
            
            if row:
                # Ensure the row is not empty

                dictionary.append(row[0])
                # Add the first column value to the list

# print(np.array(dictionary))
# print(len(dictionary))

global possible_words_1
possible_words_1 = []
global possible_words_2
possible_words_2 = []

# target = "...b.r"

def search_word_length(n):
     
    for i in range(len(dictionary)):

        # print(dictionary[i])

        if len(dictionary[i]) == n:
            
            possible_words_1.append(dictionary[i])

    return possible_words_1
        
def search_substring(target):
    possible_words_1 = search_word_length(len(target))
    # returns a list of words matching target word length

    possible_words_2 = []

    for i in range(len(possible_words_1)):
        # loops through list of n letter words

        selected_word = possible_words_1[i].lower()

        # Ensure the selected word is the same length as the target
        if len(selected_word) != len(target):
            continue

        possible = True

        for j in range(len(target)):
            # loops through each letter of the word

            if target[j] == "." or target[j] == selected_word[j]:
                continue
            else:
                possible = False
                break

        if possible:
            possible_words_2.append(selected_word)

    possible_words = set(possible_words_2)
    return list(possible_words)
            
if __name__ == "__main__":

    print(f'{search_substring("......")}')
    print(f'number of possible words = {len(search_substring("......"))}')
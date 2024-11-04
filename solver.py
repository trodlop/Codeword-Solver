import numpy as np
import data
import identify_words
import check_possible_words

import time

global solved
solved = False

global word_counter
word_counter = 1
global count
count = 0
global selected_word

global possible_words 
possible_words = {}
global subbed_letters
subbed_letters = {}

def substitute_letters_all():

    for i in range(len(identify_words.words)):

        word_list = identify_words.words[f'word {i + 1}']

        substitution = list(word_list[0]) 

        for j in range(len(substitution)):

            if data.key[f'{substitution[j]}'] != "":

                substitution[j] = data.key[f'{substitution[j]}']

            else:

                substitution[j] = "."

        identify_words.words[f'word {i + 1}'].append(substitution)

    # for key, value in identify_words.words.items():
    #     print(f"{key}: {value}")

def increment_word():
    global word_counter
    word_counter = word_counter + 1

def decrease_word():
    global word_counter
    word_counter = word_counter - 1

def select_word():
    global word_counter
    global selected_word
    global num_list
    global sub_list

    selected_word = identify_words.words[f'word {word_counter}']

    sub_list = selected_word[0][:]
    num_list = selected_word[0][:]

def substitute_letters_single():
    global word_counter
    global selected_word
    global num_list
    global sub_list
    
    for i in range(len(sub_list)):

        if data.key[f'{sub_list[i]}'] != "":

            sub_list[i] = data.key[f'{sub_list[i]}']

        else:

            sub_list[i] = "."

    if len(identify_words.words[f'word {word_counter}']) < 2:

        identify_words.words[f'word {word_counter}'].append(sub_list)

    elif len(identify_words.words[f'word {word_counter}']) == 2:

        temp_list = identify_words.words[f'word {word_counter}'][:]
        temp_list[1] = sub_list[:]
        identify_words.words[f'word {word_counter}'] = temp_list[:]

    # TODO      Instead of appending sub_list to the end of the word, replace the previous sub_list entry 

def search():
    global word_counter
    global selected_word
    global num_list
    global sub_list
    global target
    global possible_words

    target = ''.join(sub_list)

    #? print(f'\ntarget = {target}\n')

    stage_1_check = check_possible_words.search_substring(target)
    stage_2_check = []

    temp_key = {}

    for i in range(len(num_list)):

        temp_key[f'{num_list[i]}'] = sub_list[i]

    for i in range(len(stage_1_check)):

        checking = stage_1_check[i]

        possible = True
        count = 0

        for j in range (len(checking)):

            # temp_key[f'{num_list[j]}'] gives the letter stored in the temporary key at this iteration, eg. 'work' when j = 1

            if temp_key[f'{num_list[j]}'] == ".":

                if checking[j] in temp_key.values(): # Checks whether 

                    possible = False
                    break

                else:

                    temp_key[f'{num_list[j]}'] = checking[j]

                    count += 1

            elif temp_key[f'{num_list[j]}'] == checking[j]:

                count += 1
                
            else:

                possible = False
                break

        if possible == True and count == len(checking):

            stage_2_check.append(checking)

        for j in range(len(num_list)):

            temp_key[f'{num_list[j]}'] = sub_list[j]

    possible_words[f'layer {word_counter}'] = stage_2_check[:]

    # print(stage_2_check)
    # print(f'number of possibilities = {len(stage_2_check)}')

    #? print(possible_words)
    #? print(len(possible_words[f'layer {word_counter}']))

def update_key():
    global subbed_letters
    global word_counter

    list = subbed_letters[f'layer {word_counter}'][:]

    word = list[2][:]
    letters = list[1][:]
    numbers = list[0][:]

    to_remove_l = []
    to_remove_n = []

    letters_in_key = {value for value in data.key.values() if value != ""}

    for i in range(len(letters)):

        if data.key[f'{numbers[i]}'] == "":

            if letters[i] not in letters_in_key:
                data.key[f'{numbers[i]}'] = letters[i]
            else:
                to_remove_l.append(letters[i])
                to_remove_n.append(numbers[i])

        else:

            to_remove_l.append(letters[i])
            to_remove_n.append(numbers[i])  

    for letter in to_remove_l:
        letters.remove(letter)
    for number in to_remove_n:
        numbers.remove(number)   

    subbed_letters[f'layer {word_counter}'] = [numbers,letters,word]

    # print(subbed_letters)

    # for key, value in data.key.items():
    #     print(f"{key}: {value}")

    # print(letters)
    # print(numbers)

def revert_key():

    global subbed_letters
    global word_counter

    if f'layer {word_counter}' not in subbed_letters:
        print(f"No layer found for word_counter {word_counter}.")
        return

    # Get the current layer's state
    list = subbed_letters[f'layer {word_counter}'][:]

    # Get the letters, numbers, and word
    word = list[2][:]
    letters = list[1][:]
    numbers = list[0][:]
    
    # Lists to restore to original state
    to_restore_l = []
    to_restore_n = []

    # Check each letter to see if it was substituted
    for i in range(len(letters)):
        if data.key[f'{numbers[i]}'] == letters[i]:
            data.key[f'{numbers[i]}'] = ""
        else:
            to_restore_l.append(letters[i])
            to_restore_n.append(numbers[i])
    
    # Restore the original letters and numbers to the subbed_letters layer
    for letter in to_restore_l:
        letters.remove(letter)
    for number in to_restore_n:
        numbers.remove(number)
    
    subbed_letters[f'layer {word_counter}'] = [numbers, letters, word]

def main_loop():
    global solved
    global possible_words
    global subbed_letters
    global first_word_list
    global first_word
    global count

    identify_words.horizontal_words()
    identify_words.vertical_words()

    #? for key, value in identify_words.words.items():
    #?     print(f"{key}: {value}")

    print("")

    # Begins by searching all possible words for the first word 
    select_word()
    substitute_letters_single()
    search()

    while word_counter <= len(identify_words.words):
        
        if len(possible_words[f'layer {word_counter}']) > 0:

            # print("\nmove on to next word")
            #? print(f'selected word = {word_counter}       {selected_word}\n')

            first_word_list = possible_words[f'layer {word_counter}'][:]
            first_word = first_word_list[0][:]

            nums = identify_words.words[f'word {word_counter}'][:]
            subbed_letters[f'layer {word_counter}'] = [nums[0],list(first_word),first_word]

            #? for key, value in data.key.items():
            #?      print(f"{key}: {value}")

            #? print(f'\nletters to substitute = {subbed_letters}\n')
            update_key()

            #? for key, value in data.key.items():
            #?      print(f"{key}: {value}")

            increment_word()

            select_word()

            #? print(f'\nselected word = {word_counter}       {selected_word}\n')
            
            substitute_letters_single()

            #? print("")

            #? for key, value in identify_words.words.items():
            #?     print(f"{key}: {value}")

            search()

        elif len(possible_words[f'layer {word_counter}']) == 0:

            decrease_word()
            select_word()

            #? print(f'\nselected word = {word_counter}       {selected_word}\n')

            revert_key()

            list_to_remove = possible_words[f'layer {word_counter}'][:]
            list_to_remove.pop(0)

            possible_words[f'layer {word_counter}'] = list_to_remove[:]

            #? print("")

            #? for key, value in data.key.items():
            #?      print(f"{key}: {value}")

        else:
            
            print("\n\nerror in backtracking algorithm\n\n")

            break

        time.sleep(0.1)

        for key, value in possible_words.items():
            # print("")
            print(f"\n{key}: {value}")
            print(len(value))

        print("\n")

        count += 1
        print(f'Checked {count} words       Checking word - {word_counter}, {target}')

        # print(f'\rChecked {count} words       Checking word - {word_counter}', end='')

        # break

    print("solved")
    for key, value in data.key.items():
        print(f"{key}: {value}")


#TODO           PSEUDOCODE:

#TODO           update main key using the first word from stage_2_check
#TODO           store the letters which were updated 
#TODO           substitute new letters into second word
#TODO           if no possibilities -> remove updated letters from the key, remove word from stage_2_check, update main key using next word from stage_2_check

if __name__ == "__main__"  :

    main_loop()


#!  NOTE: "ctrl + c" will stop the runtime without killing the terminal
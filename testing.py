import numpy as np
import data
import identify_words
import check_possible_words
import time

solved = False
word_counter = 1
count = 0
selected_word = None
possible_words = {}
subbed_letters = {}

def substitute_letters_all():
    for i, word_list in identify_words.words.items():
        substitution = list(word_list[0])
        for j in range(len(substitution)):
            substitution[j] = data.key.get(substitution[j], ".")
        word_list.append(substitution)
    print("Substitute letters for all words done.")

def increment_word():
    global word_counter
    word_counter += 1

def decrease_word():
    global word_counter
    word_counter -= 1

def select_word():
    global word_counter, selected_word, num_list, sub_list

    if f'word {word_counter}' not in identify_words.words:
        print(f"KeyError: 'word {word_counter}' not found in identify_words.words.")
        return False
    
    selected_word = identify_words.words[f'word {word_counter}']
    sub_list = selected_word[0][:]
    num_list = selected_word[0][:]
    print(f"Selected word {word_counter}: {selected_word}")
    return True

def substitute_letters_single():
    global word_counter, selected_word, num_list, sub_list
    sub_list = [data.key.get(char, ".") for char in sub_list]
    identify_words.words[f'word {word_counter}'] = [num_list, sub_list]
    print(f"Substituted letters for word {word_counter}: {identify_words.words[f'word {word_counter}']}")

def search():
    global word_counter, selected_word, num_list, sub_list, possible_words
    target = ''.join(sub_list)
    stage_1_check = check_possible_words.search_substring(target)
    stage_2_check = []
    temp_key = {num: sub for num, sub in zip(num_list, sub_list)}

    for checking in stage_1_check:
        possible = True
        count = 0
        temp_key_copy = temp_key.copy()

        for j, char in enumerate(checking):
            if temp_key_copy[num_list[j]] == ".":
                if char in temp_key_copy.values():
                    possible = False
                    break
                temp_key_copy[num_list[j]] = char
                count += 1
            elif temp_key_copy[num_list[j]] == char:
                count += 1
            else:
                possible = False
                break

        if possible and count == len(checking):
            stage_2_check.append(checking)

    possible_words[f'layer {word_counter}'] = stage_2_check
    print(f"Search for word {word_counter} produced {len(stage_2_check)} possibilities.")

def update_key():
    global subbed_letters, word_counter
    list = subbed_letters[f'layer {word_counter}']
    word, letters, numbers = list[2], list[1], list[0]
    letters_in_key = set(data.key.values())
    to_remove = []

    for num, char in zip(numbers, letters):
        if data.key.get(num) is None:
            print(f"KeyError: {num} not found in data.key")
            continue

        if data.key[num] == "":
            if char not in letters_in_key:
                data.key[num] = char
            else:
                to_remove.append((char, num))
        else:
            to_remove.append((char, num))

    for char, num in to_remove:
        letters.remove(char)
        numbers.remove(num)

    subbed_letters[f'layer {word_counter}'] = [numbers, letters, word]
    print(f"Updated key for word {word_counter}: {data.key}")

def revert_key():
    global subbed_letters, word_counter

    if f'layer {word_counter}' not in subbed_letters:
        print(f"No layer found for word_counter {word_counter}.")
        return

    list = subbed_letters[f'layer {word_counter}']
    word, letters, numbers = list[2], list[1], list[0]
    to_restore = []

    for num, char in zip(numbers, letters):
        if data.key.get(num) is None:
            print(f"KeyError: {num} not found in data.key")
            continue

        if data.key[num] == char:
            data.key[num] = ""
        else:
            to_restore.append((char, num))

    for char, num in to_restore:
        letters.remove(char)
        numbers.remove(num)

    subbed_letters[f'layer {word_counter}'] = [numbers, letters, word]
    print(f"Reverted key for word {word_counter}: {data.key}")

def main_loop():
    global solved, possible_words, subbed_letters, first_word_list, first_word, count
    identify_words.horizontal_words()
    identify_words.vertical_words()

    if not select_word():
        return

    substitute_letters_single()
    search()

    while word_counter <= len(identify_words.words):
        if possible_words.get(f'layer {word_counter}'):
            first_word_list = possible_words[f'layer {word_counter}']
            if not first_word_list:
                decrease_word()
                continue

            first_word = first_word_list.pop(0)

            nums = identify_words.words[f'word {word_counter}'][0]
            subbed_letters[f'layer {word_counter}'] = [nums, list(first_word), first_word]
            update_key()
            increment_word()

            if not select_word():
                break

            substitute_letters_single()
            search()
        else:
            decrease_word()

            if not select_word():
                break

            revert_key()
            possible_words[f'layer {word_counter}'] = possible_words.get(f'layer {word_counter}', [])[1:]

        count += 1
        print(f'\rChecked {count} words       Checking word - {word_counter}', end='')

    print("\nsolved")
    for key, value in data.key.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main_loop()
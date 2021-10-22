# reads all text files in directory and makes separate frequency analysis for each one,
# and finally merging the analysis results to one

# import glob                 # to do mass-readings
# paths = glob.glob("*.txt")  # if txt files are found in same folder as python file
from fa_db_functionality import make_fa_dict_from_db, make_all_fa_dicts_from_db

all_frequencies = {}
global num_of_files
global total_letters_read
num_of_files = 0
total_letters_read = 0

# key = location in alphabet, value = letter. letters in order. Add other symbols for use in more langugages.
letters_num = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F", 7: "G", 8: "H", 9: "I", 10: "J", 11: "K",
               12: "L", 13: "M", 14: "N", 15: "O", 16: "P", 17: "Q", 18: "R", 19: "S", 20: "T", 21: "U", 22: "V",
               23: "W", 24: "X", 25: "Y", 26: "Z", 27: "Å", 28: "Ä", 29: "Ö"}

# Values will be summed here for resulting frequency of all files combined for each letter
combined = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "G": 0, "H": 0, "I": 0, "J": 0, "K": 0,
            "L": 0, "M": 0, "N": 0, "O": 0, "P": 0, "Q": 0, "R": 0, "S": 0, "T": 0, "U": 0, "V": 0,
            "W": 0, "X": 0, "Y": 0, "Z": 0, "Å": 0, "Ä": 0, "Ö": 0}

def make_fa_dict_from_text(text):
    """create and return frequency analysis dictionary from given text"""
    fa_dict = {}
    for letter in text:
        if letter.isalpha() and letter.lower() not in fa_dict.keys(): 
            fa_dict[letter.lower()] = 1
        elif letter.lower() in fa_dict.keys():
            fa_dict[letter.lower()] += 1
    no_of_letters = sum(fa_dict.values())
    for letter, count in fa_dict.items():
        fa_dict[letter] = count / no_of_letters * 100
    return fa_dict


def analyze_all_files(paths):
    """ for all paths in directory, open that file and read its contents"""
    global num_of_files
    global total_letters_read
    for path in paths:
        f = open(path, encoding="utf-8")

        text = f.read()

        # Frequency found in that particular file
        letter_frequencies = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "G": 0, "H": 0, "I": 0, "J": 0, "K": 0,
                              "L": 0, "M": 0, "N": 0, "O": 0, "P": 0, "Q": 0, "R": 0, "S": 0, "T": 0, "U": 0, "V": 0,
                              "W": 0, "X": 0, "Y": 0, "Z": 0, "Å": 0, "Ä": 0, "Ö": 0}

        for letter in text:
            if not letter == " ":
                if letter.isalpha():
                    total_letters_read += 1
            if letter.upper() in letter_frequencies.keys():  # if letter among supported letters, increase frequency
                letter_frequencies[letter.upper()] = letter_frequencies[letter.upper()] + 1

        num_of_files += 1  # increase value of number of files
        all_frequencies[num_of_files] = letter_frequencies
        print(path + ": ", letter_frequencies)


def combine_files():
    global num_of_files
    # combine files
    for i in range(1, len(letters_num)):
        for j in range(1, num_of_files + 1):  # add values to all letters in alphabet for all files
            combined[letters_num[i]] += all_frequencies[j][letters_num[i]]

    print("\nTotal:")
    print("Combined sum of occurences of letter:", combined)
    for k, _ in combined.items():  # divide value by total numbers of letters read
        try:
            combined[k] = round((combined[k] / total_letters_read) * 100, 2)
        except ZeroDivisionError:
            combined[k] = 0

    print("Combined: (frequency percentage of total)", combined)

# module with functions for detection of language via frequency analysis



def make_ordered_tuple(fa_dict):
    """Takes a fa-dict as argument and returns a tuple that is sorted
    from most frequently used letter to the least used letter. Want a tuple
    to preserve order and content (immutable). """
    fa_list = [(letter, freq) for letter, freq in fa_dict.items()]  # create list with letter-and-frequency pairs
    ordered_list_w_freq = sorted(fa_list, key=lambda x: x[1], reverse=True) # Sort the list with the frequency-value as key
    ordered_list_of_letters = [letter for letter, _ in ordered_list_w_freq] # make list of only letters, still sorted
    # for letter, _ in ordered_list_w_freq:
    #     ordered_list_of_letters.append(letter)
    return tuple(ordered_list_of_letters)   # convert list to tuple and return it


def compare_tuples(tuple1, tuple2):
    """Takes 2 tuples as arguments and returns the total number of matches in
    the top 6 letters and the bottom 6 letters of each tuple combined """
    no_of_matches = 0
    for letter in tuple1[:6]:   # increment no_of_matches for each match in first 6 letters of each tuple
        if letter in tuple2[:6]:
            no_of_matches += 1
            # print(letter)
    for letter in tuple1[-6:]:  # increment no_of_matches for each match in the last 6 letters of each tuple
        if letter in tuple2[-6:]:
            no_of_matches += 1
            # print(letter)
    return no_of_matches

def detect_language_w_fa(fa_dict_to_detect, dict_w_all_fa):
    """ takes one fa-dict for a language we want to detect, and another dict with all known fa as arguments,
        returns a list of tuples with the top matching language(s) [(language, score)]"""
    match_score_dict = {}
    tuple_to_detect = make_ordered_tuple(fa_dict_to_detect) # make an ordered tuple out of the dict to detect language for
    for lang, fa in dict_w_all_fa.items():  # iterate through the items in the dict that contains known analyses
        # make an ordered tuple from the fa to compare to and compare it to the tuple_to_detect, then
        # add the matching score to the dict match_score_dict with the language as key
        tuple_to_match = make_ordered_tuple(fa) 
        match_score_dict[lang] = compare_tuples(tuple_to_detect, tuple_to_match)    
    # create a sorted list from the matching score dictionary
    sorted_list = sorted([(lang, score) for lang, score in match_score_dict.items()], key=lambda x: x[1], reverse=True)
    if len(sorted_list) != 0:   # check that the list is not empty
        top_matches = [sorted_list[0]]  # initiate list with top match, other matches will be appended
    else:   # if list is empty, report in terminal and return from function
        print("Something went wrong, there are no elements in matching-languages-list. Check database.")
        return
    # check if there are more languages with same score and append them to list with top matching languages
    for lang, score in sorted_list[1:]:
        if score == top_matches[0][1]:
            top_matches.append((lang, score))
    return top_matches


def return_detected_lang(text):
    """Takes a text as argument and returns the detected language name,
    it will also return a list of all languages with same score"""
    text_fa = make_fa_dict_from_text(text)  # make fa-dict from text
    dict_w_all_fa = make_all_fa_dicts_from_db() # make a dict with all known fa that are in database
    score_list = detect_language_w_fa(text_fa, dict_w_all_fa) # get matching scores for text compared to all languages in database
    if len(score_list) == 1: # If there is only one entry in list, report following:
        print("The language is detected as", score_list[0][0], "with a matching score of",
              score_list[0][1])
        return score_list, score_list[0][0]
    else: # if there are more than one language with same matching score, report following:
        print("The language is detected as one of the following, all with a matching score of",
              score_list[0][1])
        for lang, _ in score_list:
            print(lang)
        return score_list, score_list[0][0]



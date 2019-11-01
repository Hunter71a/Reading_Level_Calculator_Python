#  Carl Olson   2019.10.08
#  CSCI-1511    Python
#  Lab 7: WordFrequency Enhanced With Reading Level Calculation of the text

# This program practices file i/o, error handling, and functions
# Receives a .txt file as input, processes the text eliminating punctuation
# and eventually sorting the words into a dictionary listing the number of occurrences
# for each word. The text is further analyzed for reading level using the Flesh-Kincaid
# grade level formula.

import sys


def ask_yes_or_no(question):
    """Ask a yes or no question"""
    answer = None
    while answer not in ('y', 'n'):
        answer = input(question).lower()
    return answer


def end_program():
    """End Program
    :return: none, program terminates
    """
    input("Press enter to exit")
    sys.exit()


def open_file(file_name, mode):
    """
      Open a text file with exception handling
    :param file_name: hardcoded to trivia.txt
    :param mode: read-only
    :return: file object
    """
    the_file = "not_found"
    try:
        the_file = open(file_name, mode)
    except IOError as e:
        print("Unable to open file:", file_name)
        try_again = ask_yes_or_no("Would you like to open a different text file? (y/n)")
        if try_again == "y":
            return the_file
        else:
            end_program()
    return the_file


def reading_level(input, total_words_processed, words):
    """   Estimate the reading level of text using the Flesch-Kincaid formula
    :param input:
    :param total_words_processed:
    :param words:
    :return: appropriate grade level of reading material
    """
    sentences = 0
    syllables = 0
    vowels = ('a', 'e', 'i', 'o', 'u')
    sentence_punctuation = ('.', '!', '?')
    for letter in input:
        if letter in sentence_punctuation:
            sentences += 1

    for word in words:
        sils = 0
        last_letter = "consonant"
        for letter in word:
            if letter in vowels and last_letter == "vowel":
                last_letter = "vowel"
            if letter in vowels and last_letter == "consonant":
                last_letter = "vowel"
                sils += 1
            if letter not in vowels and last_letter == "vowel":
                last_letter = "consonant"
                sils += 1
            if letter not in vowels and last_letter == "consonant":
                last_letter = "consonant"
        syllables += sils / 2  # fudge factor method to eliminate issues cause with words starting with either consonants or vowels

    average_syllables_per_word = syllables / total_words_processed
    average_words_per_sentence = total_words_processed / sentences

    reading_score = (0.39 * (average_words_per_sentence)) + (11.8 * (average_syllables_per_word)) - 15.59
    return reading_score


def process_file(file_to_process):
    """process and break text into words and count the number of occurrences of each word """
    count = 0
    word_count = {}
    print("\nFile Details: ", file_to_process, "\n")
    input = file_to_process.read()
    lines = input.lower()
    punctuation = ('!', '.', ',', '?', '-', '<', '>', '/', '^', '&', '%', '$', '\"', '\n', '—')
    for mark in punctuation:
        lines = lines.replace(mark, " ")
    words = lines.split()
    total_words_processed = len(words)

    for word in words:
        if word in word_count:
            word_count[word] = word_count[word] + 1
        else:
            word_count[word] = 1
        count += 1
    sorted_keys = sorted(word_count)
    number_unique_words = len(sorted_keys)
    reading_score = reading_level(input, total_words_processed, words)
    print("Word \t\t\t\tCount")
    for key in sorted_keys:
        print("{0:15} :      {1}".format(key, word_count[key]))
    print("\nTotal words processed:", total_words_processed)
    print("Total number of unique words:", number_unique_words)
    print("The estimated reading level is grade {:4.1f}".format(reading_score))
    print()


def which_file():
    file_name = input("What file do you want to process? ")
    return file_name


def main():
    print("\n\t\t\t\t\tWelcome to the Text Analyzer XL2000")
    print("""\n
If you enter a text file, the number of times each individual word is used will be counted.
Addition capabilities to estimate reading level have been added, and two text files have been
included to demonstrate the awesomeness! The file "spongebob.txt" is a transcript of Spongebob talking,
and the file "address.txt" is the "Gettysburg Address" by Abraham Lincoln    
    """)

    file = "not_found"
    while file == "not_found":
        file = open_file(which_file(), "r")
    process_file(file)


main()
end_program()
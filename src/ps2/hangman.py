# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "src/ps2/words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    # initiate a variable to keep track whether the word is guessed
    is_guessed = True
    # loop over the letters in the secret word
    for letter in secret_word:
        is_guessed = is_guessed and letter in letters_guessed
    return is_guessed



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    # empty string to record the word
    guessed_word = ''
    # loop over letters in secret_word and add the letter if it's guessed,
    for letter in secret_word:
        if letter in letters_guessed:
            guessed_word += letter
        # or add '_ ' if the letter is not in the list
        else:
            guessed_word += '_ '
    return guessed_word



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    # get all lower letters in the alphabet
    letters_lower = string.ascii_lowercase
    # make a list of alphabets that are not guessed
    available_letters = [letter for letter in letters_lower if letter not in letters_guessed]
    # create a string instead by using join
    available_letters = ''.join(available_letters)
    return available_letters
    
    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    # initiate variables
    VOWELS = ['a', 'e', 'i', 'o', 'u']
    len_word = len(secret_word)
    n_guesses = 6
    letters_guessed = []
    available_letters = get_available_letters(letters_guessed)
    guessed_word = get_guessed_word(secret_word, letters_guessed)
    n_warnings = 3
    # print game start statements
    print('Welcome to the game Hangman!')
    print(f'I am thinking of a word that is {len_word} letters long.')
    print(f'You have {n_warnings} warnings left.')
    print('-------------')
    
    # create a game loop
    while n_guesses > 0:
        available_letters = get_available_letters(letters_guessed)
        print(f'You have {n_guesses} guesses left.')
        print(f'Available_letters: {available_letters}')
        guessed_letter = input('Please guess a letter: ')
        # check if the letters are in the available letters (or in the letters at all)
        if guessed_letter.lower() not in available_letters:
            # check if any warnings left
            if n_warnings > 0:
                n_warnings -= 1
                if guessed_letter.lower() in letters_guessed:
                    print(f"Oops! You've already guessed that letter. You have {n_warnings} warnings left: {guessed_word}")
                else:
                    print(f'Oops! That is not a valid letter. You have {n_warnings} warnings left: {guessed_word}')
            # if not reduce guessed
            else:
                n_guesses -= 1
                if guessed_letter.lower() in letters_guessed:
                    print(f"Oops! You've already guessed that letter. You have no warnings left so you lose one guess: {guessed_word}")
                else:
                    print(f'Oops! That is not a valid letter. You have no warnings left so you lose one guess: {guessed_word}')
            print('-------------')
        else:
            # unify letters using lower
            guessed_letter = guessed_letter.lower()
            letters_guessed.append(guessed_letter)
            guessed_word = get_guessed_word(secret_word, letters_guessed)
            # check if guessed letter is in the word
            if guessed_letter in secret_word:
                print(f'Good guess: {guessed_word}')
            elif guessed_letter not in secret_word:
                print(f'Oops! That letter is not in my word: {guessed_word}')
                # check if the guess is a vowel or consonant
                if guessed_letter in VOWELS:
                    n_guesses -= 2
                else:
                    n_guesses -= 1
            print('-------------')

            if is_word_guessed(secret_word, letters_guessed):
                score = n_guesses * len(set(secret_word))
                print('Congratulations, you won!')
                print(f'Your total score for this game is: {score}')
                break
            
            if n_guesses <= 0:
                print(f'Sorry, you ran out of guesses. The word was {secret_word}.')
                break






# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    # check if the two words are matching length (use strip to remove space in '_ ')
    result = True
    # strip the word (inside '_ ') from spaces
    my_word = ''.join([letter.strip() for letter in my_word])
    if len(my_word) == len(other_word):
        for letter_1, letter_2 in zip(my_word, other_word):
            # make sure the matched letter is not already guessed
            if letter_1 == '_' and letter_2 not in my_word:
                result = result and True
            # check if the letters are the same
            elif letter_1 == letter_2:
                result = result and True
            else:
                result = result and False
    else:
        result = False
    
    return result


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    possible_matches = [word for word in wordlist if match_with_gaps(my_word, word)]
    if len(possible_matches) == 0:
        print("No matches found")
    else:
        print(*possible_matches)



def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    # initiate variables
    VOWELS = ['a', 'e', 'i', 'o', 'u']
    len_word = len(secret_word)
    n_guesses = 6
    letters_guessed = []
    available_letters = get_available_letters(letters_guessed)
    guessed_word = get_guessed_word(secret_word, letters_guessed)
    n_warnings = 3
    # print game start statements
    print('Welcome to the game Hangman!')
    print(f'I am thinking of a word that is {len_word} letters long.')
    print(f'You have {n_warnings} warnings left.')
    print('-------------')
    
    # create a game loop
    while n_guesses > 0:
        available_letters = get_available_letters(letters_guessed)
        print(f'You have {n_guesses} guesses left.')
        print(f'Available_letters: {available_letters}')
        guessed_letter = input('Please guess a letter: ')
        # add a hint mechanism
        if guessed_letter == '*':
            print('Possible word matches are:')
            show_possible_matches(guessed_word)
        # check if the letters are in the available letters (or in the letters at all)
        elif guessed_letter.lower() not in available_letters:
            # check if any warnings left
            if n_warnings > 0:
                n_warnings -= 1
                if guessed_letter.lower() in letters_guessed:
                    print(f"Oops! You've already guessed that letter. You have {n_warnings} warnings left: {guessed_word}")
                else:
                    print(f'Oops! That is not a valid letter. You have {n_warnings} warnings left: {guessed_word}')
            # if not reduce guessed
            else:
                n_guesses -= 1
                if guessed_letter.lower() in letters_guessed:
                    print(f"Oops! You've already guessed that letter. You have no warnings left so you lose one guess: {guessed_word}")
                else:
                    print(f'Oops! That is not a valid letter. You have no warnings left so you lose one guess: {guessed_word}')
            print('-------------')
        else:
            # unify letters using lower
            guessed_letter = guessed_letter.lower()
            letters_guessed.append(guessed_letter)
            guessed_word = get_guessed_word(secret_word, letters_guessed)
            # check if guessed letter is in the word
            if guessed_letter in secret_word:
                print(f'Good guess: {guessed_word}')
            elif guessed_letter not in secret_word:
                print(f'Oops! That letter is not in my word: {guessed_word}')
                # check if the guess is a vowel or consonant
                if guessed_letter in VOWELS:
                    n_guesses -= 2
                else:
                    n_guesses -= 1
            print('-------------')

            if is_word_guessed(secret_word, letters_guessed):
                score = n_guesses * len(set(secret_word))
                print('Congratulations, you won!')
                print(f'Your total score for this game is: {score}')
                break
            
            if n_guesses <= 0:
                print(f'Sorry, you ran out of guesses. The word was {secret_word}.')
                break



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    # secret_word = choose_word(wordlist)
    # hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)

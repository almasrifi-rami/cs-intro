# Problem Set 4C
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string
from ps4a import get_permutations

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


### END HELPER CODE ###

WORDLIST_FILENAME = 'src/ps4/words.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object
                
        text (string): the message's text

        A SubMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)
    
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words
                
    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)
        
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled 
        according to vowels_permutation. The first letter in vowels_permutation 
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52 
        keys of all the uppercase letters and all the lowercase letters.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        transpose_dict = {}
        # match the lower vowels and their permutations
        for vowel_1, vowel_2 in zip(VOWELS_LOWER, vowels_permutation):
            transpose_dict[vowel_1] = vowel_2
        # repeat for the upper vowels
        for vowel_1, vowel_2 in zip(VOWELS_UPPER, [vowel.upper() for vowel in vowels_permutation]):
            transpose_dict[vowel_1] = vowel_2
        # keep all other letters the same
        for letter in CONSONANTS_LOWER + CONSONANTS_UPPER:
            transpose_dict[letter] = letter

        return transpose_dict

    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary
        
        Returns: an encrypted version of the message text, based 
        on the dictionary
        '''
        # initiate the encrypted message
        message_encrypted = ''
        # loop over the letters in the message and add the encrypted letter from transpose_dict to the encrypted message
        for letter in self.get_message_text():
            message_encrypted += transpose_dict.get(letter, letter)

        return message_encrypted
        
class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        super().__init__(text)

    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message 
        
        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.
        
        If no good permutations are found (i.e. no permutations result in 
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message    
        
        Hint: use your function from Part 4A
        '''
        # initiate variables
        n_val_words = 0
        # the message returned will be the original message in case no good decryptions are found
        original_message = self.message_text
        # get the permutations of the lower case vowels (no need for upper)
        permutations = get_permutations(VOWELS_LOWER)

        # loop over the permutations
        for permutation in permutations:
            # get the transpose dictionary
            transpose_dict = super().build_transpose_dict(permutation)
            # apply the dictionary to get the decrypted message
            decrypted_message = super().apply_transpose(transpose_dict)
            # calculate the value by splitting the message into words and checking if they are in word_list and sum()
            val = sum([is_word(self.valid_words, word) for word in decrypted_message.split(" ")])

            # check if the value is higher than n_val_words
            if val > n_val_words:
                # replace n_val_words with the new value
                n_val_words = val
                # replace the original message with the decrypted message
                original_message = decrypted_message

        return original_message

    

if __name__ == '__main__':

    # Example test case
    message = SubMessage("Hello World!")
    permutation = "eaiuo"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Hallu Wurld!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())
     
    #TODO: WRITE YOUR TEST CASES HERE
    message = SubMessage("How are you doing?")
    permutation = "iouea"
    enc_dict = message.build_transpose_dict(permutation)
    print('Original message:', message.get_message_text(), 'Permutation', permutation)
    print('Expected encryption:', "Hew iro yea deung?")
    print('Actual encryption:', message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print('Decrypted message:', enc_message.decrypt_message())

    message = SubMessage("Wie geht es Ihnen?")
    permutation = "uoeai"
    enc_dict = message.build_transpose_dict(permutation)
    print('Original message:', message.get_message_text(), 'Permutation', permutation)
    print('Expected encryption:', "Weo goht os Ehnon?")
    print('Actual encryption:', message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print('Decrypted message:', enc_message.decrypt_message())
# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    # define a base case when sequence is 1 character long
    if len(sequence) == 1:
        return sequence
    # recursive case
    # the code will use set() to avoid duplicates
    # the code will use nested list comprehension to loop over the letters in the sequence and for each of these loops
    # will loop over the permutations of the sequence without this letter
    # using replace() with optional argument to only replace 1 letter in cases of duplicate letters in the sequence
    else:
        return set([i + permutation for i in sequence for permutation in get_permutations(sequence.replace(i, "", 1))])

if __name__ == '__main__':
#    #EXAMPLE
#    example_input = 'abc'
#    print('Input:', example_input)
#    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
#    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)

    example_input_1 = 'abc'
    print('Input:', example_input_1)
    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    print('Actual Output:', get_permutations(example_input_1))

    example_input_2 = 'bust'
    print('Input:', example_input_2)
    print('Expected Output:', ['bust', 'ubst', 'usbt', 'ustb', 'bsut', 'sbut',
                               'subt', 'sutb', 'bstu', 'sbtu', 'stbu', 'stub',
                               'buts', 'ubts', 'utbs', 'utsb', 'btus', 'tbus',
                               'tubs', 'tusb', 'btsu', 'tbsu', 'tsbu', 'tsub'])
    print('Actual Output:', get_permutations(example_input_2))

    example_input_3 = 'ab'
    print('Input:', example_input_3)
    print('Expected Output:', ['ab', 'ba'])
    print('Actual Output:', get_permutations(example_input_3))
    # a simple case with duplicate letters
    example_input_4 = 'aba'
    print('Input:', example_input_4)
    print('Expected Output:', ['aba', 'aab', 'baa'])
    print('Actual Output:', get_permutations(example_input_4))
    # another duplicate letters case
    example_input_5 = 'aaa'
    print('Input:', example_input_5)
    print('Expected Output:', ['aaa'])
    print('Actual Output:', get_permutations(example_input_5))
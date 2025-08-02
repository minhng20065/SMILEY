'''This module tracks errors arising from input in the program.'''
class Error:
    '''This class contains al the methods to detect and handle
    errors in the program arising from inputs.'''
    def verify_numeric(self, num):
        '''This function verifies whether an input is numeric, returning True
        if it is and False if it isn't. It takes in the input to be checked.'''
        return num.isdigit()
    def verity_alpha(self, alpha):
        '''This function verifies whether an input is alphabetical, returning True
        if it is and False if it isn't. It takes in the input to be checked.'''
        return alpha.isalpha()

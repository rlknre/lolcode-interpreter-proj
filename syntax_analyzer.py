
import re

from lexical_analyzer import lexical_tester
from lexical_analyzer import sample1, sample2, sample3, sample4, sample5

test = lexical_tester(sample5)

# arrays for lexeme tracking
code_per_line = []

# arrays for syntax tracking
errors = []


# test if code syntax of lolcode is valid
def syntax_tester(code, code_details):

    code_block = code_details
    reading_line = 1

    while True:

        if reading_line > len(code_details):
            break

        current_line = code_block[reading_line-1]

        if len(current_line) > 1:
            check_syntax = current_line[1:]
            print(check_syntax)
        else:
            print("<linebreak>")

        reading_line += 1
    
# testing 

syntax_tester(sample5, test)
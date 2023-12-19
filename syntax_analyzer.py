import re

# import lexical analyzer function
from lexical_analyzer import lexical_tester

# import retrieved tokens from lexical analyzer
from lexical_analyzer import token_list

# import sample code blocks
from lexical_analyzer import sample1, sample2, sample3, sample4, sample5

# import keyword classifiers
from lexical_analyzer import DELIMITER_CODE, DELIMITER_STR, DELIMITER_VAR, DELIMITER_CONDT, DELIMITER_END
from lexical_analyzer import IDENTIFIER_VARS, IDENTIFIER_FUNC, IDENTIFIER_LOOP
from lexical_analyzer import VAR_DECLARE, VAR_ASSIGN

from lexical_analyzer import KEYWORD_COMMENT
from lexical_analyzer import KEYWORD_ARITHMETIC 
from lexical_analyzer import KEYWORD_SEPERATOR 
from lexical_analyzer import KEYWORD_SEPERATOR 
from lexical_analyzer import KEYWORD_BOOLEAN 
from lexical_analyzer import KEYWORD_CONCAT 
from lexical_analyzer import KEYWORD_TYPECAST 
from lexical_analyzer import KEYWORD_PRINT 
from lexical_analyzer import KEYWORD_INPUT 
from lexical_analyzer import KEYWROD_CONDT 
from lexical_analyzer import KEYWORD_LOOP 
from lexical_analyzer import KEYWORD_FUNC 

from lexical_analyzer import LITERAL
from lexical_analyzer import LITERAL_NUMBAR
from lexical_analyzer import LITERAL_NUMBR
from lexical_analyzer import LITERAL_TROOF
from lexical_analyzer import LITERAL_YARN


# arrays for syntax tracking
errors = []

# test if code syntax of lolcode is valid
def syntax_tester(code_details):

    code_delimiter_start = False
    varsec_delimiter_start = False

    varsec_line_start = 0
    varsec_line_end = 0
    
    code_block = code_details

    # for checking
    # for line in code_block: print(line)
    # print("")

    # variables for comment cleaning
    searching_TLDR = 0
    searching_TLDR_from_line = 0

    # remove instances of comments
    for line in code_block:

        error_information = []

        if len(line) > 1:

            # search for instances for TLDR after reading OBTW
            if searching_TLDR == 1:
                if len(line) == 2:
                    if line[-1][0] == 'TLDR' and line[-1][1] == KEYWORD_COMMENT:
                        line.pop()
                        searching_TLDR = 0

            # searcy for instances of comments
            elif searching_TLDR == 0:

                # single-line comments
                if line[-1][0] == 'BTW' and line[-1][1] == KEYWORD_COMMENT:
                    line.pop()

                # multi-line comments
                if ['OBTW', KEYWORD_COMMENT] in line:
                
                    for keyword in line:
                        if not(isinstance(keyword, list)): 
                            continue
                        # skip line counters in code line detail

                        # invalid OBTW instance
                        if keyword[0] == 'OBTW' and keyword[1] == KEYWORD_COMMENT:

                            searching_TLDR = 1
                            searching_TLDR_from_line = str(line[0])

                            # possible errors for OBTW / TLDR
                            if len(line) > 2 and line[-1] == ['TLDR', KEYWORD_COMMENT]:
                                errors.append("Invalid TLDR multiline syntax at Line " + str(line[0]))
                                searching_TLDR = 0
                                searching_TLDR_from_line = 0
                            if len(line) > 2 or keyword != line[-1]:
                                errors.append("Invalid OBTW multiline syntax at Line " + str(line[0]))

                                while True:
                                    if line[-1][0] == 'OBTW': 
                                        line.pop()
                                        break
                                    line.pop()

                        # valid OBTW instance
                        if len(line) == 2 and keyword == ['OBTW', KEYWORD_COMMENT]:
                            line.pop()                   
    # end of loop for cleaning up comments

    if searching_TLDR == 1:
        errors.append("Invalid multiline syntax, no TLDR for OBTW at Line " + searching_TLDR_from_line)
    
    # IMPORTANT: In this part, we only check the syntax of the whole code if there are no errors
    # in the comments part. If ever there is an OBTW with a missing TLDR, it sees the code
    # block after the OBTW as a whole multiline comment, hence, no code syntax to check


    else:
    # for checking
        print("")
        for line in code_block:
            print(line)
            print(str(len(line)) + "\n")
        # print("\nValid comments!")

    # IMPORTANT: Here, we start checking the syntax of the keywords in the code block.
    # We implement a For Loop that checks each code line details and determines whether
    # the succession of keywords are valid or not.

    for line in code_block:

        if len(line) > 1:

            line_no = str(line[0])
            
            # HAI not yet found
            if code_delimiter_start == False:

                # HAI
                if line[1][0] in token_list:
                    if line[1][0] == 'HAI' and line[1][1] == DELIMITER_CODE:
                        code_delimiter_start = True
                    elif line[1][0] != 'HAI' and line[1][1] != DELIMITER_CODE:
                        errors.append("Line " + line_no + ": Invalid syntax, should start with HAI first")

            # HAI code block section
            elif code_delimiter_start == True:

                # WAZZUP
                if line[1][0] == 'WAZZUP' and line[1][1] == DELIMITER_VAR:
                    if len(line) > 2:
                        errors.append("Line " + line_no + ": Invalid WAZZUP syntax, declaration of variable section")
                    elif len(line) == 2:
                        # currently in WAZZUP, should end with BUHBYE
                        varsec_delimiter_start = True
                        varsec_line_start = line_no

                # BUHBYE
                if line[1][0] == 'BUHBYE' and line[1][1] == DELIMITER_VAR:
                    if len(line) > 2:
                        errors.append("Line " + line_no + ": Invalid BUHBYE syntax, end of variable section")
                    elif len(line) == 2:
                        varsec_delimiter_start = False
                        varsec_line_end = line_no
                
                # I HAS A
                if line[1][0] == 'I HAS A' and line[1][1] == VAR_DECLARE:
                    # missing values
                    if len(line) < 2:
                        errors.append("Line " + line_no + ": Invalid I HAS A syntax in variable declaration")
                    # check for literal
                    if len(line) >= 3:
                        if line[2][1] != IDENTIFIER_VARS:
                            errors.append("Line " + line_no + ": Invalid I HAS A syntax, should have valid variable")
                    # assignment to variable
                    if len(line) >= 4:
                        if len(line) == 4:
                            errors.append("Line " + line_no + ": Invalid I HAS A syntax, should have ITZ to initialize")
                        else:
                            # variable
                            if line[3][1] != VAR_ASSIGN:
                                errors.append("Line " + line_no + ": Invalid I HAS A syntax, should have ITZ to initialize")
                            # also checks expression instance
                            if line[4][1] not in [KEYWORD_ARITHMETIC, LITERAL_NUMBAR, LITERAL_NUMBR, LITERAL_TROOF, LITERAL_YARN, IDENTIFIER_VARS]:
                                errors.append("Line " + line_no + ": Invalid I HAS A syntax, should have valid variable")
                    
                    # NOTE: add condition for expressions

                    if len(line) >= 6:
                        if line[4][1] != KEYWORD_ARITHMETIC:
                            errors.append("Line " + line_no + ": Invalid I HAS A syntax, waiting for expression")
                    
                    # NOTE: for editing here ^

                # VISIBLE
                if line[1][0] == 'VISIBLE' and line[1][1] == KEYWORD_PRINT:
                    if len(line) < 2:
                        errors.append("Line " + line_no + ": Invalid VISIBLE syntax, waiting for values to print")
                    if len(line) >= 3:
                        if line[2][1] not in [IDENTIFIER_VARS, LITERAL_NUMBAR, LITERAL_NUMBR, LITERAL_TROOF, LITERAL_TROOF, LITERAL_YARN]:
                            errors.append("Line " + line_no + ": Invalid VISIBLE syntax, waiting for values to print")
                        else:
                        # check for concatenation 
                            if ((len(line) - 3) >= 2) and ((len(line) - 3) % 2 == 0):

                                # let x be the index we are checking, note that we adjust +3 since we want to
                                # access the indeces after the first instance of the variable to print

                                for x in range(0, len(line)-3):
                                    
                                    # + keyword
                                    if x % 2 == 0:
                                        if line[x+3][1] != KEYWORD_CONCAT:
                                            errors.append("Line " + line_no + ": Invalid VISIBLE syntax, waiting for concatenation keyword")
                                    # variables
                                    elif x % 2 != 0:
                                        if line[x+3][1] not in [IDENTIFIER_VARS, LITERAL_NUMBAR, LITERAL_NUMBR, LITERAL_TROOF, LITERAL_TROOF, LITERAL_YARN]:
                                            errors.append("Line " + line_no + ": Invalid VISIBLE syntax, waiting for value to print")
                            
                            # invalid number of multivalues to print
                            else:
                                errors.append("Line " + line_no + ": Invalid VISIBLE syntax, invalid print parameters")


    # end of for loop for checking syntax

    # check if variable section is valid
    if varsec_delimiter_start == True:
        errors.append("Line " + varsec_line_start + ": Invalid WAZZUP syntax, BUHBYE keyword not found")


# testing 

sample = """HAI
BTW comment here
WAZZUP
    I HAS A thing
    I HAS A thing2 ITZ SUM OF 5 AN 4
BUHBYE
OBTW yes
TLDR
GIMMEH var      BTW this asks for an input

SMOOSH "Heyy string" AN "HellO there" AN " HUH"
VISIBLE "Concat" + " these " + "no" +

VISIBLE HAI
KTHXBYE
"""

test = lexical_tester(sample)
syntax_tester(test)
print("")
for error in errors:
    print(error)
print("")
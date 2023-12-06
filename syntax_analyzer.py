
import re

from lexical_analyzer import lexical_tester
from lexical_analyzer import token_list
from lexical_analyzer import sample1, sample2, sample3, sample4, sample5

# arrays for syntax tracking
errors = []

# test if code syntax of lolcode is valid
def syntax_tester(code_details):
    
    code_delimiter_start = False
    code_delimiter_end = False
    code_block = code_details
    
    reading_line = 1

    while True:
        if reading_line > len(code_details):
            break
        # end loop if all lines read

        current_line = code_block[reading_line-1]
        # print(current_line)
        # start syntax checking here
        if len(current_line) > 1:

            check_syntax = current_line[1:]
            lexeme_count = len(check_syntax[0:])
            starting_token = check_syntax[0][0]
            # print(check_syntax)
            # print(starting_token)
            # print(lexeme_count)
            # print("")

            # check first if code delimiter starter "HAI" exists
            if code_delimiter_start == False:
                if starting_token in token_list:

                    # valid keywords before "HAI"

                    # function
                    if starting_token == "HOW IZ I":
                        if lexeme_count > 1:
                            func_name = check_syntax[1][1]
                            if func_name == 'Variable Identifier':
                                
                                # ADD CHECKER FOR FUNC PARAMETERS
                                # if lexeme_count > 4:
                                #     func_parameters = check_syntax[2:]

                                # loops until it finds "IF U SAY SO" keyword
                                func_start_line = reading_line
                                while True:

                                    if reading_line > len(code_details):
                                        errors.append("No function ender for function in line " + str(func_start_line))
                                        break
                                    
                                    current_line = code_block[reading_line-1]

                                    if len(current_line) > 1:
                                        check_syntax = current_line[1:]
                                        lexeme_count = len(check_syntax)
                                        starting_token = check_syntax[0][0]

                                        if starting_token == "IF U SAY SO":
                                            break
                                    reading_line += 1
                                # eo loop 

                            else:
                                errors.append("Invalid function name at Line " + str(reading_line))
                        else:
                            errors.append("Invalid function parameters at Line " + str(reading_line))

                    # comments
                    elif starting_token == "BTW":
                        None
                    elif starting_token == "OBTW":
                        
                        # search for TLDR multiline ender
                        comment_start_line = reading_line
                        while True:
                            
                            if reading_line > len(code_details):
                                errors.append("No multiline comment ender for comment in line" + str(comment_start_line))
                                break
                            current_line = code_block[reading_line-1]

                            if len(current_line) > 1:
                                starting_token = check_syntax[0][0]
                                if starting_token == "TLDR":
                                    break
                            
                            reading_line += 1
                    
                    # start of code
                    elif starting_token == "HAI":
                        code_delimiter_start = True

                    # invalid keyword found before "HAI"
                    else:
                        if "Program should start with HAI" not in errors:
                            errors.append("Program should start with HAI")

            # HAI keyword found, proceed to block of code
            elif code_delimiter_start == True:
                
                # var initialization
                if starting_token == "I HAS A":
                    None
                
                # printing
                elif starting_token == "VISIBLE":
                    if lexeme_count >= 2:
                        if lexeme_count == 2:
                            if check_syntax[1][1] == "Variable Identifier":
                                None
                            elif check_syntax[1][1] == "Literal":
                                None
                            else:
                                errors.append("Error: Should be VISIBLE <var> at Line " + str(reading_line))
                        else:
                            None
                            # ADD: Condt for concatenation of printing values
                    else:
                        errors.append("Error: Should be VISIBLE <var> at Line " + str(reading_line))
                
                # input
                elif starting_token == "GIMMEH":
                    if lexeme_count == 2:
                        if check_syntax[1][1] != "Variable Identifier":
                            errors.append("Error, should have variable receiver for GIMMEH at Line " + str(reading_line))
                    else:
                        errors.append("Error in GIMMEH input at Line " + str(reading_line))

                # end of program
                elif starting_token == "KTHXBYE":
                    code_delimiter_end = True

        # updates line the analyzer is reading
        reading_line += 1

    # check that program should end valid way
    if code_delimiter_end == False and code_delimiter_start == True:
        errors.append("Program should end with KTHNXBYE")

# testing 

sample = """HOW IZ I func_name
    BTW ANYTHING
IF U SAY SO

HAI
GIMMEH 
VISIBLE 
KTHXBYE
"""

test = lexical_tester(sample)
syntax_tester(test)
print("")
for error in errors:
    print(error)
print("")

# NOTES:
# lexical structure tas s agui
# tanggalin na comments sa lexical palang checker
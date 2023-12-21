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
from lexical_analyzer import LITERAL_NOOB


# arrays for syntax tracking
errors = []

# test if code syntax of lolcode is valid
def syntax_tester(code_details):

    code_delimiter_start = False
    varsec_delimiter_start = False
    func_delimiter_start = False
    switch_delimiter_start = False
    loop_delimiter_start = False

    func_line_start = 0
    switch_line_start = 0
    loop_line_start = 0
    varsec_line_start = 0
    varsec_line_end = 0
    
    code_block = code_details

    # for checking
    # for line in code_block: print(line)
    # print("")

    # variables for comment cleaning
    invalid_OBTW = 0
    invalid_TLDR = 0
    searching_TLDR = 0
    searching_TLDR_from_line = 0

    # remove instances of comments
    for line in code_block:

        error_information = []

        if len(line) > 1:

            # ----------------------------------------------------------------------------------------------------------------------------------------------

            # TLDR
            if searching_TLDR == 1:
                if len(line) == 2:
                    if line[-1][0] == 'TLDR' and line[-1][1] == KEYWORD_COMMENT:
                        line.pop()
                        searching_TLDR = 0
            
            # ----------------------------------------------------------------------------------------------------------------------------------------------

            # search for instances of comments
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
                                errors.append("Line " + str(line[0]) + ": Invalid TLDR multiline syntax")
                                searching_TLDR = 0
                                searching_TLDR_from_line = 0
                            if len(line) > 2 or keyword != line[-1]:
                                errors.append("Line " + str(line[0]) + ": Invalid OBTW multiline syntax")
                                invalid_OBTW = 1

                                while True:
                                    if line[-1][0] == 'OBTW': 
                                        line.pop()
                                        break
                                    line.pop()

                        # valid OBTW instance
                        if len(line) == 2 and keyword == ['OBTW', KEYWORD_COMMENT]:
                            line.pop() 
                
                if ['TLDR', KEYWORD_COMMENT] in line:
                    errors.append("Line " + str(line[0]) + ": Invalid TLDR multiline declaration, no OBTW")

            # ---------------------------------------------------------------------------------------------------------------------------------------------- 
                 
    # end of loop for cleaning up comments

    if searching_TLDR == 1 or invalid_TLDR == 1:
        errors.append("Line " + searching_TLDR_from_line + ": Invalid multiline syntax, no TLDR for OBTW")
    
    # IMPORTANT: In this part, we only check the syntax of the whole code if there are no errors
    # in the comments part. If ever there is an OBTW with a missing TLDR, it sees the code
    # block after the OBTW as a whole multiline comment, hence, no code syntax to check

    # for checking
    # print("")
    # for line in code_block:
    #     print(line)
    #     print(str(len(line)) + "\n")

    else:

    # IMPORTANT: Here, we start checking the syntax of the keywords in the code block.
    # We implement a For Loop that checks each code line details and determines whether
    # the succession of keywords are valid or not.

        for line in code_block:

            if len(line) > 1:

                line_no = str(line[0])
                
                # HAI, HOW IZ I not yet found
                if code_delimiter_start == False and func_delimiter_start == False:

                    # ----------------------------------------------------------------------------------------------------------------------------------------------

                    # only checks valid starting keywords before HAI
                    if line[1][0] in token_list:

                        if line[1][0] in ['HAI', 'HOW IZ I', 'KTHXBYE']:

                            # HAI
                            if line[1][0] == 'HAI' and line[1][1] == DELIMITER_CODE:
                                if len(line) != 2:
                                    errors.append("Line " + line_no + ": Invalid HAI syntax")
                                elif len(line) == 2:
                                    code_delimiter_start = True

                    # ----------------------------------------------------------------------------------------------------------------------------------------------
                            
                            # Invalid KTHXBYE
                            if line[1][0] == 'KTHXBYE' and line[1][1] == DELIMITER_CODE:
                                if len(line) != 2:
                                    errors.append("Line " + line_no + ": Invalid KTHXBYE syntax")
                                elif len(line) == 2:
                                    errors.append("Line " + line_no + ": Invalid KTHXBYE syntax, waiting for HAI keyword")

                    # ----------------------------------------------------------------------------------------------------------------------------------------------

                            # HOW IZ I
                            if line[1][0] == 'HOW IZ I' and line[1][1] == IDENTIFIER_FUNC:
                                if len(line) <= 2:
                                    errors.append("Line " + line_no + ": Invalid HOW IZ I syntax, missing function parameters")
                                # check its parameters
                                elif len(line) >= 3:

                                    # Still checks if there is a valid IF U SAY SO
                                    func_delimiter_start = True
                                    func_line_start = line_no

                                    # no parameters
                                    if len(line) == 3:
                                        if line[-1][1] != IDENTIFIER_VARS:
                                            errors.append("Line " + line_no + ": Invalid HOW IZ I function parameters")

                                    # with parameters
                                    elif len(line) > 3:
                                        if len(line) == 4:
                                            errors.append("Line " + line_no + ": Invalid HOW IZ I function parameters")

                                        # one parameter
                                        elif len(line) == 5:
                                            if line[3][0] != 'YR' or line[3][1] != KEYWORD_SEPERATOR:
                                                errors.append("Line " + line_no + ": Invalid HOW IZ I function parameters")
                                            elif line[4][1] != IDENTIFIER_VARS:
                                                errors.append("Line " + line_no + ": Invalid HOW IZ I function parameters")

                                        # multiple parameters
                                        elif len(line) >= 6:

                                            # For value parameters, there should always be an iteration of 3 additional parameters
                                            # for multiple parameter count. Following the syntax [AN] [YR] [varident]
                                            parameters = len(line) - 5

                                            # invalid
                                            if parameters % 3 != 0:
                                                errors.append("Line " + line_no + ": Invalid HOW IZ I function parameters")

                                            # valid
                                            else:
                                                # checker for syntax to check
                                                check_for_AN = 1
                                                check_for_YR = 0
                                                check_for_varident = 0

                                                for x in range(0, len(line)-5):

                                                    # AN keyword
                                                    if check_for_AN == 1:
                                                        if line[x+5][0] == 'AN' and line[x+5][1] == KEYWORD_SEPERATOR:
                                                            check_for_YR = 1
                                                            check_for_AN = 0
                                                        else:
                                                            errors.append("Line " + line_no + ": Invalid function parameter, waiting for AN keyword")
                                                            break

                                                    # YR keyword
                                                    elif check_for_YR == 1:
                                                        if line[x+5][0] == 'YR' and line[x+5][1] == KEYWORD_SEPERATOR:
                                                            check_for_varident = 1
                                                            check_for_YR = 0
                                                        else:
                                                            errors.append("Line " + line_no + ": Invalid function parameter, waiting for YR keyword")
                                                            break

                                                    # valid varident keyword
                                                    elif check_for_varident == 1:
                                                        if line[x+5][1] == IDENTIFIER_VARS:
                                                            check_for_AN = 1
                                                            check_for_varident = 0
                                                        else:
                                                            errors.append("Line " + line_no + ": Invalid function parameter, waiting for valid variable")
                                                            break
                                        
                    # ----------------------------------------------------------------------------------------------------------------------------------------------

                        # invalid starting keyword before HAI
                        else:
                            errors.append("Line " + line_no + ": Invalid syntax, should be inside valid code sections")

                    # invalid lexeme keyword found
                    else: 
                        errors.append("Line " + line_no + ": Invalid syntax, found keyword not in lexemes")

                    # ----------------------------------------------------------------------------------------------------------------------------------------------

                # Main program or Function code block section
                elif (code_delimiter_start == True) or (func_delimiter_start == True):

                    # ----------------------------------------------------------------------------------------------------------------------------------------------

                    # Invalid keywords in HAI-KTHXBYE
                    if line[1][0] in ['HOW IZ I', 'IF U SAY SO']:
                        if code_delimiter_start ==  True and func_delimiter_start == False:
                            errors.append("Line " + line_no + ": Invalid keyword in HAI-KTHXBYE code block")

                    # ----------------------------------------------------------------------------------------------------------------------------------------------

                    # keywords for varident operations
                    if line[1][1] == IDENTIFIER_VARS:

                        # valid
                        if len(line) >= 4:

                            # R and IS NOW A
                            if len(line) == 4:

                                # R
                                if line[2][0] == 'R' and line[2][1] == VAR_ASSIGN:

                                    # NOTE: Insert expression instance for succeeding if statement

                                    if line[3][1] not in [IDENTIFIER_VARS, LITERAL_NUMBAR, LITERAL_NUMBR, LITERAL_TROOF, LITERAL_YARN]:
                                        errors.append("Line " + line_no + ": Invalid R parameter, expecting literal, variable, or expression")
                                
                                # IS NOW A
                                elif line[2][0] == 'IS NOW A' and line[2][1] == KEYWORD_TYPECAST:
                                    if line[3][1] != LITERAL:
                                        errors.append("Line " + line_no + ": Invalid typecasting, expecting literal type")

                                else:
                                    errors.append("Line " + line_no + ": Invalid typecasting parameters")

                            # R MAEK
                            elif len(line) == 6:
                                if line[2][0] == 'R' and line[2][1] == VAR_ASSIGN and line[3][0] == 'MAEK' and line[3][1] == KEYWORD_TYPECAST:
                                    if line[4][1] != IDENTIFIER_VARS or line[5][1] != LITERAL:
                                        errors.append("Line " + line_no + ": Invalid typecasting parameters")
                                else:
                                    errors.append("Line " + line_no + ": Invalid typecasting parameters")
                            
                            else:
                                errors.append("Line " + line_no + ": Invalid typecasting parameters")
                                
                        # invalid
                        else:
                            errors.append("Line " + line_no + ": Waiting for an operation for the variable")

                    # ----------------------------------------------------------------------------------------------------------------------------------------------

                    # KTHXBYE
                    if line[1][0] == 'KTHXBYE' and line[1][1] == DELIMITER_CODE:
                        if code_delimiter_start == True:
                            if len(line) != 2:
                                errors.append("Line " + line_no + ": Invalid KTHXBYE syntax")
                            elif len(line) == 2:
                                code_delimiter_start = False
                        else:
                            errors.append("Line " + line_no + ": Invalid KTHXBYE call")
                                
                    # ----------------------------------------------------------------------------------------------------------------------------------------------

                    # IF U SAY SO
                    if line[1][0] == 'IF U SAY SO' and line[1][1] == IDENTIFIER_FUNC:
                        if func_delimiter_start == True:
                            if len(line) != 2:
                                errors.append("Line " + line_no + ": Invalid IF U SAY SO syntax")
                            elif len(line) == 2:
                                func_delimiter_start = False
                        else:
                            errors.append("Line " + line_no + ": Invalid IF U SAY SO call")

                    # ----------------------------------------------------------------------------------------------------------------------------------------------

                    # FOUND YR


                    # ----------------------------------------------------------------------------------------------------------------------------------------------

                    # GTFO
                    if line[1][0] == 'GTFO' and line[1][1] == KEYWORD_FUNC:
                        if func_delimiter_start == True:
                            if len(line) != 2:
                                errors.append("Line " + line_no + ": Invalid GTFO syntax")
                        else:
                            errors.append("Line " + line_no + ": Invalid GTFO call")

                    # ----------------------------------------------------------------------------------------------------------------------------------------------

                    # I IZ


                    # ----------------------------------------------------------------------------------------------------------------------------------------------

                    # WAZZUP
                    if line[1][0] == 'WAZZUP' and line[1][1] == DELIMITER_VAR:
                        if func_delimiter_start == False:
                            if len(line) > 2:
                                errors.append("Line " + line_no + ": Invalid WAZZUP syntax, declaration of variable section")
                            elif len(line) == 2:
                                # currently in WAZZUP, should end with BUHBYE
                                varsec_delimiter_start = True
                                varsec_line_start = line_no
                        # should not be within a function
                        else:
                            errors.append("Line " + line_no + ": Invalid WAZZUP syntax, should not be inside function")

                    # ----------------------------------------------------------------------------------------------------------------------------------------------

                    # BUHBYE
                    if line[1][0] == 'BUHBYE' and line[1][1] == DELIMITER_VAR:
                        if func_delimiter_start == False:
                            varsec_line_end = line_no
                            if len(line) > 2:
                                errors.append("Line " + varsec_line_end + ": Invalid BUHBYE syntax, end of variable section")
                            elif len(line) == 2:
                                # check if WAZZUP already exists
                                if varsec_delimiter_start == False:
                                    errors.append("Line " + line_no + ": Invalid BUHBYE syntax, expected WAZZUP before instance")
                                else:
                                    varsec_delimiter_start = False
                        # should not be within a function
                        else:
                            errors.append("Line " + line_no + ": Invalid BUHBYE syntax, should not be inside function")
                            
                    # ----------------------------------------------------------------------------------------------------------------------------------------------
                    
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

                    # ----------------------------------------------------------------------------------------------------------------------------------------------

                    # VISIBLE
                    if line[1][0] == 'VISIBLE' and line[1][1] == KEYWORD_PRINT:
                        if len(line) <= 2:
                            errors.append("Line " + line_no + ": Invalid VISIBLE syntax, waiting for values to print")
                        if len(line) >= 3:
                            if line[2][1] not in [IDENTIFIER_VARS, LITERAL_NUMBAR, LITERAL_NUMBR, LITERAL_TROOF, LITERAL_TROOF, LITERAL_YARN]:
                                errors.append("Line " + line_no + ": Invalid VISIBLE syntax, waiting for values to print")
                            else:
                            # check for multiple values (should be even len(line)-3 since 1 concat keyword is to 1 var)
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
                                    if len(line) > 3:
                                        errors.append("Line " + line_no + ": Invalid VISIBLE syntax, invalid print parameters")

                    # ----------------------------------------------------------------------------------------------------------------------------------------------

                    # SMOOSH
                    if line[1][0] == 'SMOOSH' and line[1][1] == KEYWORD_CONCAT:
                        # check if nested
                        if line.count(['SMOOSH', KEYWORD_CONCAT]) > 1:
                            errors.append("Line " + line_no + ": Invalid SMOOSH syntax, no nesting for this operation")
                        else:
                            if len(line) < 4:
                                errors.append("Line " + line_no + ": Invalid SMOOSH syntax, waiting for values to concatenate")
                            if len(line) >= 5:
                                if line[2][1] not in [IDENTIFIER_VARS, LITERAL_NUMBAR, LITERAL_NUMBR, LITERAL_TROOF, LITERAL_TROOF, LITERAL_YARN]:
                                    errors.append("Line " + line_no + ": Invalid SMOOSH syntax, waiting for values to concatenate")
                                else:
                                # check for concatenation, also retrieves MKAY keyword
                                    if ((len(line) - 3) >= 2):

                                        # let x be the index we are checking, note that we adjust +3 since we want to
                                        # access the indeces after the first instance of the variable to print

                                        for x in range(0, len(line)-3):
                                            
                                            # + keyword
                                            if x % 2 == 0:
                                                if line[x+3][1] != KEYWORD_SEPERATOR:

                                                    # check for MKAY keyword
                                                    if (x+1) == (len(line)-3):
                                                        if line[x+3][1] != DELIMITER_END:
                                                            errors.append("Line " + line_no + ": Invalid SMOOSH syntax, invalid concatenate parameters")
                                                    # not yet end of code line
                                                    else:
                                                        errors.append("Line " + line_no + ": Invalid SMOOSH syntax, waiting for seperator keyword")
                                                else:
                                                    # check if invalid last value
                                                    if (x+1) == (len(line)-3) and (line[x+3][0] == line[-1][0]):
                                                        errors.append("Line " + line_no + ": Invalid SMOOSH syntax, waiting for value to print")
                                            # variables
                                            elif x % 2 != 0:
                                                if line[x+3][1] not in [IDENTIFIER_VARS, LITERAL_NUMBAR, LITERAL_NUMBR, LITERAL_TROOF, LITERAL_TROOF, LITERAL_YARN]:
                                                    errors.append("Line " + line_no + ": Invalid SMOOSH syntax, waiting for value to print")
                                    
                                    # invalid number of multivalues to print
                                    else:
                                        if len(line) > 3:
                                            errors.append("Line " + line_no + ": Invalid SMOOSH syntax, invalid concatenate parameters")

                    # ----------------------------------------------------------------------------------------------------------------------------------------------

                    # GIMMEH
                    if line[1][0] == 'GIMMEH' and line[1][1] == KEYWORD_INPUT:
                        if len(line) != 3:
                            errors.append("Line " + line_no + ": Invalid GIMMEH syntax, waiting for input parameter")
                        elif len(line) == 3:
                            # waiting for variable
                            if line[2][1] != IDENTIFIER_VARS:
                                errors.append("Line " + line_no + ": Invalid GIMMEH syntax, should be followed by a variable")

                    # ----------------------------------------------------------------------------------------------------------------------------------------------

        # end of for loop for checking syntax
    
    # check if function section is valid
    if func_delimiter_start == True:
        errors.append("Line " + func_line_start + ": Invalid HOW IZ I syntax, valid IF U SAY SO keyword not found")
    
    # check if code block section is valid
    if code_delimiter_start == True:
        errors.append("Line " + func_line_start + ": Invalid HAI syntax, valid KTHXBYE keyword not found")

    # check if variable section is valid
    if varsec_delimiter_start == True and invalid_OBTW == 0:
        errors.append("Line " + varsec_line_start + ": Invalid WAZZUP syntax, BUHBYE keyword not found")
    elif varsec_delimiter_start == True and invalid_OBTW == 1:
        errors.append("Line " + varsec_line_start + ": Invalid BUHBYE syntax for WAZZUP keyword")


    # IMPORTANT: Here, we pass the values of the cleaned code block and if the code is valid
    # Returns 0 if syntax errors exist
    # Returns 1 if there are no syntax errors

    if len(errors) > 0:
        return [code_block, 0]
    elif len(errors) == 0:
        return [code_block, 1]
    # error trap
    else: return [code_block, 0]


# testing 

sample = """HAI
    I HAS A var1
    I HAS A var2 ITZ 12
    I HAS A var3

    VISIBLE "noot noot" + var2

    var2 IS NOW A NUMBAR
    VISIBLE var2

    var1 R 17
    var2 R var1

    var2 R MAEK var2 YARN

    VISIBLE "Need input: "
    GIMMEH var3

KTHXBYE"""

# print("")
# test = lexical_tester(sample)
# syntax_tester(test)
# print("")

if len(errors) > 0:
    for error in errors:
        print(error)
    print("")
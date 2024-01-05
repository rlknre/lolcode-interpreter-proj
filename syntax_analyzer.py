import re

# import lexical analyzer function
from lexical_analyzer import lexical_tester

# import retrieved tokens from lexical analyzer
from lexical_analyzer import token_list
from lexical_analyzer import token_classification

# import sample code blocks
from lexical_analyzer import sample1, sample2, sample3, sample4, sample5

# import keyword classifiers
from keywords import DELIMITER_CODE, DELIMITER_STR, DELIMITER_VAR, DELIMITER_CONDT, DELIMITER_END
from keywords import IDENTIFIER_VARS, IDENTIFIER_FUNC, IDENTIFIER_LOOP
from keywords import VAR_DECLARE, VAR_ASSIGN

from keywords import KEYWORD_COMMENT
from keywords import KEYWORD_ARITHMETIC 
from keywords import KEYWORD_SEPERATOR 
from keywords import KEYWORD_SEPERATOR 
from keywords import KEYWORD_BOOLEAN 
from keywords import KEYWORD_CONCAT 
from keywords import KEYWORD_TYPECAST 
from keywords import KEYWORD_PRINT 
from keywords import KEYWORD_INPUT 
from keywords import KEYWROD_CONDT 
from keywords import KEYWORD_LOOP 
from keywords import KEYWORD_FUNC 

from keywords import LITERAL
from keywords import LITERAL_NUMBAR
from keywords import LITERAL_NUMBR
from keywords import LITERAL_TROOF
from keywords import LITERAL_YARN
from keywords import LITERAL_NOOB


# arrays for syntax tracking
errors = []

# function for checking code syntax of expressions (arithmetic/boolean operations)
def expression_tester(line_no, line, operation_type):

    # checker
    operation = 0
    operand = 0
    not_count = 0
    expecting_seperator = 0

    if len(line) < 1:
        errors.append("Line " + line_no + ": Invalid operation syntax detected")
    else:

        # ----------------------------------------------------------------------------------------------------------------------------------------------

        if line[0][1] == operation_type:

            if len(line) < 2:
                 errors.append("Line " + line_no + ": Operation missing some values")
                 return 0
            
            else:
                # Arithmetic checker of last value
                if (operation_type == KEYWORD_ARITHMETIC) and line[-1][1] not in [IDENTIFIER_VARS, LITERAL_NUMBR, LITERAL_NUMBAR, LITERAL_TROOF, LITERAL_YARN]:
                    errors.append("Line " + line_no + ": Invalid operation, should end with operand")
                    return 0
                
                # Boolean checker (ALL OF and ANY OF)
                elif (operation_type == KEYWORD_BOOLEAN) and (line[0][0] in ['ALL OF', 'ANY OF']) and (line[-1][0] != 'MKAY' and line[-1][1] != DELIMITER_END):
                    errors.append("Line " + line_no + ": Missing MKAY call for operation")
                    return 0
                
                # Boolean checker (not ALL OF or ANY OF)
                elif (operation_type == KEYWORD_BOOLEAN) and (line[0][0] not in ['ALL OF', 'ANY OF']) and line[-1][1] not in [IDENTIFIER_VARS, LITERAL_NUMBR, LITERAL_NUMBAR, LITERAL_TROOF, LITERAL_YARN]:
                    errors.append("Line " + line_no + ": Invalid operation, should end with operand")
                    return 0

                else:

                    # since NOT operations only require one operand
                    if line[0][0] == 'NOT' and operation_type == KEYWORD_BOOLEAN:
                        not_count +=1

                    # since we already checked first value
                    operation += 1

                    # count operand and operations / also check if seperator syntax is correct
                    for x in range(1, len(line)):

                        # nested ALL OF / ANY OF catcher
                        if line[x][0] == 'ALL OF' or line[x][0] == 'ANY OF':
                            errors.append("Line " + line_no + ": Nested ALL OF / ANY OF not allowed")
                            return 0

                        # expecting operation / operand
                        if expecting_seperator == 0:

                            # operation
                            if line[x][1] == operation_type:
                                operation += 1
                                if operand > 0:
                                    expecting_seperator = 1
                                if line[x][0] == 'NOT' and operation_type == KEYWORD_BOOLEAN:
                                    not_count +=1
                                
                            # operand
                            elif line[x][1] in [IDENTIFIER_VARS, LITERAL_NUMBR, LITERAL_NUMBAR, LITERAL_TROOF, LITERAL_YARN]:
                                expecting_seperator = 1
                                operand += 1
                            
                            # invalid
                            else:
                                errors.append("Line " + line_no + ": Invalid call, waiting for operation / value")
                                return 0

                        # expecting separator keyword
                        elif expecting_seperator == 1:
                            if line[x][0] == 'AN' and line[x][1] == KEYWORD_SEPERATOR:
                                expecting_seperator = 0
                            # nested operations
                            elif line[x][1] == operation_type:
                                expecting_seperator = 0
                                operation += 1
                                if line[x][0] == 'NOT' and operation_type == KEYWORD_BOOLEAN:
                                    not_count +=1
                            elif line[x][1] in [IDENTIFIER_VARS, LITERAL_NUMBR, LITERAL_NUMBAR, LITERAL_TROOF, LITERAL_YARN]:
                                operand += 1
                            else:
                                if operand == 0:
                                    errors.append("Line " + line_no + ": Invalid operation, waiting for separator")
                                    return 0
                        
                        # consider infinite arity for ALL OF and ANY OF
                        if line[0][0] in ['ALL OF', 'ANY OF']:
                            return 1
                        
                        # check if operation / operand count is still valid
                        if operand > operation:
                            if operand == operation + 3:
                                errors.append("Line " + line_no + ": Invalid operation / operand placements")
                                return 0
                    
                    # for boolean operations
                    if operation_type == KEYWORD_BOOLEAN:
                        operation = operation - not_count

                    # for checking
                    # print(operand)
                    # print(operation)

                    # end of for loop
                    # check if number of operands and operations is valid
                    if (operation+1) == operand:
                        return 1
                    else:
                        errors.append("Line " + line_no + ": Invalid operation syntax detected")
                        return 0

        # ----------------------------------------------------------------------------------------------------------------------------------------------


# test if code syntax of lolcode is valid
def syntax_tester(code_details):

    # list of lists (each index with one line of code)
    code_block = code_details

    # variables for delimiter syntax
    code_delimiter_start = False
    varsec_delimiter_start = False
    func_delimiter_start = False
    condt_delimiter_start = False
    loop_delimiter_start = False

    func_line_start = 0
    condt_line_start = 0
    loop_line_start = 0
    varsec_line_start = 0
    varsec_line_end = 0

    # variables for comment cleaning
    invalid_OBTW = 0
    invalid_TLDR = 0
    searching_TLDR = 0
    searching_TLDR_from_line = 0

    # for checking code details with comments
    # for line in code_block: print(line)
    # print("")

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

    # for checking
    # print("")
    # for line in code_block:
    #     print(line)
    #     print(str(len(line)) + "\n")

    if searching_TLDR == 1 or invalid_TLDR == 1:
        errors.append("Line " + searching_TLDR_from_line + ": Invalid multiline syntax, no TLDR for OBTW")

    else:
        
    # IMPORTANT: We only check the syntax of the whole code if there are no errors
    # in the comments part. If ever there is an OBTW with a missing TLDR, it sees the code
    # block after the OBTW as a whole multiline comment, hence, no code syntax to check

    # Here, we start checking the syntax of the keywords in the code block.
    # We implement a For Loop that checks each code line details and determines whether
    # the succession of keywords are valid or not.

        for line in code_block:

            if len(line) > 1:

                line_no = str(line[0])
                
                # HAI, HOW IZ I not yet found
                if code_delimiter_start == False:

                    # ----------------------------------------------------------------------------------------------------------------------------------------------

                    # only checks valid starting keywords before HAI
                    if line[1][0] in token_list:

                        if line[1][0] in ['HAI', 'KTHXBYE']:

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


                        # invalid starting keyword before HAI
                        else:
                            errors.append("Line " + line_no + ": Invalid syntax, should be inside valid code sections")

                    # invalid lexeme keyword found
                    else: 
                        errors.append("Line " + line_no + ": Invalid syntax, found keyword not in lexemes")

                    # ----------------------------------------------------------------------------------------------------------------------------------------------


                # Main program or Function code block section
                elif (code_delimiter_start == True):

                    # ----------------------------------------------------------------------------------------------------------------------------------------------

                    # Arithmetic Operation
                    if line[1][1] == KEYWORD_ARITHMETIC:
                        check_syntax = line[1:]
                        valid_arithmetic = expression_tester(line_no, check_syntax, KEYWORD_ARITHMETIC)

                        # for checking
                        # if valid_arithmetic == 1: print("Valid!")
                        # else:
                        #     print("Not valid!")
                    
                    # Boolean Operation
                    if line[1][1] == KEYWORD_BOOLEAN:
                        check_syntax = line[1:]
                        valid_arithmetic = expression_tester(line_no, check_syntax, KEYWORD_BOOLEAN)
                    
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

                    # IF-THEN, SWITCH keywords
                    if line[1][0] in ['O RLY?', 'WTF?', 'OIC'] and line[1][1] == DELIMITER_CONDT:
                        if len(line) != 2:
                            errors.append("Line " + line_no + ": Invalid condition delimiter syntax")
                        else:
                            if line[1][0] == 'O RLY?':
                                if condt_delimiter_start == True:
                                    errors.append("Line " + line_no + ": Invalid O RLY? if-else call")
                                else:
                                    condt_delimiter_start = True
                                    condt_line_start = line_no                                
                            elif line[1][0] == 'OIC':
                                if condt_delimiter_start == True:
                                    condt_delimiter_start = False
                                    condt_line_start = 0

                    if line[1][0] in ['YA RLY', 'NO WAI'] and line[1][1] == KEYWROD_CONDT:
                        if len(line) != 2:
                            errors.append("Line " + line_no + ": Invalid YA RLY/NO WAI condition syntax")

                    if line[1][0] == 'OMGWTF' and line[1][1] == KEYWROD_CONDT:
                        if len(line) != 2:
                            errors.append("Line " + line_no + ": Invalid OMGWTF switch-case syntax")
                    
                    if line[1][0] == 'OMG' and line[1][1] == KEYWROD_CONDT:
                        if len(line) == 3:
                            if line[2][1] not in [LITERAL_NOOB, LITERAL_NUMBAR, LITERAL_NUMBR, LITERAL_TROOF, LITERAL_YARN]:
                                errors.append("Line " + line_no + ": Waiting for literal condition")
                        else:
                            errors.append("Line " + line_no + ": Invalid OMG switch-case syntax")

                    # ----------------------------------------------------------------------------------------------------------------------------------------------

                    # keywords for varident operations
                    if line[1][1] == IDENTIFIER_VARS:

                        # valid
                        if len(line) == 2: None
                        elif len(line) >= 4:

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

                    # MAEK
                    if line[1][0] == 'MAEK' and line[1][1] == KEYWORD_TYPECAST:
                        if len(line) == 4:
                            if line[2][1] != IDENTIFIER_VARS or line[3][1] != LITERAL:
                                errors.append("Line " + line_no + ": Invalid typecasting parameters")
                        elif len(line) == 5:
                            if line[2][1] != IDENTIFIER_VARS or line[3][0] != 'A' or line[4][1] != LITERAL:
                                errors.append("Line " + line_no + ": Invalid typecasting parameters")
                        else:
                            errors.append("Line " + line_no + ": Invalid MAEK usage / parameters")
                    
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

                    # GTFO
                    if line[1][0] == 'GTFO' and line[1][1] == KEYWROD_CONDT:
                        if len(line) != 2:
                            errors.append("Line " + line_no + ": Invalid GTFO syntax")

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

                                # NOTE: Insert condition for expressions

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

    # check if flow-control statement sections are valid
    if condt_delimiter_start == True:
        errors.append("Line " + condt_line_start + ": Invalid O RLY? syntax, valid OIC keyword not found")

    # check if variable section is valid
    if varsec_delimiter_start == True and invalid_OBTW == 0:
        errors.append("Line " + varsec_line_start + ": Invalid WAZZUP syntax, BUHBYE keyword not found")
    elif varsec_delimiter_start == True and invalid_OBTW == 1:
        errors.append("Line " + varsec_line_start + ": Invalid BUHBYE syntax for WAZZUP keyword")


    # IMPORTANT: Here, we pass the values of the cleaned code block and if the code is valid
    # Returns 0 if syntax errors exist
    # Returns 1 if there are no syntax errors

    # for checking
    for line in code_block:
        print(line)

    if len(errors) > 0:
        return [code_block, 0]
    elif len(errors) == 0:
        return [code_block, 1]
    # error trap
    else: return [code_block, 0]


# testing 

sample = """HAI


KTHXBYE"""

print("")
test = lexical_tester(sample)
syntax_tester(test)
print("")

if len(errors) > 0:
    for error in errors:
        print(error)
    print("")
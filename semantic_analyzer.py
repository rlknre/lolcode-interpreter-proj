import re

# import lexical analyzer function
from lexical_analyzer import lexical_tester

# import syntax analyzer function
from syntax_analyzer import syntax_tester

# import keyword classifiers
from keywords import DELIMITER_CODE, DELIMITER_STR, DELIMITER_VAR, DELIMITER_CONDT, DELIMITER_END
from keywords import IDENTIFIER_VARS, IDENTIFIER_FUNC, IDENTIFIER_LOOP
from keywords import VAR_DECLARE, VAR_ASSIGN

from keywords import KEYWORD_COMMENT
from keywords import KEYWORD_COMPARE
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

# import library
import tkinter as tk
import math

from lexical_analyzer import detect_lexemes


# ----------------------------------------------------------------------------------------------------------------------------------------------

def perform_arithmetic(symbol_names, symbol_vals, symbol_types, line, line_number):
        
    result = 0
    to_numbar = 0

    # check if there is a lost lexeme
    for x in range(0, len(line)):
        if line[x][1] != KEYWORD_ARITHMETIC:
            if line[x][1] not in [IDENTIFIER_VARS, LITERAL_NUMBR, LITERAL_NUMBAR, LITERAL_TROOF, LITERAL_YARN]:
                if line[x][0] != 'AN':
                    error_message = ("Line " + str(line_number) + ": Invalid value found in arithmetic expression")
                    return[0, error_message]

    # check if symbols exist
    for x in range(0, len(line)):
        if line[x][1] == IDENTIFIER_VARS:
            if line[x][0] not in symbol_names:
                error_message = ("Line " + str(line_number) + ": Invalid variable name found in arithmetic expression")
                return[0, error_message]
    
    # check each operand if they are valid (for yarns and vars)
    for x in range(0, len(line)):
        if line[x][1] in [IDENTIFIER_VARS, LITERAL_NUMBR, LITERAL_NUMBAR, LITERAL_TROOF, LITERAL_YARN]:
            
            # check if variable is valid
            if line[x][1] == IDENTIFIER_VARS:
                # retrieve type of varident
                var_index = symbol_names.index(line[x][0])
                varident_type = symbol_types[var_index]

                # Checker for NUMBAR
                if varident_type == LITERAL_NUMBAR:
                    to_numbar = 1

                # check if YARN / TROOF is valid
                if varident_type not in [LITERAL_NUMBR, LITERAL_NUMBAR]:
                    # NOOBs invalid
                    if varident_type == LITERAL_NOOB:
                        error_message = ("Line " + str(line_number) + ": NOOBs are invalid in arithmetic expressions")
                        return[0, error_message]
                    # YARN
                    elif varident_type == LITERAL_YARN:
                        # check if valid NUMBR / NUMBAR / TROOF

                        varident_details = detect_lexemes(symbol_vals[var_index])
                        # returns [lexeme_token, lexeme_classification]
                        varident_class = varident_details[1]

                        if varident_class not in [LITERAL_NUMBR, LITERAL_NUMBAR, LITERAL_TROOF]:
                            error_message = ("Line " + str(line_number) + ": Invalid operand type found in expression")
                            return[0, error_message]
                        else:
                            if varident_class == LITERAL_NUMBAR:
                                to_numbar = 1
            # update checker for NUMBAR
            elif line[x][1] == LITERAL_NUMBAR:
                to_numbar = 1

    # For implicit typecasting, check if values should be float or int
    new_class = LITERAL_NUMBR
    if to_numbar == 1:
        new_class = LITERAL_NUMBAR

    # Implicit Typecasting
    for x in range(0, len(line)):

        # Varidents
        if line[x][1] == IDENTIFIER_VARS:
            # retrieves index of varident as well in symbols table
            var_index = symbol_names.index(line[x][0])
            varident_value = symbol_vals[var_index]
            varident_type = symbol_types[var_index]

            # YARN to -
            if varident_type == LITERAL_YARN:
                varident_details = detect_lexemes(symbol_vals[var_index])
                # returns [lexeme_token, lexeme_classification]
                varident_value = varident_details[0]
                varident_class = varident_details[1]

                # YARN to NUMBR
                if varident_class == LITERAL_NUMBR:
                    if new_class == LITERAL_NUMBAR:
                        symbol_vals[var_index] = float(varident_value)
                    else:
                        symbol_vals[var_index] = varident_value
                    symbol_types[var_index] = new_class
                # YARN TO NUMBAR
                elif varident_class == LITERAL_NUMBAR:
                    symbol_vals[var_index] = varident_value
                    symbol_types[var_index] = new_class
                # YARN to TROOF to NUMBR / NUMBAR
                elif varident_class == LITERAL_TROOF:
                    if varident_value == 'WIN':
                        if new_class == LITERAL_NUMBR:
                            symbol_vals[var_index] = 1
                            symbol_types[var_index] = LITERAL_NUMBR
                        else:
                            symbol_vals[var_index] = 1.0
                            symbol_types[var_index] = LITERAL_NUMBAR
                    elif varident_value == 'FAIL':
                        if new_class == LITERAL_NUMBR:
                            symbol_vals[var_index] = 0
                            symbol_types[var_index] = LITERAL_NUMBR
                        else:
                            symbol_vals[var_index] = 0.0
                            symbol_types[var_index] = LITERAL_NUMBAR

            # TROOF to -
            elif varident_type == LITERAL_TROOF:
                if varident_value == 'WIN':
                    if new_class == LITERAL_NUMBR:
                        symbol_vals[var_index] = 1
                        symbol_types[var_index] = LITERAL_NUMBR
                    else:
                        symbol_vals[var_index] = 1.0
                        symbol_types[var_index] = LITERAL_NUMBAR
                elif varident_value == 'FAIL':
                    if new_class == LITERAL_NUMBR:
                        symbol_vals[var_index] = 0
                        symbol_types[var_index] = LITERAL_NUMBR
                    else:
                        symbol_vals[var_index] = 0.0
                        symbol_types[var_index] = LITERAL_NUMBAR                

            # NUMBR to -
            elif varident_type == LITERAL_NUMBR:
                if to_numbar == 1:
                    symbol_vals[var_index] = float(symbol_vals[var_index])
                    symbol_types[var_index] = LITERAL_NUMBAR

        # end of loop for varident typecasting

        # NUMBRs
        elif line[x][1] == LITERAL_NUMBR:
            if to_numbar == 1:
                line[x][0] = float(line[x][0])
                line[x][1] = LITERAL_NUMBAR

        # TROOFs
        elif line[x][1] == LITERAL_TROOF:
            if to_numbar == 1:
                if line[x][0] == 'WIN':
                    line[x][0] = 1.0
                elif line[x][0] == 'FAIL':
                    line[x][0] = 0.0
                line[x][1] = LITERAL_NUMBAR
            else:
                if line[x][0] == 'WIN':
                    line[x][0] = 1
                elif line[x][0] == 'FAIL':
                    line[x][0] = 0
                line[x][1] = LITERAL_NUMBR

    # end of Implicit Typecasting loop

    # initialize the computing list with the code line
    compute_list = line

    # perform arithmetic operation
    counter = len(compute_list)
    while counter != 1:

        # computing values
        testing_list = []
        expecting_seperator = 0
        expecting_operand = 0

        # for clearing
        index_of_operation = 0

        # loop through line and find one operation to perform
        for x in range(0, len(compute_list)):

            # Operation
            if compute_list[x][1] == KEYWORD_ARITHMETIC:
                if expecting_operand == 1:
                    expecting_operand = 0
                    index_of_operation = 0
                    testing_list.clear()
                elif expecting_seperator == 1:
                    expecting_seperator = 0
                    index_of_operation = 0
                    testing_list.clear()
                # update values
                testing_list.append(compute_list[x])
                expecting_operand = 1
                index_of_operation = x
            
            # AN
            elif compute_list[x][0] == 'AN':
                if expecting_seperator == 1:
                    expecting_operand = 1
                    expecting_seperator = 0
                else:
                    expecting_operand = 0
                    expecting_seperator = 0
                    testing_list.clear()
            
            # Operand
            elif compute_list[x][1] in [IDENTIFIER_VARS, LITERAL_NUMBR, LITERAL_NUMBAR, LITERAL_TROOF, LITERAL_YARN]:
                if expecting_operand == 1:
                    expecting_operand = 0
                    expecting_seperator = 1

                    if compute_list[x][1] == IDENTIFIER_VARS:
                        # retrieve value of varident
                        var_index = symbol_names.index(compute_list[x][0])
                        testing_list.append([symbol_vals[var_index], symbol_types[var_index]])
                    else:
                        testing_list.append(compute_list[x])

                    if len(testing_list) == 3:
                        break
                else:
                    expecting_operand = 0
                    expecting_seperator = 0
                    testing_list.clear()
        
        # perform operation
        answer = 0
        if len(testing_list) == 3:

            # print(compute_list)

            # values from testing list
            perform_operation = testing_list[0][0]
            if to_numbar == 1:
                value1 = float(testing_list[1][0])
                value2 = float(testing_list[2][0])
            else:
                value1 = int(testing_list[1][0])
                value2 = int(testing_list[2][0])                
            
            # perform operation here
            if perform_operation == 'SUM OF':
                answer = value1 + value2
            elif perform_operation == 'DIFF OF':
                answer = value1 - value2
            elif perform_operation == 'PRODUKT OF':
                answer = value1 * value2
            elif perform_operation == 'QUOSHUNT OF':
                if to_numbar == 1:
                    answer = value1 / value2    # float division
                else:
                    answer = value1 // value2   # int division
            elif perform_operation == 'MOD OF':
                answer = value1 % value2
            elif perform_operation == 'BIGGR OF':
                answer = max(value1, value2)
            elif perform_operation == 'SMALLR OF':
                answer = min(value1, value2)
            
            # insert answer to computing list and update values
            if to_numbar == 1: 
                compute_list[index_of_operation] = [answer, LITERAL_NUMBR]
            else: 
                compute_list[index_of_operation] = [answer, LITERAL_NUMBAR]
            # remove used values
            first_half = compute_list[:index_of_operation+1]
            second_half = compute_list[index_of_operation+4 :]
            compute_list = first_half + second_half

        counter = len(compute_list)
        if counter == 1:
            print(str(compute_list[0][0]))
            # break
            return[1, compute_list[0][0], new_class]
        # print(compute_list)

        # end of for loop for retrieving testing list


# ----------------------------------------------------------------------------------------------------------------------------------------------

# IMPORTANT: Does not perform ALL OF and ANY OF

def perform_boolean(symbol_names, symbol_vals, symbol_types, line, line_number):
        
    result = 0

    # check if there is a lost lexeme
    for x in range(0, len(line)):
        if line[x][1] != KEYWORD_BOOLEAN:
            if line[x][1] not in [IDENTIFIER_VARS, LITERAL_NUMBR, LITERAL_NUMBAR, LITERAL_TROOF, LITERAL_YARN, LITERAL_NOOB]:
                if line[x][0] != 'AN':
                    error_message = ("Line " + str(line_number) + ": Invalid value found in boolean expression")
                    return[0, error_message]

    # check if symbols exist
    for x in range(0, len(line)):
        if line[x][1] == IDENTIFIER_VARS:
            if line[x][0] not in symbol_names:
                error_message = ("Line " + str(line_number) + ": Invalid variable name found in boolean expression")
                return[0, error_message]
    
    # check each operand if they are valid (for yarns and vars)
    for x in range(0, len(line)):
        if line[x][1] in [IDENTIFIER_VARS, LITERAL_NUMBR, LITERAL_NUMBAR, LITERAL_TROOF, LITERAL_YARN, LITERAL_NOOB]:
            
            # check if variable is valid
            if line[x][1] == IDENTIFIER_VARS:
                # retrieve type of varident
                var_index = symbol_names.index(line[x][0])
                varident_type = symbol_types[var_index]

                # check if YARN is valid
                if varident_type not in [LITERAL_TROOF, LITERAL_NOOB]:
                    # YARN
                    if varident_type == LITERAL_YARN:
                        # check if valid NUMBR / NUMBAR / TROOF

                        varident_details = detect_lexemes(symbol_vals[var_index])
                        # returns [lexeme_token, lexeme_classification]
                        varident_value = varident_details[0]
                        varident_class = varident_details[1]

                        if varident_class != LITERAL_TROOF:
                            if varident_class != LITERAL_YARN:
                                # check if valid NUMBAR / NUMBR to TROOF
                                if varident_class == LITERAL_NUMBAR or varident_class == LITERAL_NUMBR:
                                    varident_value = float(varident_value)
                                    if varident_value != 1.0:
                                        if varident_value != 0.0:
                                            error_message = ("Line " + str(line_number) + ": Invalid operand type found in expression (1) ")
                                            return[0, error_message]
                                elif varident_class == LITERAL_NUMBR:
                                    varident_value = int(varident_value)
                                    if varident_value != 1:
                                        if varident_value != 0:
                                            error_message = ("Line " + str(line_number) + ": Invalid operand type found in expression (1) ")
                                            return[0, error_message]

                    # NUMBR / NUMBAR
                    elif varident_type == LITERAL_NUMBR or varident_type == LITERAL_NUMBAR:
                        varident_val = symbol_vals[var_index]
                        if varident_val != 1:
                            if varident_val != 1.0:
                                if varident_val != 0:
                                    if varident_val != 0.0:
                                        error_message = ("Line " + str(line_number) + ": Invalid operand type found in expression (2) ")
                                        return[0, error_message]
                    else:
                        error_message = ("Line " + str(line_number) + ": Invalid operand type found in expression (3)")
                        return[0, error_message]

    # Implicit Typecasting
    for x in range(0, len(line)):

        # Varidents
        if line[x][1] == IDENTIFIER_VARS:
            # retrieves index of varident as well in symbols table
            var_index = symbol_names.index(line[x][0])
            varident_value = symbol_vals[var_index]
            varident_type = symbol_types[var_index]

            # NOOB to TROOF
            if varident_type == LITERAL_NOOB:
                symbol_vals[var_index] = 'FAIL'
                symbol_types[var_index] = LITERAL_TROOF

            # YARN to -
            elif varident_type == LITERAL_YARN:
                varident_details = detect_lexemes(symbol_vals[var_index])
                # returns [lexeme_token, lexeme_classification]
                varident_value = varident_details[0]
                varident_class = varident_details[1]

                # YARN (NUMBR) - TROOF
                if varident_class == LITERAL_NUMBR:
                    varident_value = int(varident_value)
                    if varident_value == 1:
                        symbol_vals[var_index] = 'WIN'
                    elif varident_value == 0:
                        symbol_vals[var_index] = 'FAIL'
                    symbol_types[var_index] = LITERAL_TROOF
                # YARN (NUMBAR) - TROOF
                elif varident_class == LITERAL_NUMBAR:
                    varident_value = float(varident_value)
                    if varident_value == 1.0:
                        symbol_vals[var_index] = 'WIN'
                    elif varident_value == 0.0:
                        symbol_vals[var_index] = 'FAIL'
                    symbol_types[var_index] = LITERAL_TROOF
                # YARN (WIN FAIL)
                elif varident_value == 'WIN':
                    symbol_vals[var_index] = 'WIN'
                    symbol_types[var_index] = LITERAL_TROOF
                elif varident_value == 'FAIL':
                    symbol_vals[var_index] = 'FAIL'
                    symbol_types[var_index] = LITERAL_TROOF

            # NUMBR to TROOF           
            elif varident_type == LITERAL_NUMBR:
                varident_value = int(varident_value) 
                if varident_value == 1:
                    symbol_vals[var_index] = 'WIN'
                elif varident_value == 0:
                    symbol_vals[var_index] = 'FAIL'
                symbol_types[var_index] = LITERAL_TROOF

            # NUMBAR to TROOF
            elif varident_type == LITERAL_NUMBAR:
                varident_value = float(varident_value) 
                if varident_value == 1.0:
                    symbol_vals[var_index] = 'WIN'
                elif varident_value == 0.0:
                    symbol_vals[var_index] = 'FAIL'
                symbol_types[var_index] = LITERAL_TROOF

        # end of loop for varident typecasting

        # YARNs
        elif line[x][1] == LITERAL_YARN:
            varident_details = detect_lexemes(str(line[x][0]))
            # returns [lexeme_token, lexeme_classification]
            varident_value = varident_details[0]
            varident_class = varident_details[1]

            # YARN (NUMBR / NUMBAR) - TROOF
            if varident_class == LITERAL_NUMBR or varident_class == LITERAL_NUMBAR:
                varident_value = int(varident_value)
                if varident_value == 1:
                    symbol_vals[var_index] = 'WIN'
                elif varident_value == 0:
                    symbol_vals[var_index] = 'FAIL'
                    symbol_types[var_index] = LITERAL_TROOF
            # YARN (WIN FAIL)
            elif varident_value == 'WIN':
                symbol_vals[var_index] = 'WIN'
                symbol_types[var_index] = LITERAL_TROOF
            elif varident_value == 'FAIL':
                symbol_vals[var_index] = 'FAIL'
                symbol_types[var_index] = LITERAL_TROOF
            # NOOB
            elif varident_value == '':
                symbol_vals[var_index] = 'FAIL'
                symbol_types[var_index] = LITERAL_TROOF
        
        # NUMBRs
        elif line[x][1] == LITERAL_NUMBR:
            varident_value = int(line[x][0]) 
            if varident_value == 1:
                line[x][0] = 'WIN'
            elif varident_value == 0:
                line[x][0] = 'FAIL'
            line[x][1] = LITERAL_TROOF

        # NUMBARs
        elif line[x][1] == LITERAL_NUMBAR:
            varident_value = float(line[x][0]) 
            if varident_value == 1.0:
                line[x][0] = 'WIN'
            elif varident_value == 0.0:
                line[x][0] = 'FAIL'
            line[x][1] = LITERAL_TROOF        

    # end of Implicit Typecasting loop

    # initialize the computing list with the code line
    compute_list = line

    # perform boolan operation
    counter = len(compute_list)
    while counter != 1:

        # computing values
        testing_list = []
        expecting_seperator = 0
        expecting_operand = 0
        not_operator_found = 0

        # for clearing
        index_of_operation = 0

        # loop through line and find one operation to perform
        for x in range(0, len(compute_list)):

            # Operation
            if compute_list[x][1] == KEYWORD_BOOLEAN:
                if expecting_operand == 1:
                    expecting_operand = 0
                    index_of_operation = 0
                    testing_list.clear()
                elif expecting_seperator == 1:
                    expecting_seperator = 0
                    index_of_operation = 0
                    testing_list.clear()
                # update values
                testing_list.append(compute_list[x])
                expecting_operand = 1
                index_of_operation = x
                # check if NOT operator
                if compute_list[x][0] == 'NOT':
                    if not_operator_found == 0:
                        not_operator_found = 1
                    else:
                        not_operator_found = 1
                        testing_list.clear()
                        testing_list.append(compute_list[x])
            
            # AN
            elif compute_list[x][0] == 'AN':
                if expecting_seperator == 1:
                    expecting_operand = 1
                    expecting_seperator = 0
                else:
                    not_operator_found = 0
                    expecting_operand = 0
                    expecting_seperator = 0
                    testing_list.clear()
            
            # Operand
            elif compute_list[x][1] in [IDENTIFIER_VARS, LITERAL_NUMBR, LITERAL_NUMBAR, LITERAL_TROOF, LITERAL_YARN]:
                if expecting_operand == 1:
                    expecting_operand = 0
                    expecting_seperator = 1

                    if compute_list[x][1] == IDENTIFIER_VARS:
                        # retrieve value of varident
                        var_index = symbol_names.index(compute_list[x][0])
                        testing_list.append([symbol_vals[var_index], symbol_types[var_index]])
                    else:
                        testing_list.append(compute_list[x])

                    # non NOT
                    if len(testing_list) == 3: 
                        break
                    # NOT
                    if not_operator_found == 1: 
                        break
                else:
                    not_operator_found = 0
                    expecting_operand = 0
                    expecting_seperator = 0
                    testing_list.clear()
        
        # print(testing_list)
        # break

        # perform operation
        answer = 0
        if len(testing_list) == 3:

            # print(compute_list)

            # Other BOOLS
            if testing_list[0][0] != 'NOT':
                # values from testing list
                perform_operation = testing_list[0][0]     
                value1 = testing_list[1][0]
                value2 = testing_list[2][0]
                
                # AND
                if perform_operation == 'BOTH OF':
                    if value1 == value2:
                        answer = 'WIN'
                    else:
                        answer = 'FAIL'
                # OR
                elif perform_operation == 'EITHER OF':
                    if value1 == 'WIN' or value2 == 'WIN':
                        answer = 'WIN'
                    else:
                        answer = 'FAIL'
                # XOR
                elif perform_operation == 'WON OF':
                    if value1 == value2:
                        answer = 'FAIL'
                    else:
                        answer = 'WIN'

                # insert answer to computing list and update values
                compute_list[index_of_operation] = [answer, LITERAL_TROOF]

                # remove used values
                first_half = compute_list[:index_of_operation+1]
                second_half = compute_list[index_of_operation+4 :]
                compute_list = first_half + second_half
        
        # NOT operation 
        elif len(testing_list) == 2: 
            
            if testing_list[0][0] == 'NOT':
                answer = testing_list[1][0]
                if answer == 'WIN':
                    answer = 'FAIL'
                elif answer == 'FAIL':
                    answer = 'WIN'
                # insert answer to computing list and update values
                compute_list[index_of_operation] = [answer, LITERAL_TROOF]
                
                # remove used values
                first_half = compute_list[:index_of_operation+1]
                second_half = compute_list[index_of_operation+2 :]
                compute_list = first_half + second_half
        
        # end of boolean computation

        counter = len(compute_list)
        if counter == 1:
            # print(str(compute_list[0][0]))
            # break
            return[1, compute_list[0][0]]
        # print(compute_list)

        # end of for loop for retrieving testing list


# ----------------------------------------------------------------------------------------------------------------------------------------------

def perform_comparison():
    None


# ----------------------------------------------------------------------------------------------------------------------------------------------

# perform the code if syntax is valid

def semantic_perform(code_details):

    # errors
    errors = []

    # symbol table 
    symbol_table_identifiers = []
    symbol_table_values = []
    symbol_table_type = []
    lines_to_print = ''

    symbol_table_identifiers.append('IT')
    symbol_table_values.append('NOOB')
    symbol_table_type.append(LITERAL_NOOB)

    code_block = code_details

    for line in code_block:

        line_no = str(line[0])

        if len(line) > 1:

            # ----------------------------------------------------------------------------------------------------------------------------------------------

            # Arithmetic Operation
            if line[1][1] == KEYWORD_ARITHMETIC:
                # call the perform_arithmetic() func and check if valid
                a_expr = line[1:]
                a_perform = perform_arithmetic(symbol_table_identifiers, symbol_table_values, symbol_table_type, a_expr, line_no)

                # if invalid, returns [0, error message]
                # if valid, returns [1, result, type of result]

                if len(a_perform) == 2:
                    # error
                    if a_perform[0] == 0:
                        errors.append(a_perform[1])
                elif len(a_perform) == 3:
                    # valid
                    if a_perform[0] == 1:
                        answer_type = a_perform[2]
                        # NUMBAR
                        if answer_type == LITERAL_NUMBAR:
                            answer_result = float(a_perform[1])
                            symbol_table_values[0] = answer_result
                            symbol_table_type[0] = LITERAL_NUMBAR
                        # NUMBR
                        elif answer_type == LITERAL_NUMBR:
                            answer_result = int(a_perform[1])
                            symbol_table_values[0] = answer_result
                            symbol_table_type[0] = LITERAL_NUMBR

            # ----------------------------------------------------------------------------------------------------------------------------------------------

            # Boolean Operation
            if line[1][1] == KEYWORD_BOOLEAN:
                b_expr = line[1:]
                b_perform = perform_boolean(symbol_table_identifiers, symbol_table_values, symbol_table_type, b_expr, line_no)

                # if invalid, returns [0, error message]
                # if valid, returns [1, result]

                if b_perform[0] == 0:
                    errors.append(b_perform[1])
                elif b_perform[0] == 1:
                    # insert to IT variable
                    symbol_table_values[0] = b_perform[1]
                    symbol_table_type[0] = LITERAL_TROOF
                    print(b_perform[1])

            # ----------------------------------------------------------------------------------------------------------------------------------------------

            # Comparison Operation


            # ----------------------------------------------------------------------------------------------------------------------------------------------

            # I HAS A
            if line[1][0] == "I HAS A" and line[1][1] == VAR_DECLARE:

                # uninitialized variable
                if len(line) == 3:
                    symbol_table_identifiers.append(line[2][0])
                    symbol_table_values.append('NOOB')
                    symbol_table_type.append(LITERAL_NOOB)

                # initialized variable
                elif len(line) == 5:

                    # NOTE: add condition where it overwrites the value if variable already exists

                    symbol_table_identifiers.append(line[2][0])

                    if line[4][1] == LITERAL_YARN:
                        symbol_table_values.append(line[4][0])
                        symbol_table_type.append(LITERAL_YARN)
                    
                    elif line[4][1] == LITERAL_TROOF:
                        symbol_table_values.append(line[4][0])
                        symbol_table_type.append(LITERAL_TROOF)
                    
                    # convert values to its corresponding type
                    elif line[4][1] == LITERAL_NUMBR:
                        symbol_table_values.append(int(line[4][0]))
                        symbol_table_type.append(LITERAL_NUMBR)
                    
                    elif line[4][1] == LITERAL_NUMBAR:
                        symbol_table_values.append(float(line[4][0]))
                        symbol_table_type.append(LITERAL_NUMBAR)
                
                # expressions
                elif len(line) > 5:

                    # arithmetic
                    if line[4][1] == KEYWORD_ARITHMETIC:
                        testing_list = line[4:]
                        a_perform = perform_arithmetic(symbol_table_identifiers, symbol_table_values, symbol_table_type, testing_list, line_no)

                        # if invalid, returns [0, error message]
                        # if valid, returns [1, result, type of result]
                        if len(a_perform) == 2:
                            # error
                            if a_perform[0] == 0:
                                errors.append(a_perform[1])
                        elif len(a_perform) == 3:
                                # valid
                            if a_perform[0] == 1:
                                answer_type = a_perform[2]
                                # NUMBAR
                                if answer_type == LITERAL_NUMBAR:
                                    answer_result = float(a_perform[1])
                                    # add to symbols table
                                    symbol_table_identifiers.append(line[2][0])
                                    symbol_table_values.append(answer_result)
                                    symbol_table_type.append(LITERAL_NUMBAR)
                                # NUMBR
                                elif answer_type == LITERAL_NUMBR:
                                    answer_result = int(a_perform[1])
                                    # add to symbols table
                                    symbol_table_identifiers.append(line[2][0])
                                    symbol_table_values.append(answer_result)
                                    symbol_table_type.append(LITERAL_NUMBR)

                    # boolean
                    elif line[4][1] == KEYWORD_BOOLEAN:
                        testing_list = line[4:]
                        b_perform = perform_boolean(symbol_table_identifiers, symbol_table_values, symbol_table_type, testing_list, line_no)

                        # if invalid, returns [0, error message]
                        # if valid, returns [1, result]

                        if b_perform[0] == 0:
                            errors.append(b_perform[1])
                        elif b_perform[0] == 1:
                            # insert to IT variable
                            symbol_table_values[0] = b_perform[1]
                            symbol_table_type[0] = LITERAL_TROOF
                                        
            # ----------------------------------------------------------------------------------------------------------------------------------------------

            # VISIBLE
            if line[1][0] == 'VISIBLE' and line[1][1] == KEYWORD_PRINT:
                # only one to print
                if len(line) <= 3:
                    if line[2][1] == LITERAL_YARN:
                        # use the IT variable 
                        symbol_table_values[0] = ''
                        symbol_table_values[0] = (line[2][0])
                        symbol_table_type[0] = LITERAL_YARN

                        lines_to_print += symbol_table_values[0] + '\n'

                    else:
                        if line[2][0] in symbol_table_identifiers:
                            var_index = symbol_table_identifiers.index(line[2][0])
                            
                            symbol_table_values[0] = ''
                            it_var = str(symbol_table_values[var_index])
                            symbol_table_values[0] = it_var
                            symbol_table_type[0] = LITERAL_YARN

                            lines_to_print += symbol_table_values[0] + '\n'
                        
                # multiple values
                else:
                    # VISIBLE (not SMOOSH) 
                    if line[2][1] != 'SMOOSH':
                        for_printing = ''
                        testing_list = []           # for expressions
                        expected_operation = ''     # for operation type
                        expect_expr_token = 0       # check for expression tokens
                        expect_concat = 0           # check for concat keyword

                        # expressions
                        for x in range(2, len(line)):

                            # Operations
                            if line[x][1] in [KEYWORD_ARITHMETIC, KEYWORD_BOOLEAN, KEYWORD_COMPARE]:
                                # start of testing list, update checkers
                                if expect_expr_token == 0:
                                    expected_operation = line[x][1]
                                    expect_expr_token = 1
                                    expect_concat = 1
                                # always append value
                                testing_list.append(line[x])
                                        
                            # AN
                            if line[x][0] == 'AN':
                                if expect_expr_token == 1:
                                    testing_list.append(line[x])
                                        
                            # Operands
                            if line[x][1] in [IDENTIFIER_VARS, LITERAL_NUMBAR, LITERAL_NUMBR, LITERAL_TROOF, LITERAL_TROOF, LITERAL_YARN]:
                                # expressions
                                if expect_expr_token == 1:
                                    testing_list.append(line[x])
                                # non expressions
                                elif expect_expr_token == 0:
                                    if line[x][1] == IDENTIFIER_VARS:
                                        if line[x][0] in symbol_table_identifiers:
                                            var_index = symbol_table_identifiers.index(line[x][0])
                                            val_varid = str(symbol_table_values[var_index])
                                            for_printing = ''.join([for_printing, val_varid])
                                        else:
                                            errors.append("Line " + line_no + ": Invalid variable call, does not exist")
                                    else:
                                        for_printing = ''.join([for_printing, str(line[x][0])])

                            # MKAY
                            if line[x][0] == 'MKAY' and line[x][1] == DELIMITER_END:
                                if expect_expr_token == 1:
                                    testing_list.append(line[x])

                            # Concat
                            if line[x][1] == KEYWORD_CONCAT:
                                # expressions
                                if expect_expr_token == 1:

                                    # Arithmetic Operations
                                    if testing_list[0][1] == KEYWORD_ARITHMETIC:
                                        a_perform = perform_arithmetic(symbol_table_identifiers, symbol_table_values, symbol_table_type, testing_list, line_no)
                                        testing_list = []

                                        # if invalid, returns [0, error message]
                                        # if valid, returns [1, result, type of result]
                                        if len(a_perform) == 2:
                                            # error
                                            if a_perform[0] == 0:
                                                errors.append(a_perform[1])
                                        elif len(a_perform) == 3:
                                            # valid
                                            if a_perform[0] == 1:
                                                answer_type = a_perform[2]
                                                # NUMBAR
                                                if answer_type == LITERAL_NUMBAR:
                                                    answer_result = float(a_perform[1])
                                                    symbol_table_values[0] = answer_result
                                                    symbol_table_type[0] = LITERAL_NUMBAR
                                                    for_printing = ''.join([for_printing, str(answer_result)])
                                                # NUMBR
                                                elif answer_type == LITERAL_NUMBR:
                                                    answer_result = int(a_perform[1])
                                                    symbol_table_values[0] = answer_result
                                                    symbol_table_type[0] = LITERAL_NUMBR
                                                    for_printing = ''.join([for_printing, str(answer_result)])
                                            
                                        expected_operation = ''
                                        expect_expr_token = 0
                                        expect_concat = 0

                                    # Boolean Operations
                                    elif testing_list[0][1] == KEYWORD_BOOLEAN:
                                        # Boolean Operation
                                        b_perform = perform_boolean(symbol_table_identifiers, symbol_table_values, symbol_table_type, testing_list, line_no)
                                        testing_list = []
                                        # if invalid, returns [0, error message]
                                        # if valid, returns [1, result]

                                        if b_perform[0] == 0:
                                            errors.append(b_perform[1])
                                        elif b_perform[0] == 1:
                                            # insert to IT variable
                                            symbol_table_values[0] = b_perform[1]
                                            symbol_table_type[0] = LITERAL_TROOF
                                            for_printing = ''.join([for_printing, str(b_perform[1])])
                                        
                                        expected_operation = ''
                                        expect_expr_token = 0
                                        expect_concat = 0

                                # non expressions
                                else:
                                    expect_concat = 0

                        # for single expressions
                        if expect_expr_token == 1:

                            # Arithmetic Operations
                            if testing_list[0][1] == KEYWORD_ARITHMETIC:
                                a_perform = perform_arithmetic(symbol_table_identifiers, symbol_table_values, symbol_table_type, testing_list, line_no)
                                testing_list = []
                                
                                # if invalid, returns [0, error message]
                                # if valid, returns [1, result, type of result]
                                if len(a_perform) == 2:
                                    # error
                                    if a_perform[0] == 0:
                                        errors.append(a_perform[1])
                                elif len(a_perform) == 3:
                                    # valid
                                    if a_perform[0] == 1:
                                        answer_type = a_perform[2]
                                        # NUMBAR
                                        if answer_type == LITERAL_NUMBAR:
                                            answer_result = float(a_perform[1])
                                            symbol_table_values[0] = answer_result
                                            symbol_table_type[0] = LITERAL_NUMBAR
                                            for_printing = ''.join([for_printing, str(answer_result)])
                                        # NUMBR
                                        elif answer_type == LITERAL_NUMBR:
                                            answer_result = int(a_perform[1])
                                            symbol_table_values[0] = answer_result
                                            symbol_table_type[0] = LITERAL_NUMBR
                                            for_printing = ''.join([for_printing, str(answer_result)])

                            # Boolean Operations
                            elif testing_list[0][1] == KEYWORD_BOOLEAN:
                                # Boolean Operation
                                b_perform = perform_boolean(symbol_table_identifiers, symbol_table_values, symbol_table_type, testing_list, line_no)
                                testing_list = []
                                # if invalid, returns [0, error message]
                                # if valid, returns [1, result]

                                if b_perform[0] == 0:
                                    errors.append(b_perform[1])
                                elif b_perform[0] == 1:
                                    # insert to IT variable
                                    symbol_table_values[0] = b_perform[1]
                                    symbol_table_type[0] = LITERAL_TROOF
                                    for_printing = ''.join([for_printing, str(b_perform[1])])

                        # append to list for printing values
                        if for_printing != '':
                            lines_to_print += (for_printing) + '\n'
                            # also update IT variable
                            symbol_table_values[0] = for_printing
                            symbol_table_type[0] = LITERAL_YARN

                    # end of VISIBLE (non SMOOSH)

                    # VISIBLE SMOOSH (expressions not counted)
                    elif line[2][0] == 'SMOOSH':
                        # should place concatenated string to IT variable
                        it_var = ''
                        valid_concat = 1
                        expecting_seperator = 0

                        # retrieve smoosh expression for printing
                        smoosh_print = line[2:]

                        for x in range(1, len(smoosh_print)):
                            # YARN
                            if smoosh_print[x][1] == LITERAL_YARN:
                                if expecting_seperator == 0:
                                    expecting_seperator = 1
                                    it_var = ''.join([it_var, (smoosh_print[x][0])])
                                else:
                                    valid_concat = 0
                                    break
                            else:
                                # Varident
                                if smoosh_print[x][1] == IDENTIFIER_VARS:
                                    if smoosh_print[x][0] in symbol_table_identifiers:
                                        expecting_seperator = 1
                                        var_index = symbol_table_identifiers.index(smoosh_print[x][0])
                                        to_yarn = symbol_table_values[var_index]

                                        # typecast
                                        if symbol_table_type[var_index] != LITERAL_YARN:
                                            to_yarn = str(symbol_table_values[var_index])

                                            # implicit recast of variables
                                            symbol_table_values[var_index] = to_yarn
                                            symbol_table_type[var_index] = LITERAL_YARN
                                        it_var = ''.join([it_var, to_yarn])                                            
                                    else:
                                        valid_concat = 0
                                        break
                                # Other values
                                elif smoosh_print[x][1] in [LITERAL_NOOB, LITERAL_NUMBAR, LITERAL_NUMBR, LITERAL_NUMBAR]:
                                    if expecting_seperator == 0:
                                        expecting_seperator = 1
                                        # implicit typecast
                                        smoosh_print[x][0] = str(smoosh_print[x][0])
                                        smoosh_print[x][1] = LITERAL_YARN
                                        it_var = ''.join([it_var, (smoosh_print[x][0])])
                                    else:
                                        valid_concat = 0
                                        break
                                # AN
                                else: 
                                    if smoosh_print[x][0] == 'AN':
                                        if expecting_seperator == 0:
                                            valid_concat = 0
                                            break
                                        else:
                                            expecting_seperator = 0
                        # initialze CONCAT values to IT variable if valid
                        if valid_concat == 1:
                            symbol_table_values[0] = it_var
                            symbol_table_type[0] = LITERAL_YARN
                            lines_to_print += (it_var) + '\n'
                        else:
                            errors.append("Line " + str(line_no) + ": Invalid SMOOSH detected")

                    # end of VISIBLE SMOOSH
                    
            # ----------------------------------------------------------------------------------------------------------------------------------------------

            # Varidens
            if line[1][1] == IDENTIFIER_VARS:

                if line[1][0] in symbol_table_identifiers:

                    var_index = symbol_table_identifiers.index(line[1][0])

                    # IS NOW A
                    if line[2][0] == 'IS NOW A' and line[2][1] == KEYWORD_TYPECAST:

                        # NUBR cases
                        if symbol_table_type[var_index] == LITERAL_NUMBR:
                            # proceed to conversion
                            if line[3][0] == 'NUMBAR':
                                to_numbar = float(symbol_table_values[var_index])
                                symbol_table_values[var_index] = to_numbar
                                symbol_table_type[var_index] = LITERAL_NUMBAR
                            elif line[3][0] == 'YARN':
                                to_str = str(symbol_table_values[var_index])
                                symbol_table_values[var_index] = to_str
                                symbol_table_type[var_index] = LITERAL_YARN
                            elif line[3][0] == 'TROOF':
                                if symbol_table_values[var_index] == 1:
                                    symbol_table_values[var_index] = 'WIN'
                                    symbol_table_type[var_index] = LITERAL_TROOF
                                elif symbol_table_values[var_index] == 0:
                                    symbol_table_values[var_index] = 'FAIL'
                                    symbol_table_type[var_index] = LITERAL_TROOF
                                else:
                                    errors.append("Line " + str(line_no) + ": Invalid typecasting of NUMBR to TROOF")

                        # NUMBAR cases
                        elif symbol_table_type[var_index] == LITERAL_NUMBAR:
                            # proceed to conversion
                            if line[3][0] == 'NUMBR':
                                to_numbr = int(symbol_table_values[var_index])
                                symbol_table_values[var_index] = to_numbr
                                symbol_table_type[var_index] = LITERAL_NUMBR
                            elif line[3][0] == 'YARN':
                                to_str = str(symbol_table_values[var_index])
                                symbol_table_values[var_index] = to_str
                                symbol_table_type[var_index] = LITERAL_YARN
                            elif line[3][0] == 'TROOF':
                                if symbol_table_values[var_index] == 1.0:
                                    symbol_table_values[var_index] = 'WIN'
                                    symbol_table_type[var_index] = LITERAL_TROOF
                                elif symbol_table_values[var_index] == 0:
                                    symbol_table_values[var_index] = 'FAIL'
                                    symbol_table_type[var_index] = LITERAL_TROOF
                                errors.append("Line " + str(line_no) + ": Invalid typecasting of NUMBAR to TROOF")

                        # TROOF cases
                        elif symbol_table_type[var_index] == LITERAL_TROOF:
                            # proceed to conversion
                            if line[3][0] == 'NUMBR':
                                if symbol_table_values[var_index] == 'WIN':
                                    to_numbar = 1
                                    symbol_table_values[var_index] = to_numbar
                                    symbol_table_type[var_index] = LITERAL_NUMBAR
                                elif symbol_table_values[var_index] == 'FAIL':
                                    to_numbar = 0
                                    symbol_table_values[var_index] = to_numbar
                                    symbol_table_type[var_index] = LITERAL_NUMBAR
                            elif line[3][0] == 'NUMBAR':
                                if symbol_table_values[var_index] == 'WIN':
                                    to_numbar = 1.0
                                    symbol_table_values[var_index] = to_numbar
                                    symbol_table_type[var_index] = LITERAL_NUMBAR
                                elif symbol_table_values[var_index] == 'FAIL':
                                    to_numbar = 0.0
                                    symbol_table_values[var_index] = to_numbar
                                    symbol_table_type[var_index] = LITERAL_NUMBAR
                            elif line[3][0] == 'YARN':
                                to_str = str(symbol_table_values[var_index])
                                symbol_table_values[var_index] = to_str
                                symbol_table_type[var_index] = LITERAL_YARN

                        # YARN case
                        elif symbol_table_type[var_index] == LITERAL_YARN:
                            varident_details = detect_lexemes(symbol_table_values[var_index])
                            # returns [lexeme_token, lexeme_classification]
                            varident_value = varident_details[0]
                            varident_class = varident_details[1]

                            if line[3][0] == 'NUMBR':
                                if varident_class != LITERAL_NUMBR:
                                    errors.append("Line " + str(line_no) + ": Invalid typecasting found")
                                else:
                                    symbol_table_values[var_index] = int(varident_value)
                                    symbol_table_type[var_index] = LITERAL_NUMBR
                            elif line[3][0] == 'NUMBAR':
                                if varident_class != LITERAL_NUMBR:
                                    errors.append("Line " + str(line_no) + ": Invalid typecasting found")
                                else:
                                    symbol_table_values[var_index] = float(varident_value)
                                    symbol_table_type[var_index] = LITERAL_NUMBAR
                            elif line[3][0] == 'TROOF':
                                # NUMBR / NUBAR - TROOF
                                if varident_class == LITERAL_NUMBR:
                                    if varident_value == 1:
                                        symbol_table_values[var_index] = 'WIN'
                                        symbol_table_type[var_index] = LITERAL_TROOF
                                    elif varident_value == 0:
                                        symbol_table_values[var_index] = 'FAIL'
                                        symbol_table_type[var_index] = LITERAL_TROOF
                                    else:
                                        errors.append("Line " + str(line_no) + ": Invalid typecasting found")
                                elif varident_class == LITERAL_NUMBAR:
                                    if varident_class == LITERAL_NUMBAR:
                                        if varident_value == 1.0:
                                            symbol_table_values[var_index] = 'WIN'
                                            symbol_table_type[var_index] = LITERAL_TROOF
                                        elif varident_value == 0.0:
                                            symbol_table_values[var_index] = 'FAIL'
                                            symbol_table_type[var_index] = LITERAL_TROOF
                                        else:
                                            errors.append("Line " + str(line_no) + ": Invalid typecasting found")
                                # YARN - TROOF
                                elif varident_class == LITERAL_TROOF:
                                    symbol_table_values[var_index] = varident_value
                                    symbol_table_type[var_index] = LITERAL_TROOF
                                else:
                                    errors.append("Line " + str(line_no) + ": Invalid typecasting found")

                            # YARN to TROOF to NUMBR / NUMBAR
                            elif varident_class == LITERAL_TROOF:
                                if varident_value == 'WIN':
                                    if new_class == LITERAL_NUMBR:
                                        symbol_table_values[var_index] = 1
                                        symbol_table_type[var_index] = LITERAL_NUMBR
                                    else:
                                        symbol_table_values[var_index] = 1.0
                                        symbol_table_type[var_index] = LITERAL_NUMBAR
                                elif varident_value == 'FAIL':
                                    if new_class == LITERAL_NUMBR:
                                        symbol_table_values[var_index] = 0
                                        symbol_table_type[var_index] = LITERAL_NUMBR
                                    else:
                                        symbol_table_values[var_index] = 0.0
                                        symbol_table_type[var_index] = LITERAL_NUMBAR

                        # NOOB case
                        else:
                            errors.append("Line " + str(line_no) + ": NOOB can only be implicitly casted to TROOF")

                    # end of IS NOW A clause

                    # R
                    elif line[2][0] == 'R' and line[2][1] == VAR_ASSIGN and line[3][1] in [KEYWORD_ARITHMETIC, KEYWORD_BOOLEAN, KEYWORD_COMPARE, LITERAL_NUMBR, LITERAL_NUMBAR, LITERAL_YARN, LITERAL_TROOF]:

                        # literal
                        if line[3][1] in [LITERAL_NUMBR, LITERAL_NUMBAR, LITERAL_YARN, LITERAL_TROOF]:
                            # retrieve new value
                            symbol_table_values[var_index] = line[3][0]
                            # NUMBR
                            if line[3][1] == LITERAL_NUMBR:
                                symbol_table_type[var_index] = LITERAL_NUMBR   
                            # NUMBAR
                            elif line[3][1] == LITERAL_NUMBAR:
                                symbol_table_type[var_index] = LITERAL_NUMBAR   
                            # YARN
                            elif line[3][1] == LITERAL_YARN:
                                symbol_table_type[var_index] = LITERAL_YARN   
                            # TROOF
                            elif line[3][1] == LITERAL_TROOF:
                                symbol_table_type[var_index] = LITERAL_TROOF

                        # variable
                        elif line[3][1] == IDENTIFIER_VARS:
                            # check first if second variable exists
                            if line[3][0] in symbol_table_identifiers:
                                # reassign value of 1st var with value of 2nd var
                                retrieve_var_index = symbol_table_identifiers.index(line[1][0])
                                symbol_table_values[var_index] = retrieve_var_index
                                symbol_table_type[var_index] = symbol_table_type[retrieve_var_index]                               
                            else:
                                errors.append("Line " + str(line_no) + ": Variable does not exist")
                        
                        # arithmetic expression
                        elif line[3][1] == KEYWORD_ARITHMETIC:

                            perform_mathe = line[3:]                            
                            a_perform = perform_arithmetic(symbol_table_identifiers, symbol_table_values, symbol_table_type, perform_mathe, line_no)
                            
                            # if invalid, returns [0, error message]
                            # if valid, returns [1, result, type of result]
                            if len(a_perform) == 2:
                                # error
                                if a_perform[0] == 0:
                                    errors.append(a_perform[1])
                            elif len(a_perform) == 3:
                                # valid
                                if a_perform[0] == 1:
                                    answer_type = a_perform[2]
                                    # to IT
                                    symbol_table_values[0] = a_perform[1]
                                    symbol_table_type[0] = a_perform[2]
                                    # from IT to 1st var value
                                    symbol_table_values[var_index] = a_perform[1]
                                    symbol_table_type[var_index] = a_perform[2]

                        # boolean expression
                        elif line[3][1] == KEYWORD_BOOLEAN:
                            b_expr = line[3:]
                            b_perform = perform_boolean(symbol_table_identifiers, symbol_table_values, symbol_table_type, b_expr, line_no)

                            # if invalid, returns [0, error message]
                            # if valid, returns [1, result]

                            if b_perform[0] == 0:
                                errors.append(b_perform[1])
                            elif b_perform[0] == 1:
                                    # to IT
                                    symbol_table_values[0] = b_perform[1]
                                    symbol_table_type[0] = LITERAL_TROOF
                                    # from IT to 1st var value
                                    symbol_table_values[var_index] = b_perform[1]
                                    symbol_table_type[var_index] = LITERAL_TROOF

                        # compare expression    

                        else:
                            errors.append("Line " + str(line_no) + ": Invalid R assignment call")

                    # end of R clause

                    # R MAEK
                    elif line[2][0] == 'R' and line[3][0] == 'MAEK':
                        if len(line) >= 6:
                            # check if correct call of variable name:
                            if line[1][0] == line[4][0] and line[5][1] == LITERAL:

                                # NUBR cases
                                if symbol_table_type[var_index] == LITERAL_NUMBR:
                                    # proceed to conversion
                                    if line[5][0] == 'NUMBAR':
                                        to_numbar = float(symbol_table_values[var_index])
                                        symbol_table_values[var_index] = to_numbar
                                        symbol_table_type[var_index] = LITERAL_NUMBAR
                                    elif line[5][0] == 'YARN':
                                        to_str = str(symbol_table_values[var_index])
                                        symbol_table_values[var_index] = to_str
                                        symbol_table_type[var_index] = LITERAL_YARN
                                    elif line[5][0] == 'TROOF':
                                        if symbol_table_values[var_index] == 1:
                                            symbol_table_values[var_index] = 'WIN'
                                            symbol_table_type[var_index] = LITERAL_TROOF
                                        elif symbol_table_values[var_index] == 0:
                                            symbol_table_values[var_index] = 'FAIL'
                                            symbol_table_type[var_index] = LITERAL_TROOF
                                        else:
                                            print(str(symbol_table_values[var_index]))
                                            errors.append("Line " + str(line_no) + ": Invalid typecasting of NUMBR to TROOF")

                                # NUMBAR cases
                                elif symbol_table_type[var_index] == LITERAL_NUMBAR:
                                    # proceed to conversion
                                    if line[5][0] == 'NUMBR':
                                        to_numbr = int(symbol_table_values[var_index])
                                        symbol_table_values[var_index] = to_numbr
                                        symbol_table_type[var_index] = LITERAL_NUMBR
                                    elif line[5][0] == 'YARN':
                                        to_str = str(symbol_table_values[var_index])
                                        symbol_table_values[var_index] = to_str
                                        symbol_table_type[var_index] = LITERAL_YARN
                                    elif line[5][0] == 'TROOF':
                                        if symbol_table_values[var_index] == 1.0:
                                            symbol_table_values[var_index] = 'WIN'
                                            symbol_table_type[var_index] = LITERAL_TROOF
                                        elif symbol_table_values[var_index] == 0:
                                            symbol_table_values[var_index] = 'FAIL'
                                            symbol_table_type[var_index] = LITERAL_TROOF
                                        errors.append("Line " + str(line_no) + ": Invalid typecasting of NUMBAR to TROOF")

                                # TROOF cases
                                elif symbol_table_type[var_index] == LITERAL_TROOF:
                                    # proceed to conversion
                                    if line[5][0] == 'NUMBR':
                                        if symbol_table_values[var_index] == 'WIN':
                                            to_numbar = 1
                                            symbol_table_values[var_index] = to_numbar
                                            symbol_table_type[var_index] = LITERAL_NUMBAR
                                        elif symbol_table_values[var_index] == 'FAIL':
                                            to_numbar = 0
                                            symbol_table_values[var_index] = to_numbar
                                            symbol_table_type[var_index] = LITERAL_NUMBAR
                                    elif line[5][0] == 'NUMBAR':
                                        if symbol_table_values[var_index] == 'WIN':
                                            to_numbar = 1.0
                                            symbol_table_values[var_index] = to_numbar
                                            symbol_table_type[var_index] = LITERAL_NUMBAR
                                        elif symbol_table_values[var_index] == 'FAIL':
                                            to_numbar = 0.0
                                            symbol_table_values[var_index] = to_numbar
                                            symbol_table_type[var_index] = LITERAL_NUMBAR
                                    elif line[5][0] == 'YARN':
                                        to_str = str(symbol_table_values[var_index])
                                        symbol_table_values[var_index] = to_str
                                        symbol_table_type[var_index] = LITERAL_YARN

                                # YARN case
                                elif symbol_table_type[var_index] == LITERAL_YARN:
                                    varident_details = detect_lexemes(symbol_table_values[var_index])
                                    # returns [lexeme_token, lexeme_classification]
                                    varident_value = varident_details[0]
                                    varident_class = varident_details[1]

                                    if line[5][0] == 'NUMBR':
                                        if varident_class != LITERAL_NUMBR:
                                            errors.append("Line " + str(line_no) + ": Invalid typecasting found")
                                        else:
                                            symbol_table_values[var_index] = int(varident_value)
                                            symbol_table_type[var_index] = LITERAL_NUMBR
                                    elif line[5][0] == 'NUMBAR':
                                        if varident_class != LITERAL_NUMBR:
                                            errors.append("Line " + str(line_no) + ": Invalid typecasting found")
                                        else:
                                            symbol_table_values[var_index] = float(varident_value)
                                            symbol_table_type[var_index] = LITERAL_NUMBAR
                                    elif line[5][0] == 'TROOF':
                                        # NUMBR / NUBAR - TROOF
                                        if varident_class == LITERAL_NUMBR:
                                            if varident_value == 1:
                                                symbol_table_values[var_index] = 'WIN'
                                                symbol_table_type[var_index] = LITERAL_TROOF
                                            elif varident_value == 0:
                                                symbol_table_values[var_index] = 'FAIL'
                                                symbol_table_type[var_index] = LITERAL_TROOF
                                            else:
                                                errors.append("Line " + str(line_no) + ": Invalid typecasting found")
                                        elif varident_class == LITERAL_NUMBAR:
                                            if varident_class == LITERAL_NUMBAR:
                                                if varident_value == 1.0:
                                                    symbol_table_values[var_index] = 'WIN'
                                                    symbol_table_type[var_index] = LITERAL_TROOF
                                                elif varident_value == 0.0:
                                                    symbol_table_values[var_index] = 'FAIL'
                                                    symbol_table_type[var_index] = LITERAL_TROOF
                                                else:
                                                    errors.append("Line " + str(line_no) + ": Invalid typecasting found")
                                        # YARN - TROOF
                                        elif varident_class == LITERAL_TROOF:
                                            symbol_table_values[var_index] = varident_value
                                            symbol_table_type[var_index] = LITERAL_TROOF
                                        else:
                                            errors.append("Line " + str(line_no) + ": Invalid typecasting found")

                                    # YARN to TROOF to NUMBR / NUMBAR
                                    elif varident_class == LITERAL_TROOF:
                                        if varident_value == 'WIN':
                                            if new_class == LITERAL_NUMBR:
                                                symbol_table_values[var_index] = 1
                                                symbol_table_type[var_index] = LITERAL_NUMBR
                                            else:
                                                symbol_table_values[var_index] = 1.0
                                                symbol_table_type[var_index] = LITERAL_NUMBAR
                                        elif varident_value == 'FAIL':
                                            if new_class == LITERAL_NUMBR:
                                                symbol_table_values[var_index] = 0
                                                symbol_table_type[var_index] = LITERAL_NUMBR
                                            else:
                                                symbol_table_values[var_index] = 0.0
                                                symbol_table_type[var_index] = LITERAL_NUMBAR

                                # NOOB case
                                else:
                                    errors.append("Line " + str(line_no) + ": NOOB can only be implicitly casted to TROOF")

                    # end of R MAEK clause

                    # R SMOOSH
                    elif line[2][0] == 'R' and line[3][0] == 'SMOOSH':
                        # should place concatenated string to IT variable
                        it_var = ''
                        valid_concat = 1
                        expecting_seperator = 0

                        # retrieve smoosh expression for printing
                        smoosh_print = line[3:]

                        for x in range(1, len(smoosh_print)):
                            # YARN
                            if smoosh_print[x][1] == LITERAL_YARN:
                                if expecting_seperator == 0:
                                    expecting_seperator = 1
                                    it_var = ''.join([it_var, (smoosh_print[x][0])])
                                else:
                                    valid_concat = 0
                                    break
                            else:
                                # Varident
                                if smoosh_print[x][1] == IDENTIFIER_VARS:
                                    if smoosh_print[x][0] in symbol_table_identifiers:
                                        expecting_seperator = 1
                                        var_index = symbol_table_identifiers.index(smoosh_print[x][0])
                                        to_yarn = symbol_table_values[var_index]

                                        # typecast
                                        if symbol_table_type[var_index] != LITERAL_YARN:
                                            to_yarn = str(symbol_table_values[var_index])

                                            # implicit recast of variables
                                            symbol_table_values[var_index] = to_yarn
                                            symbol_table_type[var_index] = LITERAL_YARN
                                        it_var = ''.join([it_var, to_yarn])                                            
                                    else:
                                        valid_concat = 0
                                        break
                                # Other values
                                elif smoosh_print[x][1] in [LITERAL_NOOB, LITERAL_NUMBAR, LITERAL_NUMBR, LITERAL_NUMBAR]:
                                    if expecting_seperator == 0:
                                        expecting_seperator = 1
                                        # implicit typecast
                                        smoosh_print[x][0] = str(smoosh_print[x][0])
                                        smoosh_print[x][1] = LITERAL_YARN
                                        it_var = ''.join([it_var, (smoosh_print[x][0])])
                                    else:
                                        valid_concat = 0
                                        break
                                # AN
                                else: 
                                    if smoosh_print[x][0] == 'AN':
                                        if expecting_seperator == 0:
                                            valid_concat = 0
                                            break
                                        else:
                                            expecting_seperator = 0
                        # initialze CONCAT values to IT variable if valid
                        if valid_concat == 1:
                            # add to IT
                            symbol_table_values[0] = it_var
                            symbol_table_type[0] = LITERAL_YARN
                            # add to var
                            symbol_table_values[var_index] = it_var
                            symbol_table_type[var_index] = LITERAL_YARN
                        else:
                            errors.append("Line " + str(line_no) + ": Invalid SMOOSH detected")

                    # end of R MAEK SMOOSH clause

                # end of Varident first line clause
                else:
                    errors.append("Line " + str(line_no) + ": Variable does note exist")

            # ----------------------------------------------------------------------------------------------------------------------------------------------
            

            # ----------------------------------------------------------------------------------------------------------------------------------------------

            # GIMMEH
            if line[1][0] == 'GIMMEH' and line[1][1] == KEYWORD_INPUT:
                if line[2][0] in symbol_table_identifiers:
                    var_index = symbol_table_identifiers.index(line[2][0])

                    val_input = tk.simpledialog.askstring(title="GIMMEH", prompt=("Input: " + str(line[2][0])))
                    
                    symbol_table_values[var_index] = val_input
                    symbol_table_type[var_index] = LITERAL_YARN
                else:
                    errors.append("Line " + str(line_no) + ": Variable does not exist")

            # ----------------------------------------------------------------------------------------------------------------------------------------------

            # SMOOSH (does not consider expressions)
            if line[1][0] == 'SMOOSH' and line[1][1] == KEYWORD_CONCAT:
                # should place concatenated string to IT variable
                it_var = ''
                valid_concat = 1

                for x in range(1, len(line)):
                    if (x % 2) == 0:
                        if line[x][1] == LITERAL_YARN:
                            it_var = ''.join([it_var, (line[x][0])])
                        else:
                            #
                            if line[x][0] in symbol_table_identifiers:
                                var_index = symbol_table_identifiers.index(line[x][0])
                                to_yarn = symbol_table_values[var_index]

                                # typecast
                                if symbol_table_type[var_index] != LITERAL_YARN:
                                    to_yarn = str(symbol_table_values[var_index])

                                    # implicit recast of variables
                                    symbol_table_values[var_index] = to_yarn
                                    symbol_table_type[var_index] = LITERAL_YARN

                                it_var = ' '.join([it_var, to_yarn])
                            # other values
                            elif line[x][1] in [LITERAL_NUMBAR, LITERAL_NUMBR, LITERAL_TROOF, LITERAL_NOOB]:
                                # implicit typecast
                                line[x][1] = str(line[x][1])
                                line[x][0] = LITERAL_YARN
                                it_var = ''.join([it_var, (line[x][0])])
                            # invalid
                            else:
                                valid_concat = 0

                # initialze CONCAT values to IT variable if valid
                if valid_concat == 1:
                    symbol_table_values[0] = it_var
                    symbol_table_type[0] = LITERAL_YARN
                    lines_to_print += (it_var) + '\n'
                else:
                    errors.append("Line " + str(line_no) + ": Invalid SMOOSH detected")

            # ----------------------------------------------------------------------------------------------------------------------------------------------


            # ----------------------------------------------------------------------------------------------------------------------------------------------


            # ----------------------------------------------------------------------------------------------------------------------------------------------

    # end of for loop for semantic checker

    if len(errors) > 0 :
        for error in errors:
            print(error)

    # checker of symbol table
    print("\n--- \n\nSymbol Table: ")
    print("\nVariables: \n" + str(symbol_table_identifiers))
    print("\nValues: \n" + str(symbol_table_values))
    print("\nTypes: \n" + str(symbol_table_type))

    return [symbol_table_identifiers, symbol_table_values, lines_to_print, errors]

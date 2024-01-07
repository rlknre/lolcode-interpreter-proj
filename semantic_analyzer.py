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

def perform_boolean():
    None


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
    symbol_table_values.append('')
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
                            print(answer_result)
                            symbol_table_values[0] = answer_result
                            symbol_table_type[0] = LITERAL_NUMBR

            # ----------------------------------------------------------------------------------------------------------------------------------------------

            # I HAS A
            if line[1][0] == "I HAS A" and line[1][1] == VAR_DECLARE:

                # uninitialized variable
                if len(line) == 3:
                    symbol_table_identifiers.append(line[2][0])
                    symbol_table_values.append('')
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

            # ----------------------------------------------------------------------------------------------------------------------------------------------

            # VSIBLIE
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
                    # use the IT variable
                    symbol_table_values[0] = ''
                    it_var = ''
                    valid_visible = 1
                    for x in range(1, len(line)):
                        if (x % 2) == 0:
                            if line[x][1] == LITERAL_YARN:

                                it_var = ''.join([it_var, (line[x][0])])

                            else:
                                if line[x][0] in symbol_table_identifiers:
                                    var_index = symbol_table_identifiers.index(line[x][0])
                                    to_yarn = str(symbol_table_values[var_index])
                                    it_var = ''.join([it_var, to_yarn])
                                else:
                                    valid_visible = 0

                    # does not print if a variable not found 
                    if valid_visible == 1:
                        symbol_table_values[0] = it_var
                        symbol_table_type[0] = LITERAL_YARN
                        lines_to_print += symbol_table_values[0] + '\n'

                    # NOTE: add error condition
                    
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
                                # NOTE: Add else statement
                            
                            # NOTE: Add else statement

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
                                # NOTE: Add else statement
                            
                            # NOTE: Add else statement


                        # TROOF cases


                        # YARN case

                # NOTE: Add error message for nonexisting varidents

            # ----------------------------------------------------------------------------------------------------------------------------------------------
            

            # ----------------------------------------------------------------------------------------------------------------------------------------------

            # GIMMEH
            if line[1][0] == 'GIMMEH' and line[1][1] == KEYWORD_INPUT:
                if line[2][0] in symbol_table_identifiers:
                    var_index = symbol_table_identifiers.index(line[2][0])

                    val_input = tk.simpledialog.askstring(title="GIMMEH", prompt=("Input: " + str(line[2][0])))
                    
                    symbol_table_values[var_index] = val_input
                    symbol_table_type[var_index] = LITERAL_YARN

                # NOTE: add error condition

            # ----------------------------------------------------------------------------------------------------------------------------------------------

            # SMOOSH
            if line[1][0] == 'SMOOSH' and line[1][1] == KEYWORD_CONCAT:
                # should place concatenated string to IT variable
                it_var = ''
                valid_concat = 1

                for x in range(1, len(line)):
                    if (x % 2) == 0:
                        if line[x][1] == LITERAL_YARN:
                            # to_concat = list(line[x][0])
                            # to_concat = to_concat[:-1]
                            # to_concat = to_concat[1:]
                            # to_concat = ''.join(to_concat)

                            it_var = ''.join([it_var, (line[x][0])])
                        else:
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
                            
                            else:
                                valid_concat = 0

                # initialze CONCAT values to IT variable if valid
                if valid_concat == 1:
                    symbol_table_values[0] = it_var
                    symbol_table_type[0] = LITERAL_YARN

                # NOTE: Add error message

            # ----------------------------------------------------------------------------------------------------------------------------------------------


            # ----------------------------------------------------------------------------------------------------------------------------------------------


            # ----------------------------------------------------------------------------------------------------------------------------------------------

    # checker of symbol table
    print("\n--- \n\nSymbol Table: ")
    print("\nVariables: \n" + str(symbol_table_identifiers))
    print("\nValues: \n" + str(symbol_table_values))
    print("\nTypes: \n" + str(symbol_table_type))

    return [symbol_table_identifiers, symbol_table_values, lines_to_print, errors]

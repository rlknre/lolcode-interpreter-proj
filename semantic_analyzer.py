import re

# import lexical analyzer function
from lexical_analyzer import lexical_tester

# import syntax analyzer function
from syntax_analyzer import syntax_tester

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


# ----------------------------------------------------------------------------------------------------------------------------------------------

# errors
semantic_errors = []

# ----------------------------------------------------------------------------------------------------------------------------------------------

def perform_arithmetic():
    None


# ----------------------------------------------------------------------------------------------------------------------------------------------

def perform_boolean():
    None


# ----------------------------------------------------------------------------------------------------------------------------------------------

def perform_comparison():
    None


# ----------------------------------------------------------------------------------------------------------------------------------------------

# perform the code if syntax is valid

def semantic_perform(code_details):

    # symbol table 
    symbol_table_identifiers = []
    symbol_table_values = []
    symbol_table_type = []

    symbol_table_identifiers.append('IT')
    symbol_table_values.append('')
    symbol_table_type.append(LITERAL_NOOB)

    code_block = code_details

    for line in code_block:

        if len(line) > 1:

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

                        print(symbol_table_values[0])

                    else:
                        if line[2][0] in symbol_table_identifiers:
                            var_index = symbol_table_identifiers.index(line[2][0])
                            
                            symbol_table_values[0] = ''
                            it_var = str(symbol_table_values[var_index])
                            symbol_table_values[0] = it_var
                            symbol_table_type[0] = LITERAL_YARN

                            print(symbol_table_values[0])
                        
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
                        print(symbol_table_values[0])

                    # NOTE: add error condition
                    
            # ----------------------------------------------------------------------------------------------------------------------------------------------

            
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
                    val_input = input('')
                    val_input = val_input.strip('\n')
                    
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

    return [symbol_table_identifiers, symbol_table_values]

    # checker of symbol table
    print("\n--- \n\nSymbol Table: ")
    print("\nVariables: \n" + str(symbol_table_identifiers))
    print("\nValues: \n" + str(symbol_table_values))
    print("\nTypes: \n" + str(symbol_table_type))

# testing area ---------------------------------------------------------------------------------------------------------------------------------

sample = """HAI
    I HAS A var1 ITZ "hello"
    I HAS A var2 ITZ 12
    I HAS A var3 ITZ WIN

    VISIBLE "noot noot" + var2
    BTW VISIBLE var2

    BTW var2 IS NOW A NUMBAR

    VISIBLE ""
    VISIBLE "String before input: " + var1
    VISIBLE "Need input: "
    BTW GIMMEH var1

    VISIBLE ""
    VISIBLE "String after input: " + var2

    BTW SMOOSH "hellO" AN var3 AN var1

KTHXBYE"""

# # check if lexical test found a lexeme
# found_lexeme = 0
# lexical_test = lexical_tester(sample)
# for line in lexical_test:
#     if len(line) > 1:
#         found_lexeme = 1
#         break

# if found_lexeme == 1:
#     syntax_test = syntax_tester(lexical_test)

#     # check if return value of syntax is correct
#     if len(syntax_test) != 2:
#         print("\nInvalid\n")

#     else:
#         syntax_check = syntax_test[1]

#         # no errors in code
#         if syntax_check == 1:
#             code_block = syntax_test[0]

#             # run code here
#             print("")
#             semantic_perform(code_block)
#             print("")
            
#         # errors in code
#         else:
#             print("\nInvalid\n")

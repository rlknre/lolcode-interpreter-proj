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

# symbol table 
symbol_table_identifiers = []
symbol_table_values = []
symbol_table_type = []

symbol_table_identifiers.append('IT')
symbol_table_values.append('')
symbol_table_type.append(LITERAL_NOOB)

# perform the code if semantics are valid

def semantic_perform(code_details):

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
                    symbol_table_identifiers.append(line[2][0])

                    if line[4][1] == LITERAL_YARN:
                        # clear string
                        yarn_val = line[4][0]
                        yarn_val = list(yarn_val)
                        yarn_val = yarn_val[:-1]
                        yarn_val = yarn_val[1:]
                        yarn_val = ''.join(yarn_val)
                        symbol_table_values.append(yarn_val)
                        symbol_table_type.append(LITERAL_YARN)
                    
                    elif line[4][1] == LITERAL_TROOF:
                        symbol_table_values.append(line[4][0])
                        symbol_table_type.append(LITERAL_YARN)
                    
                    elif line[4][1] == LITERAL_NUMBR:
                        symbol_table_values.append(int(line[4][0]))
                        symbol_table_type.append(LITERAL_NUMBR)
                    
                    elif line[4][1] == LITERAL_NUMBAR:
                        symbol_table_values.append(float(line[4][0]))
                        symbol_table_type.append(LITERAL_NUMBAR)

             # ----------------------------------------------------------------------------------------------------------------------------------------------

            # VISIBLE
            if line[1][0] == 'VISIBLE' and line[1][1] == KEYWORD_PRINT:
                # only one to print
                if len(line) <= 3:
                    if line[2][1] == LITERAL_YARN:
                        # use the IT variable 
                        symbol_table_values[0] = ''

                        # cleans string
                        it_var = line[2][0]
                        it_var = list(it_var)
                        it_var = it_var[:-1]
                        it_var = it_var[1:]
                        symbol_table_values[0] = ''.join(it_var)
                        symbol_table_type[0] = LITERAL_YARN

                        print(symbol_table_values[0])
                    else:
                        print(line[2][0])

                # multiple values
                else:
                    # use the IT variable
                    symbol_table_values[0] = ''
                    it_var = ''
                    for x in range(1, len(line)-1):
                        if (x % 2) == 0:
                            if line[x][1] == LITERAL_YARN:
                                to_print = list(line[x][0])
                                to_print = to_print[:-1]
                                to_print = to_print[1:]
                                to_print = ''.join(to_print)

                                it_var = ''.join([it_var, to_print])
                            else:
                                print(line[x][0], end=" ")

                    symbol_table_values[0] = it_var
                    symbol_table_type[0] = LITERAL_YARN
                    print(symbol_table_values[0])

    # checker
    print("\n -- ")
    print(symbol_table_identifiers)
    print(symbol_table_values)
    print(symbol_table_type)

# testing

sample = """HAI
    I HAS A var1
    I HAS A var2 ITZ 12
    I HAS A var3
    I HAS A var4 ITZ WIN
    I HAS A var5 ITZ 12.5

    VISIBLE "noot noot" + var2

    var2 IS NOW A NUMBAR
    VISIBLE var2

    var1 R 17
    var2 R var1

    var2 R MAEK var2 YARN

    BTW VISIBLE "Need input: "
    GIMMEH var3

KTHXBYE"""

# check if lexical test found a lexeme
found_lexeme = 0
lexical_test = lexical_tester(sample)
for line in lexical_test:
    if len(line) > 1:
        found_lexeme = 1
        break

if found_lexeme == 1:
    syntax_test = syntax_tester(lexical_test)

    # check if there are errors in the code
    if len(syntax_test) != 2:
        print("\nInvalid\n")

    # no errors in code
    else:
        syntax_check = syntax_test[1]
        if syntax_check == 1:
            code_block = syntax_test[0]
            print("\nNo errors. Running code... \n")
            print("--- \n")

            # run code here
            semantic_perform(code_block)
            print("")
            
        else:
            print("\nInvalid\n")

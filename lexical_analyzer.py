
import re   # regex library

# https://www.w3schools.com/python/python_regex.asp
# findall	Returns a list containing all matches
# search	Returns a Match object if there is a match anywhere in the string
# split	    Returns a list where the string has been split at each match
# sub	    Replaces one or many matches with a string

# arrays for lexeme tracking
code_per_line = []
token_list = []
token_classification = []

# constants for lexeme classification
DELIMITER_CODE = "Code Delimiter"
DELIMITER_STR = "String Delimiter"
DELIMITER_VAR = "Declaration Delimiter"
DELIMITER_CONDT = "Conditionals Delimiter"
DELIMITER_END = "End of Expression Delimiter"

IDENTIFIER_VARS = "Variable Identifier"
IDENTIFIER_FUNC = "Function Identifier"
IDENTIFIER_LOOP = "Loop Identifier"

VAR_DECLARE = "Variable Declaration"
VAR_ASSIGN = "Variable Assignment"

KEYWORD_COMMENT = "Comment Keyword"
KEYWORD_ARITHMETIC = "Arithmetic Keyword"
KEYWORD_SEPERATOR = "Separator Keyword"
KEYWORD_COMPARE = "Comparison Keyword"
KEYWORD_BOOLEAN = "Boolean Keyword"
KEYWORD_CONCAT = "Concatenate Keyword"
KEYWORD_TYPECAST = "Typecasting Keyword"
KEYWORD_PRINT = "Output Keyword"
KEYWORD_INPUT = "Input Keyword"
KEYWROD_CONDT = "Conditional Keyword"
KEYWORD_LOOP = "Loop Keyword"
KEYWORD_FUNC = "Function Keyword"

LITERAL = "Literal"
LITERAL_NUMBAR = "NUMBAR Literal"
LITERAL_NUMBR = "NUMBR Literal"
LITERAL_TROOF = "TROOF Literal"
LITERAL_YARN = "YARN Literal"

# add function description here

def detect_lexemes(line):

    lexeme_information = []
    lexeme_tokens = []
    lexeme_classification = []
    token = ""
    
    # code delimiter tokens

    if (re.search("^HAI$", line) != None):
        lexeme_tokens.append("HAI")
        lexeme_classification.append(
            DELIMITER_CODE
        )
        token = "HAI"

    elif (re.search("^KTHXBYE$", line) != None):
        lexeme_tokens.append("KTHXBYE")
        lexeme_classification.append(
            DELIMITER_CODE
        )
        token = "KTHXBYE"
    
    # comment tokens

    elif (re.search("(^ )?OBTW(.)", line) != None):
        lexeme_tokens.append("OBTW")
        lexeme_classification.append(
            KEYWORD_COMMENT
        )
        comment = line.split("OBTW", 1)
        token = "OBTW" + comment[1]
    
    elif (re.search("(^)?TLDR$", line) != None):
        lexeme_tokens.append("TLDR")
        lexeme_classification.append(
            KEYWORD_COMMENT
        )
        token = "TLDR"

    elif (re.search("(.)?BTW (.)", line) != None):
        lexeme_tokens.append("BTW")
        lexeme_classification.append(
            KEYWORD_COMMENT
        )
        # also removes the comment line
        comment = line.split("BTW", 1)
        token = "BTW" + comment[1]

    # variable declaration section tokens

    elif (re.search("(.)?WAZZUP$", line) != None):
        lexeme_tokens.append("WAZZUP")
        lexeme_classification.append(
            DELIMITER_VAR
        )
        token = "WAZZUP"

    elif (re.search("(.)?BUHBYE$", line) != None):
        lexeme_tokens.append("BUHBYE")
        lexeme_classification.append(
            DELIMITER_VAR
        )
        token = "BUHBYE"

    # assignment operations 1

    elif (re.search("(^ )?I HAS A(.)", line) != None):
        lexeme_tokens.append("I HAS A")
        lexeme_classification.append(
            VAR_DECLARE
        )
        token = "I HAS A"

    elif (re.search(" ITZ [a-zA-Z0-9\.]+", line) != None):
        lexeme_tokens.append("ITZ")
        lexeme_classification.append(
            VAR_ASSIGN
        )
        token = "ITZ"

    elif (re.search("(^ )?IT ", line) != None):
        lexeme_tokens.append("IT")
        lexeme_classification.append(
            VAR_ASSIGN
        )
        token = "IT"

    elif (re.search(" R ", line) != None):
        lexeme_tokens.append("R")
        lexeme_classification.append(
            VAR_ASSIGN
        )
        token = "R"
    
    # arithmetic operations

    elif ((re.search("(^ )?SUM OF ", line)) != None):
        lexeme_tokens.append("SUM OF")
        lexeme_classification.append(
            KEYWORD_ARITHMETIC
        )
        token = "SUM OF"

    elif ((re.search("(^ )?PRODUCKT OF ", line)) != None):
        lexeme_tokens.append("PRODUCKT OF")
        lexeme_classification.append(
            KEYWORD_ARITHMETIC
        )
        token = "PRODUCKT OF"
    
    elif ((re.search("(^ )?DIFF OF ", line)) != None):
        lexeme_tokens.append("DIFF OF")
        lexeme_classification.append(
            KEYWORD_ARITHMETIC
        )
        token = "DIFF OF"
    
    elif ((re.search("(^ )?QUOSHUNT OF ", line)) != None):
        lexeme_tokens.append("QUOSHUNT OF")
        lexeme_classification.append(
            KEYWORD_ARITHMETIC
        )
        token = "QUOSHUNT OF"
    
    elif ((re.search("(^ )?MOD OF ", line)) != None):
        lexeme_tokens.append("MOD OF")
        lexeme_classification.append(
            KEYWORD_ARITHMETIC
        )
        token = "MOD OF"

    # comparison operations

    elif ((re.search("(^ )?BIGGR OF ", line)) != None):
        lexeme_tokens.append("BIGGR OF")
        lexeme_classification.append(
            KEYWORD_COMPARE
        )
        token = "BIGGR OF"

    elif ((re.search("(^ )?SMALLR OF ", line)) != None):
        lexeme_tokens.append("SMALLR OF")
        lexeme_classification.append(
            KEYWORD_COMPARE
        )
        token = "SMALLR OF"
    
    elif ((re.search("(^ )?BOTH OF ", line)) != None):
        lexeme_tokens.append("BOTH OF")
        lexeme_classification.append(
            KEYWORD_BOOLEAN
        )
        token = "BOTH OF"

    elif ((re.search("(^ )?EITHER OF ", line)) != None):
        lexeme_tokens.append("EITHER OF")
        lexeme_classification.append(
            KEYWORD_BOOLEAN
        )
        token = "EITHER OF"
    
    elif ((re.search("(^ )?WON OF ", line)) != None):
        lexeme_tokens.append("WON OF")
        lexeme_classification.append(
            KEYWORD_BOOLEAN
        )
        token = "WON OF"
    
    elif ((re.search("(^ )?NOT ", line)) != None):
        lexeme_tokens.append("NOT")
        lexeme_classification.append(
            KEYWORD_BOOLEAN
        )
        token = "NOT"

    elif ((re.search("(^ )?ANY OF ", line)) != None):
        lexeme_tokens.append("NOT")
        lexeme_classification.append(
            KEYWORD_BOOLEAN
        )
        token = "NOT"

    elif ((re.search("(^ )?ALL OF ", line)) != None):
        lexeme_tokens.append("ALL OF")
        lexeme_classification.append(
            KEYWORD_BOOLEAN
        )
        token = "ALL OF"
    
    elif ((re.search("(^ )?BOTH SAEM ", line)) != None):
        lexeme_tokens.append("BOTH SAEM")
        lexeme_classification.append(
            KEYWORD_COMPARE
        )
        token = "BOTH SAEM"

    elif ((re.search("(^ )?DIFFRINT ", line)) != None):
        lexeme_tokens.append("DIFFRINT")
        lexeme_classification.append(
            KEYWORD_COMPARE
        )
        token = "DIFFRINT"
    
    # string concatenation token

    elif ((re.search("(^ )?SMOOSH ", line)) != None):
        lexeme_tokens.append("SMOOSH")
        lexeme_classification.append(
            KEYWORD_CONCAT
        )
        token = "SMOOSH"
    
    elif ((re.search(" \+(.)?", line)) != None):
        lexeme_tokens.append("+")
        lexeme_classification.append(
            KEYWORD_CONCAT
        )
        token = "+"

    # typecasting operations 

    elif ((re.search(" MAEK ", line)) != None):
        lexeme_tokens.append("MAEK")
        lexeme_classification.append(
            KEYWORD_TYPECAST
        )
        token = "MAEK"

    elif ((re.search(" IS NOW A ", line)) != None):
        lexeme_tokens.append("IS NOW A")
        lexeme_classification.append(
            KEYWORD_TYPECAST
        )
        token = "IS NOW A"

    elif ((re.search(" A ", line)) != None):
        lexeme_tokens.append("A")
        lexeme_classification.append("keyword")
        token = "A"
    
    # print function token

    elif ((re.search("(^ )?VISIBLE ", line)) != None):
        lexeme_tokens.append("VISIBLE")
        lexeme_classification.append(
            KEYWORD_PRINT
        )
        token = "VISIBLE"
        
    # input function token

    elif ((re.search("(^ )?GIMMEH ", line)) != None):
        lexeme_tokens.append("GIMMEH")
        lexeme_classification.append(
            KEYWORD_INPUT
        )
        token = "GIMMEH"

    # if-then tokens

    elif ((re.search("(^ )?O RLY\?$", line)) != None):
        lexeme_tokens.append("O RLY?")
        lexeme_classification.append(
            DELIMITER_CONDT
        )
        token = "O RLY?"
    
    elif ((re.search("(^ )?YA RLY$", line)) != None):
        lexeme_tokens.append("YA RLY")
        lexeme_classification.append(
            KEYWROD_CONDT
        )
        token = "YA RLY"
    
    elif ((re.search("(^ )?NO WAI$", line)) != None):
        lexeme_tokens.append("NO WAI")
        lexeme_classification.append(
            KEYWROD_CONDT
        )
        token = "NO WAI"

    elif ((re.search("(^ )?OIC$", line)) != None):
        lexeme_tokens.append("OIC")
        lexeme_classification.append(
            DELIMITER_CONDT
        )
        token = "OIC"

    # switch case tokens

    elif ((re.search("(^ )?WTF$", line)) != None):
        lexeme_tokens.append("WTF")
        lexeme_classification.append(
            DELIMITER_CONDT
        )
        token = "WTF"
    
    elif ((re.search("(^ )?OMG ", line)) != None):
        lexeme_tokens.append("OMG")
        lexeme_classification.append(
            KEYWROD_CONDT
        )
        token = "OMG"
    
    elif ((re.search("(^ )?OMGWTF$", line)) != None):
        lexeme_tokens.append("OMGWTF")
        lexeme_classification.append(
            KEYWROD_CONDT
        )
        token = "OMGWTF"

    # loop tokens

    elif ((re.search("(^ )?IM IN YR ", line)) != None):
        lexeme_tokens.append("IM IN YR")
        lexeme_classification.append(
            IDENTIFIER_LOOP
        )
        token = "IM IN YR"
    
    elif ((re.search("(^ )?IM OUTTA YR ", line)) != None):
        lexeme_tokens.append("IM OUTTA YR")
        lexeme_classification.append(
            IDENTIFIER_LOOP
        )
        token = "IM OUTTA YR"

    elif ((re.search(" UPPIN ", line)) != None):
        lexeme_tokens.append("UPPIN")
        lexeme_classification.append(
            KEYWORD_LOOP
        )
        token = "UPPIN"
    
    elif ((re.search(" NERFIN ", line)) != None):
        lexeme_tokens.append("NERFIN")
        lexeme_classification.append(
            KEYWORD_LOOP
        )
        token = "NERFIN"
    
    elif ((re.search(" TIL ", line)) != None):
        lexeme_tokens.append("TIL")
        lexeme_classification.append(
            KEYWORD_LOOP
        )
        token = "TIL"
    
    elif ((re.search(" WILE ", line)) != None):
        lexeme_tokens.append("WILE")
        lexeme_classification.append(
            KEYWORD_LOOP
        )
        token = "WILE"

    # function body tokens

    elif ((re.search("(^ )?HOW IZ I", line)) != None):
        lexeme_tokens.append("HOW IZ I")
        lexeme_classification.append(
            IDENTIFIER_FUNC
        )
        token = "HOW IZ I"
    
    elif ((re.search("(^ )?IF U SAY SO", line)) != None):
        lexeme_tokens.append("IF U SAY SO")
        lexeme_classification.append(
            IDENTIFIER_FUNC
        )
        token = "IF U SAY SO"
    
    elif ((re.search("(^ )?GTFO (.)", line)) != None):
        lexeme_tokens.append("GTFO")
        lexeme_classification.append(
            KEYWORD_FUNC
        )
        token = "GTFO"

    elif ((re.search("(^ )?FOUND YR (.)", line)) != None):
        lexeme_tokens.append("FOUND YR")
        lexeme_classification.append(
            KEYWORD_FUNC
        )
        token = "FOUND YR"
    
    elif ((re.search("(^ )?I IZ (.)", line)) != None):
        lexeme_tokens.append("I IZ")
        lexeme_classification.append(
            IDENTIFIER_FUNC
        )
        token = "I IZ"
    
    elif ((re.search(" MKAY$", line)) != None):
        lexeme_tokens.append("MKAY")
        lexeme_classification.append(\
            DELIMITER_END
        )
        token = "MKAY"
        
    # separators

    elif ((re.search(" YR ", line)) != None):
        lexeme_tokens.append("YR")
        lexeme_classification.append(
            KEYWORD_LOOP
        )
        token = "YR"

    elif ((re.search(" AN ", line)) != None):
        lexeme_tokens.append("AN")
        lexeme_classification.append(
            KEYWORD_SEPERATOR
        )
        token = "AN"

    # yarn literal: can catch multiple yarns in one line
    elif (re.search(r'["\'](.)*["\']', line) != None):

        #  https://docs.python.org/3/library/re.html
        yarn_substring = re.search(r'["\'](.)*["\']', line)
        yarn_literal = line[yarn_substring.start():yarn_substring.end()]

        lexeme_tokens.append('"')
        lexeme_tokens.append(yarn_literal.replace('"', ''))
        lexeme_tokens.append('"')

        lexeme_classification.append(
            DELIMITER_STR
        )
        lexeme_classification.append(
            LITERAL_YARN
        )
        lexeme_classification.append(
            DELIMITER_STR
        )
        token = yarn_literal
    
    # variable identifier
    elif (re.search("(^ )?[a-z]+([a-zA-Z\_\d])*", line) != None):

        # https://note.nkmk.me/en/python-re-match-object-span-group/
        # use start() and end() func to pinpoint location of literal in string line

        var_substring = re.search("(^ )?[a-z]+([a-zA-Z\_\d])*", line)

        variable_name = line[var_substring.start():var_substring.end()]
        if " " in variable_name:
            variable_name = variable_name.replace(" ", "")

        lexeme_tokens.append(variable_name)
        lexeme_classification.append(
            IDENTIFIER_VARS
        )
        token = variable_name

    # numbar / float literal
    elif (re.search(r'(\-)?\d+[\.]\d+', line) != None):

        float_substring = re.search(r'(\-)?\d+[\.]\d+', line)
        numbar_literal = line[float_substring.start():float_substring.end()]

        lexeme_tokens.append(numbar_literal)
        lexeme_classification.append(
            LITERAL_NUMBAR
        )
        token = numbar_literal

    # numbr / integer literal
    elif (re.search("(\-)?\d+", line) != None):

        num_substring = re.search("(\-)?\d+", line)
        # print(line[substring.start()])

        numbr_literal = line[num_substring.start():num_substring.end()]

        lexeme_tokens.append(numbr_literal)
        lexeme_classification.append(
            LITERAL_NUMBR
        )
        token = numbr_literal
    
    # troof literal
    elif (re.search("( WIN$| FAIL$)", line) != None):

        troof_susbtring = re.search("( WIN$| FAIL$)", line)
        troof_literal = line[troof_susbtring.start():troof_susbtring.end()]
        troof_literal = troof_literal.replace(" ", "")

        lexeme_tokens.append(troof_literal)
        lexeme_classification.append(
            LITERAL_TROOF
        )
        token = troof_literal

    # type literal
    elif (re.search("((.)?NUMBR |(.)?NUMBAR |(.)?YARN |(.)?TROOF )", line) != None):

        type_substring = re.search("((.)?NUMBR |(.)?NUMBAR |(.)?YARN |(.)?TROOF )", line)
        type_literal = line[type_substring.start():type_substring.end()]
        type_literal = type_literal.replace(" ", "")

        lexeme_tokens.append(type_literal)
        lexeme_classification.append(
            LITERAL
        )
        token = type_literal

    # return lexeme information details
    if len(lexeme_tokens) > 0 and len(lexeme_classification) > 0:
        if lexeme_classification[0] != DELIMITER_STR:
            # update global value of token descriptions
            token_list.append(lexeme_tokens[0])
            token_classification.append(lexeme_classification[0])

            # return values
            lexeme_information.append(lexeme_tokens[0])
            lexeme_information.append(lexeme_classification[0])
        
        # yarn string encountered
        else:
            # append string delimiters and other parts of yarn
            for x in lexeme_tokens: token_list.append(x)
            for y in lexeme_classification: token_classification.append(y)

            # return values
            lexeme_information.append('"' + lexeme_tokens[1] + '"')
            lexeme_information.append(lexeme_classification[1])
        
        # value to remove from line of code for checking
        lexeme_information.append(token)

    return lexeme_information

# end of func


# checkers
sample1 = """HAI
    WAZZUP
        BTW Declare Here
        I HAS A var1 ITZ 12
        I HAS A x ITZ 5
        I HAS A y ITZ 10
        I HAS A w ITZ 23
        I HAS A z ITZ 120
    BUHBYE

    MAEK var1 A NUMBAR

    SUM OF PRODUCKT OF PRODUCKT OF 3 AN 4 AN 2 AN 1

    I HAS A temp ITZ 2
    BTW prints 2 to 9 using TIL
    IM IN YR print10 UPPIN YR temp TIL BOTH SAEM temp AN 10
        VISIBLE temp
    IM OUTTA YR print10

    QUOSHUNT OF 5 AN "12"   BTW QUOSHUNT OF is division

    BTW at this point, temp's value is 10, so we must reassign its initial value
    temp R 2

    BOTH SAEM x AN BIGGER OF x AN y
    DIFFRINT z AN SMALLR OF z AN w
    ALL OF NOT x AN BOTH OF y AN z AN EITHER OF x AN y MKAY

    SMOOSH "Hello" AN "World"
    
    OBTW this
         Way
    TLDR

    BTW prints 2 to 9 but using WILE
    IM IN YR print10 UPPIN YR temp WILE DIFFRINT temp AN 10
        VISIBLE temp
    IM OUTTA YR print10
KTHXBYE
"""

sample2 = """HAI
    SUM OF PRODUCKT OF PRODUCKT OF 3 AN 4 AN 2 AN 1

    DIFFRINT 10 AN SMALLR OF 5
    O RLY?
        YA RLY
            VISIBLE "First number larger"
        NO WAI
            VISIBLE "Second number larger?"
    OIC

    BTW the previous one is an in-then statement

KTHXBYE
"""

sample3 = """HAI

    WTF?
    OMG a
        VISIBLE "It's a"    BTW ITS A
    OMGWTF
        VISIBLE "not a"     BTW NOT A
    OIC

    I HAS A temp ITZ 2
    BTW prints 2 to 9 using TIL
    IM IN YR print10 UPPIN YR temp TIL BOTH SAEM temp AN 10
        VISIBLE temp
    IM OUTTA YR print10

    BTW at this point, temp's value is 10, so we must reassign
    temp R 2

    IM IN YR print10 UPPIN YR temp TIL WILE DIFFRINT temp AN 10
        VISIBLE temp
    IM OUTTA YR print10

KTHXBYE
"""

sample4 = """HAI

    BTW here are functions in lolcode
    HOW IZ I no_parameters

    BTW function with 2 arguments
    HOW IZ I func_add YR x AN YR y
        GTFO SUM OF x AN y
    IF U SAY SO      
    
    I IZ func_add YR 22 AN YR -501.01 MKAY
    I HAS A true ITZ WIN
    
    VISIBLE "Yarn here"
    
KTHXBYE
"""

sample5 = """
HOW IZ I func_add YR x AN YR y
    GTFO SUM OF x AN y
IF U SAY SO      
BTW VALID COMMENT
HAI
    VISIBLE "Yarn here"     BTW PRINT
    I IZ func_add YR 22 AN YR -501.01 MKAY
    I HAS A str_string ITZ "Yarn Here"
KTHXBYE
"""


def lexical_tester(code):

    code = code.split("\n")
    code_line_num = 1

    checking_multiline_comments = 0

    for line in code:

        # reading current line
        line_information = []
        line_information.append(code_line_num)

        unsorted_lexemes = []

        no_space = line.split(" ")
        for val in no_space:
            if len(val) == 0 or re.search("\s", val):
                no_space.remove(val)
        # separate lines of code by space and count possible tokens

        possible_tokens = len(no_space)

        # we are checking the 'OBTW' instance
        if checking_multiline_comments == 1:

            if possible_tokens > 0:
                cleaned_line = " ".join(line.split(" "))
            
            for token in range(possible_tokens):
                token_details = detect_lexemes(cleaned_line)

                if len(token_details) > 0:
                    if token_details[1] == KEYWORD_COMMENT and token_details[2] == 'TLDR':
                        
                        # retrieves the 'TLDR' multiline ender
                        checking_multiline_comments = 0
                        cleaned_line = cleaned_line.replace('TLDR', "", 1)
                        if len(cleaned_line.replace(" ", "")) == 0:
                            token_details.pop()
                            line_information.append(token_details)
        
        # we are not checking the 'OBTW' instance, proceed
        else:
            # do not count in empty code lines
            if possible_tokens > 0:
                unsorted_lexemes_info = []
                cleaned_line = " ".join(line.split(" "))

                # check all possible tokens in a line of code
                for token in range(possible_tokens):

                    # returns list of lexeme description
                    token_details = detect_lexemes(cleaned_line)
                    
                    # should not be an empty line
                    if len(token_details) > 0:

                        # condition for OBTW comment
                        if token_details[1] == KEYWORD_COMMENT and 'OBTW' in token_details[2]:
                            checking_multiline_comments = 1

                        # condition for TLDR comment
                        if 'TLDR' in token_details[2]:
                            unsorted_lexemes_info.append(['TLDR', KEYWORD_COMMENT])
                            checking_multiline_comments = 0
                        
                        # condition for multiple YARNs in line
                        if token_details[1] == LITERAL_YARN:

                            # count if there are multiple string delimiters
                            string_delimiters = (token_details[2]).count('"')

                            # if there are multiple quotation marks, only retrieve one instance of yarn
                            if string_delimiters > 2:
                                clearing_extra_string = list(token_details[2])

                                # clears extra strings
                                while True:
                                    # string converted to list and continously pop the string list
                                    if clearing_extra_string[-1] == '"':

                                        # checks for multiple strings, make sure to get only first instance at start
                                        clearing_extra_string.pop()
                                        string_delimiters = string_delimiters - 1

                                        # already at the first instance of string
                                        if string_delimiters <= 2:
                                            clearing_extra_string.pop()
                                            break

                                    clearing_extra_string.pop()
                                
                                # include in the details only one instance of a yarn
                                token_details[2] = "".join(clearing_extra_string)
                                token_details[0] = "".join(clearing_extra_string)
                        
                        # end of condition for yarns

                        # add new details to the list of tokens and lexemes
                        remove_instance = token_details[2]
                        cleaned_line = cleaned_line.replace(remove_instance, "", 1)
                        token_details.pop()
                        unsorted_lexemes_info.append(token_details)

                    # repeat until all tokens are retrieved
                
                # sort lexemes based on its appearance in code
                if len(unsorted_lexemes_info) > 0:

                    # retrieve lexemes from information
                    for info in unsorted_lexemes_info:
                        unsorted_lexemes.append(info[0])
                
                    # retrieve indeces where lexemes are found
                    lexeme_indeces = []
                    lexeme_line = line
                    for lexeme in unsorted_lexemes:
                        index = lexeme_line.find(lexeme)

                        space_replace = ""
                        for i in range(0, len(lexeme)):
                            space_replace += " "
                        # remove isntance of lexeme, replace with spaces
                        lexeme_line = lexeme_line.replace(lexeme, space_replace, 1)
                        lexeme_indeces.append(index)
                    
                    # print(lexeme_indeces)
                    # print(unsorted_lexemes)

                    # bubble sorting algo
                    n = len(lexeme_indeces)
                    for i in range(n):
                        for j in range(n-1):
                            # sort indeces and lexeme order
                            if lexeme_indeces[j] > lexeme_indeces[j+1]:
                                temp = lexeme_indeces[j]
                                lexeme_indeces[j] = lexeme_indeces[j+1]
                                lexeme_indeces[j+1] = temp

                                temp_lexeme = unsorted_lexemes[j]
                                unsorted_lexemes[j] = unsorted_lexemes[j+1]
                                unsorted_lexemes[j+1] = temp_lexeme

                    sorted_lexemes = unsorted_lexemes

                    # print(lexeme_indeces)
                    # print(sorted_lexemes)
                    # print("")

                    for lexeme in sorted_lexemes:
                        for info in unsorted_lexemes_info:
                            if info[0] == lexeme:
                                line_information.append(info)
                                break

        code_per_line.append(line_information)
        code_line_num += 1
    # end of loop

    # # uncomment loop to check lexemes each line
    # for val in code_per_line:
    #     print(val)

    # # uncomment to check lexemes
    # print("\nList of Lexemes")
    # for x in range(len(token_list)):
    #     if (len(token_list[x])) > 6:    
    #         print(token_list[x], "\t", token_classification[x])
    #     else:
    #         print(token_list[x], "\t\t", token_classification[x])
    # print("")

    # print("Number of lexemes: " + str(len(token_list)))
    # print("Literals Count: " + str(token_classification.count(LITERAL)) + "\n")

    # returns array of tokens and its classifications
    return code_per_line


# uncomment one tester for testing
# lexical_tester(sample1)
# lexical_tester(sample2)
# lexical_tester(sample3)
# lexical_tester(sample4)
# lexical_tester(sample5)
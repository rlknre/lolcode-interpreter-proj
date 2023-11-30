
import re   # regex library

# https://www.w3schools.com/python/python_regex.asp
# findall	Returns a list containing all matches
# search	Returns a Match object if there is a match anywhere in the string
# split	    Returns a list where the string has been split at each match
# sub	    Replaces one or many matches with a string

# arrays for lexeme tracking
lexeme_tokens = []
lexeme_classification = []

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

# add function description here

def detect_lexemes(lexeme_tokens, lexeme_classification, line):

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

    elif (re.search("(.)? BTW (.)", line) != None):
        lexeme_tokens.append("BTW")
        lexeme_classification.append(
            KEYWORD_COMMENT
        )

        # also removes the comment line
        comment = line.split("BTW", 1)
        token = "BTW" + comment[1]

    # fix bug for OBTW, should clear out comment section until TLDR
    elif (re.search("(^ )?OBTW (.)", line) != None):
        lexeme_tokens.append("OBTW")
        lexeme_classification.append(
            KEYWORD_COMMENT
        )
        token = "OBTW"
    
    elif (re.search("(^ )?TLDR$", line) != None):
        lexeme_tokens.append("TLDR")
        lexeme_classification.append(
            KEYWORD_COMMENT
        )
        token = "TLDR"

    # yarn literal
    # BUG: not catching all strings in one line
    elif (re.search(r'["\'](.)+["\']', line) != None):

        #  https://docs.python.org/3/library/re.html
        yarn_substring = re.search(r'["\'](.)+["\']', line)
        yarn_literal = line[yarn_substring.start():yarn_substring.end()]

        lexeme_tokens.append('"')
        lexeme_tokens.append(yarn_literal.replace('"', ''))
        lexeme_tokens.append('"')

        lexeme_classification.append(
            DELIMITER_STR
        )
        lexeme_classification.append(
            LITERAL
        )
        lexeme_classification.append(
            DELIMITER_STR
        )
        token = yarn_literal

    # variable identifier
    elif (re.search("(^ )?[a-z]+[a-zA-Z\_\d]+ ", line) != None):

        # https://note.nkmk.me/en/python-re-match-object-span-group/
        # use start() and end() func to pinpoint location of literal in string line

        var_substring = re.search("(^ )?[a-z]+[a-zA-Z\_\d]+ ", line)

        variable_name = line[var_substring.start():var_substring.end()]

        lexeme_tokens.append(variable_name)
        lexeme_classification.append(
            IDENTIFIER_VARS
        )
        token = variable_name

    # numbr / integer literal
    elif (re.search(" (\-)?\d", line) != None):

        num_substring = re.search(" (\-)?\d+", line)
        # print(line[substring.start()])

        numbr_literal = line[num_substring.start():num_substring.end()]

        lexeme_tokens.append(numbr_literal)
        lexeme_classification.append(
            LITERAL
        )
        token = numbr_literal
    
    # numbar / float literal
    # BUG: doesn't catch the dot and separates the fractional part from the whole
    elif (re.search(r' (\-)?\d+[\.]{1}\d+ ', line) != None):

        float_substring = re.search(r' (\-)?\d+[\.]{1}\d+', line)
        numbar_literal = line[float_substring.start():float_substring.end()]

        lexeme_tokens.append(numbar_literal)
        lexeme_classification.append(
            LITERAL
        )
        token = numbar_literal
    
    # troof literal
    elif (re.search("(WIN|FAIL)", line) != None):

        troof_susbtring = re.search("(WIN|FAIL)", line)
        troof_literal = line[troof_susbtring.start():troof_susbtring.end()]

        lexeme_tokens.append(troof_literal)
        lexeme_classification.append(
            LITERAL
        )
        token = troof_literal

    # type literal
    elif (re.search("(NUMBR|NUMBAR|YARN|TROOF)", line) != None):

        type_substring = re.search("(NUMBR|NUMBAR|YARN|TROOF)", line)
        type_literal = line[type_substring.start():type_substring.end()]

        lexeme_tokens.append(type_literal)
        lexeme_classification.append(
            LITERAL
        )
        token = type_literal


    # variable declaration section tokens

    elif (re.search("(.)WAZZUP$", line) != None):
        lexeme_tokens.append("WAZZUP")
        lexeme_classification.append(
            DELIMITER_VAR
        )
        token = "WAZZUP"

    elif (re.search("(.)BUHBYE$", line) != None):
        lexeme_tokens.append("BUHBYE")
        lexeme_classification.append(
            DELIMITER_VAR
        )
        token = "BUHBYE"

    # assignment operations 1

    elif (re.search("(^ )? I HAS A (.)", line) != None):
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
    
    elif ((re.search(" AN ", line)) != None):
        lexeme_tokens.append("AN")
        lexeme_classification.append(
            KEYWORD_SEPERATOR
        )
        token = "AN"

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
    
    elif ((re.search(" \+ ", line)) != None):
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
    
    elif ((re.search(" YR ", line)) != None):
        lexeme_tokens.append("YR")
        lexeme_classification.append(
            KEYWORD_LOOP
        )
        token = "YR"
    
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

    elif ((re.search("(^ )?HOW IZ I ", line)) != None):
        lexeme_tokens.append("HOW IZ I")
        lexeme_classification.append(
            IDENTIFIER_FUNC
        )
        token = "HOW IZ I"
    
    elif ((re.search("(^ )?IF U SAY SO ", line)) != None):
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
        lexeme_tokens.append("I IZ ")
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

    # this will be trimmed from the line passed here
    return token

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

sample5 = """HAI

    VISIBLE "Yarn here"

KTHXBYE
"""

# separate_lines = sample1.split("\n")
# separate_lines = sample2.split("\n")
# separate_lines = sample3.split("\n")
separate_lines = sample4.split("\n")
# separate_lines = sample5.split("\n")

for line in separate_lines:

    no_space = line.split(" ")
    for val in no_space:
        if len(val) == 0 or re.search("\s", val):
            no_space.remove(val)
    # separate lines of code by space and count possible tokens

    possible_tokens = len(no_space)

    # do not count in empty code lines
    if possible_tokens > 0:
        cleaned_line = " ".join(line.split(" "))

        # check all possible tokens in a line of code
        for token in range(possible_tokens):
            token_found = detect_lexemes(lexeme_tokens, lexeme_classification, cleaned_line)
            cleaned_line = cleaned_line.replace(token_found, "", 1)
        # appends to list of tokens

# end of loop


# check lexemes
print("\nList of Lexemes")
for x in range(len(lexeme_tokens)):
    if (len(lexeme_tokens[x])) > 6:    
        print(lexeme_tokens[x], "\t", lexeme_classification[x])
    else:
        print(lexeme_tokens[x], "\t\t", lexeme_classification[x])
print("")

print("Number of lexemes: " + str(len(lexeme_tokens)))
print("Literals Count: " + str(lexeme_classification.count(LITERAL)) + "\n")

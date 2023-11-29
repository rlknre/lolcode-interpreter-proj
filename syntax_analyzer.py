
from lexical_analyzer import detect_lexemes
from lexical_analyzer import lexeme_tokens, lexeme_classification

test = lexeme_tokens

# test if code delimiter syntax of lolcode is valid
def valid_code(code):
    if (code[0] != "HAI" and code[-1] != "KTHXBYE"):
        return 0
    return 1

if (valid_code(test) == 1):
    print("valid lolcode")

else:
    print("\ninvalid lolcode. \n")

print("")

# NOTES FROM MAAM:
# syntax == is the code correct? are variables correctly initialized?
# semantic == operations, how the operations work like PRINT 

# 1. Make sure to update Python first perform:     python -V
# 2. To install the UI library perform:            pip install tk

# https://www.youtube.com/watch?v=TuLxsvK4svQ
# https://www.youtube.com/watch?v=reJ8kTqQsTY
# https://www.geeksforgeeks.org/how-to-set-a-tkinter-window-with-a-constant-size/
# https://docs.python.org/3/library/tk.html
# https://realpython.com/python-gui-tkinter/
# https://stackoverflow.com/questions/68547433/window-is-not-showing-up-at-all-in-vscode-tkinter

# ----------------------------------------------------------------------------------------------------------------------------------------------

# Import libraries for Tkinter user interface
from tkinter import *

# Import the analyzers
from lexical_analyzer import lexical_tester
from syntax_analyzer import syntax_tester
from semantic_analyzer import semantic_perform

# From the Lexical Analyzer, lists for the token table
from lexical_analyzer import token_list
from lexical_analyzer import token_classification

# From the Syntax Analyzer, list of (possible) syntax errors
from syntax_analyzer import errors

# From the Semantic Analyzer, lists for the symbol table and semantic errors
from semantic_analyzer import symbol_table_identifiers
from semantic_analyzer import symbol_table_values
from semantic_analyzer import semantic_errors

# ----------------------------------------------------------------------------------------------------------------------------------------------

sample = """HAI


KTHXBYE"""

def execute_lolcode():
    # check if lexical test found a lexeme
    found_lexeme = 0
    lexical_test = lexical_tester(sample)
    for line in lexical_test:
        if len(line) > 1:
            found_lexeme = 1
            break

    if found_lexeme == 1:
        syntax_test = syntax_tester(lexical_test)

        # check if return value of syntax is correct
        if len(syntax_test) != 2:
            print("\nInvalid\n")

        else:
            syntax_check = syntax_test[1]

            # no errors in code
            if syntax_check == 1:
                code_block = syntax_test[0]

                # run code here
                print("")
                semantic_perform(code_block)
                print("")
                
            # syntax errors
            else:
                if len(errors) > 0:
                    for error in errors:
                        print(error)
                    print("")


# ----------------------------------------------------------------------------------------------------------------------------------------------

window = Tk()       # instantiates a new window

# adjust the visuals here
window.geometry("1080x740")
window.resizable(0, 0)

window.config(background="#D3D3D3")
window.title('LOLCODE INTERPRETER')

# Top Frame
topFrame = Frame(window, width=1080, height=355, bg="#77DD77")
topFrame.grid(row=0)

# Workspace
spaceFrame = Frame(topFrame, width=500, height=340, bg="#77DD77")
spaceFrame.grid(row=0, column=0)

# Token Table
tokenFrame = Frame(topFrame, width=290, height=340, bg="#D5E3F0")
tokenFrame.grid(row=0, column=1)

# Symbol Table
symbolFrame = Frame(topFrame, width=290, height=340, bg="#3A3845")
symbolFrame.grid(row=0, column=2)

# Execute Button Frame
buttomFrame = Frame(window, width=1080, height=50, bg="#D3D3D3")
buttomFrame.grid(row=1)

execute_button = Button(
    buttomFrame,
    text='EXECUTE',
    #command
    font = ("Roboto", 10),
    width=150,
    bg="#D3D3D3"
)
execute_button.pack(pady=8.5)

# Terminal
terminalFrame = Frame(window, width=1080, height=355, bg="#C3B1E1")
terminalFrame.grid(row=2)


window.mainloop()   # displays the window

# 1. Make sure to update Python first perform:     python -V
# 2. To install the UI library perform:            pip install tk

# https://www.youtube.com/watch?v=TuLxsvK4svQ
# https://www.youtube.com/watch?v=reJ8kTqQsTY
# https://stackoverflow.com/questions/30517089/scrollbar-to-scroll-text-widget-using-grid-layout-in-tkinter
# https://stackoverflow.com/questions/29041593/tkinter-python-treeview-change-header
# https://stackoverflow.com/questions/44659879/ttk-button-span-multiple-columns
# https://www.geeksforgeeks.org/python-tkinter-label/
# https://stackoverflow.com/questions/3842155/is-there-a-way-to-make-the-tkinter-text-widget-read-only
# https://www.geeksforgeeks.org/how-to-set-a-tkinter-window-with-a-constant-size/
# https://docs.python.org/3/library/tk.html
# https://realpython.com/python-gui-tkinter/
# https://stackoverflow.com/questions/68547433/window-is-not-showing-up-at-all-in-vscode-tkinter

# ----------------------------------------------------------------------------------------------------------------------------------------------

# Import libraries for Tkinter user interface
from tkinter import *
from tkinter import ttk

# Import the analyzers
from lexical_analyzer import lexical_tester
from syntax_analyzer import syntax_tester
from semantic_analyzer import semantic_perform

# From the Syntax Analyzer, list of cleaned token list and (possible) errors
from syntax_analyzer import lexeme_tokens
from syntax_analyzer import lexeme_classifications
from syntax_analyzer import errors

# From the Semantic Analyzer, lists for the symbol table and semantic errors
from semantic_analyzer import symbol_table_identifiers
from semantic_analyzer import symbol_table_values
from semantic_analyzer import semantic_errors

# ----------------------------------------------------------------------------------------------------------------------------------------------

sample = """BTW start of the program
HAI
WAZZUP
BTW variable dec
I HAS A monde
I HAS A num ITZ 17
I HAS A name ITZ "seventeen"
I HAS A fnum ITZ 17.0
I HAS A flag ITZ WIN
        
I HAS A sum ITZ SUM OF num AN 13
I HAS A diff ITZ DIFF OF sum AN 17
I HAS A prod ITZ PRODUKT OF 3 AN 4
I HAS A quo ITZ QUOSHUNT OF 4 AN 5
BUHBYE

BTW print literals and variables
VISIBLE "declarations"
VISIBLE monde BTW should be NOOB
VISIBLE num
VISIBLE name
VISIBLE fnum
VISIBLE flag

VISIBLE sum
VISIBLE diff
VISIBLE prod
VISIBLE quo

BTW print expressions
VISIBLE SUM OF PRODUKT OF 3 AN 5 AN BIGGR OF DIFF OF 17 AN 2 AN 5
VISIBLE BIGGR OF PRODUKT OF 11 AN 2 AN QUOSHUNT OF SUM OF 3 AN 5 AN 2
KTHXBYE"""

def execute_lolcode(lexeme_table, symbols_table):
    # check if lexical test found a lexeme
    found_lexeme = 0
    lexical_test = lexical_tester(sample)
    for line in lexical_test:
        if len(line) > 1:
            found_lexeme = 1
            break

    if found_lexeme == 1:

        if len(lexeme_tokens) == len(lexeme_classifications):

            syntax_test = syntax_tester(lexical_test)

            # check if return value of syntax is correct
            if len(syntax_test) != 2:
                print("\nInvalid\n")

            else:
                syntax_check = syntax_test[1]

                # add values to lexeme table
                for i in range(len(lexeme_tokens)):
                    lexeme_table.insert('', 'end', values = (lexeme_tokens[i], lexeme_classifications[i]))

                # no errors in code
                if syntax_check == 1:
                    code_block = syntax_test[0]

                    # run code here
                    print("")
                    semantic_perform(code_block)
                    print("")

                    # add values to symbols table
                    for i in range(len(symbol_table_identifiers)):
                        symbols_table.insert('', 'end', values = (symbol_table_identifiers[i], symbol_table_values[i]))
                
                # syntax errors
                else:
                    if len(errors) > 0:
                        for error in errors:
                            print(error)
                        print("")


# ----------------------------------------------------------------------------------------------------------------------------------------------

window = Tk()       # instantiates a new window

# adjust the visuals here
# window.geometry("1080x740")
window.resizable(0, 0)

window.config(background="#D3D3D3")
window.title('LOLCODE INTERPRETER')


# Workspace Area

file_explorer = Label(window, text="None", width=50, bg="white")
file_explorer.grid(row=0, column=0, padx=8, pady=4)

file_explorer_button = Button(window, text="Select File", bg="white", width=20)
file_explorer_button.grid(row=0, column=1, pady=4)

workspace = Text(window, width=65, height=15)
workspace.grid(row=1, column=0, columnspan=2, padx=8, pady=1)


# Lexemes Area

lexeme_header = Label(window, text="Lexemes", width=50, bg="#D3D3D3")
lexeme_header.grid(row=0, column=2, padx=8, pady=4)

lexeme_frame = Frame(window)
lexeme_frame.grid(row=1, column=2, padx=8, pady=4)

lexeme_frame_table = ttk.Treeview(
    lexeme_frame,
    height=11,
    show="headings",
    columns=["Lexeme", "Classification"]
)
lexeme_frame_table.grid(row=0, column=0)
lexeme_frame_table.column("#1", anchor=CENTER)
lexeme_frame_table.column("#2", anchor=CENTER)
lexeme_frame_table.heading("#1", text="Lexeme")
lexeme_frame_table.heading("#2", text="Classification")

lexeme_scrollbar = ttk.Scrollbar(
    lexeme_frame,
    orient="vertical",
    command=lexeme_frame_table.yview
)

lexeme_frame_table.configure(yscroll=lexeme_scrollbar.set)
lexeme_scrollbar.grid(row=0, column=2, rowspan=2, sticky=N+S+W)


# Symbols Area

symbols_header = Label(window, text="Symbol Table", width=50, bg="#D3D3D3")
symbols_header.grid(row=0, column=3, padx=8, pady=4)

symbols_frame = Frame(window)
symbols_frame.grid(row=1, column=3, padx=8, pady=4)

symbols_frame_table = ttk.Treeview(
    symbols_frame,
    height=11,
    show="headings",
    columns=["Identifier", "Value"]
)
symbols_frame_table.grid(row=0, column=0)
symbols_frame_table.column("#0", anchor=CENTER)
symbols_frame_table.column("#1", anchor=CENTER)
symbols_frame_table.heading("#1", text="Identifier")
symbols_frame_table.heading("#2", text="Value")

symbols_scrollbar = ttk.Scrollbar(
    symbols_frame,
    orient="vertical",
    command=symbols_frame_table.yview
)

symbols_frame_table.configure(yscroll=symbols_scrollbar.set)
symbols_scrollbar.grid(row=0, column=2, rowspan=2, sticky=N+S+W)


# Execute Area

buttom_frame = Frame(window)
buttom_frame.grid(row=2, columnspan=6, padx=8, pady=4)

execute_button = Button(
    buttom_frame,
    text="EXECUTE", 
    width=198, 
    command=lambda: execute_lolcode(lexeme_frame_table, symbols_frame_table)
).grid()


# Console Area

console_box = Text(window, width=175, height=20)
console_box.configure(state="disabled")
console_box.grid(row=3, column=0, columnspan=6, padx=8, pady=8)


window.mainloop()   # displays the window
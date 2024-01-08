
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
# https://www.geeksforgeeks.org/file-explorer-in-python-using-tkinter/
# https://www.tutorialspoint.com/how-to-make-the-tkinter-text-widget-read-only

# ----------------------------------------------------------------------------------------------------------------------------------------------

# Import libraries for Tkinter user interface
# from tkinter import *
import tkinter as tk
from tkinter import ttk             # treeview
from tkinter import filedialog      # file dialog

# Import the analyzers
from lexical_analyzer import lexical_tester
from syntax_analyzer import syntax_tester
from semantic_analyzer import semantic_perform

# ----------------------------------------------------------------------------------------------------------------------------------------------

def execute_lolcode(input_code, lexeme_table, symbols_table, terminal):

    # refresh terminal
    terminal.configure(state="normal")      # makes text area editable
    terminal.delete("1.0", 'end')           # delete contents of terminal
    terminal.configure(state="disabled")    # disable editing again

    # refresh lexeme table
    selected_lexemes = lexeme_table.get_children()
    for lexeme in selected_lexemes:
        lexeme_table.delete(lexeme)
    
    # refresh symbol table
    selected_symbols = symbols_table.get_children()
    for item in selected_symbols:
        symbols_table.delete(item)

    # check if lexical test found a lexeme
    found_lexeme = 0
    lexical_test = []
    lexical_test = lexical_tester(input_code)

    for line in lexical_test:
        if len(line) > 1:
            found_lexeme = 1
            break

    if found_lexeme == 1:
        # check if return value of syntax is correct

        syntax_test = []
        syntax_test = syntax_tester(lexical_test)
        # returns [code_block, valid_syntax, lexeme_tokens, lexeme_classifications, errors]

        if len(syntax_test) != 5:
            print("\nInvalid\n")
        else:
            # do a syntax check
            syntax_check = syntax_test[1]
            lexeme_tokens = syntax_test[2]
            lexeme_classifications = syntax_test[3]
            syntax_errors = syntax_test[4]
                    
            # add values to lexeme table
            for i in range(len(lexeme_tokens)):
                lexeme_table.insert('', 'end', values = (lexeme_tokens[i], lexeme_classifications[i]))
            
            if len(syntax_errors) >= 1:

                # print syntax errors
                print_errors_to_terminal = ''
                for error in syntax_errors:
                    print_errors_to_terminal = print_errors_to_terminal + str(error) + '\n'
                    print(error)
                print("")

                terminal.configure(state="normal")      # makes text area editable
                terminal.delete("1.0", 'end')           # delete contents of terminal
                terminal.insert('end', print_errors_to_terminal)
                terminal.configure(state="disabled")    # disable editing again

            # no errors
            else:
                if syntax_check == 1:
                    code_block = syntax_test[0]
                    semantic_check = []

                    # run code here
                    print("")
                    semantic_check = semantic_perform(code_block)
                    print("")

                    # returns [symbol_table_identifiers, symbol_table_values, lines_to_print, errors]
                    
                    if len(semantic_check) == 4:

                        # do a semantic check
                        symbol_table_identifiers = semantic_check[0]
                        symbol_table_values = semantic_check[1]
                        lines_to_print = semantic_check[2]
                        semantic_errors = semantic_check[3]

                        if len(semantic_errors) >= 1:

                            # print syntax errors
                            print_errors_to_terminal = ''
                            for error in semantic_errors:
                                print_errors_to_terminal = print_errors_to_terminal + str(error) + '\n'
                                print(error)
                            print("")

                            terminal.configure(state="normal")      # makes text area editable
                            terminal.delete("1.0", 'end')           # delete contents of terminal
                            terminal.insert('end', print_errors_to_terminal)
                            terminal.configure(state="disabled")    # disable editing again
                        
                        # run code if semantic is valid
                        else:

                            # add values to symbols table
                            for i in range(len(symbol_table_identifiers)):
                                symbols_table.insert('', 'end', values = (symbol_table_identifiers[i], symbol_table_values[i]))

                            terminal.configure(state="normal")      # makes text area editable
                            terminal.delete("1.0", 'end')           # delete contents of terminal
                            terminal.insert('end', lines_to_print)
                            terminal.configure(state="disabled")    # disable editing again
                    
                    # mistake in semantic analyzer catcher
                    else:
                        print("Invalid semantic check")

# ----------------------------------------------------------------------------------------------------------------------------------------------

# opens a dialog box to retreive a file
def browse_files(file_explorer_label, workspace):

    filename = ''
    # opens dialog box
    filename = filedialog.askopenfilename(
        initialdir = "/",
        title = "Select a File",
        filetypes = ( ("LOL files", "*.lol*"), ("all files", "*.*") )
    )
    if filename != '':
        # make changes in the text editor
        file_explorer_label.configure(text="File Opened: " + filename)  # change label header
        workspace.delete("1.0", 'end')  # delete contents of workspace

        # read the file and isnert contents to text editor
        read_file = open(filename, "r")
        file_text = read_file.read()
        workspace.insert('end', file_text)
        read_file.close()
      

# retrieves value in workspace area
def retrieve_input(workspace):
    input = workspace.get('1.0', 'end')
    return input


window = tk.Tk()       # instantiates a new window

# adjust the visuals here
# window.geometry("1080x740")
window.resizable(0, 0)

window.config(background="#D3D3D3")
window.title('LOLCODE INTERPRETER')


# Workspace Area

file_explorer_button = tk.Button(
    window, 
    text="Select File", 
    bg="white", 
    width=20,
    command=lambda: {
        browse_files(file_explorer, workspace_area)
    }
)
file_explorer_button.grid(row=0, column=1, pady=4)

workspace_area = tk.Text(window, width=65, height=15)
workspace_area.grid(row=1, column=0, columnspan=2, padx=8, pady=1)

file_explorer = tk.Label(window, text="None", width=50, bg="white")
file_explorer.grid(row=0, column=0, padx=8, pady=4)


# Lexemes Area

lexeme_header = tk.Label(window, text="Lexemes", width=50, bg="#D3D3D3")
lexeme_header.grid(row=0, column=2, padx=8, pady=4)

lexeme_frame = tk.Frame(window)
lexeme_frame.grid(row=1, column=2, padx=8, pady=4)

lexeme_frame_table = ttk.Treeview(
    lexeme_frame,
    height=11,
    show="headings",
    columns=["Lexeme", "Classification"]
)
lexeme_frame_table.grid(row=0, column=0)
lexeme_frame_table.column("# 1", anchor="center")
lexeme_frame_table.column("# 2", anchor="center")
lexeme_frame_table.heading("# 1", text="Lexeme")
lexeme_frame_table.heading("# 2", text="Classification")

lexeme_scrollbar = ttk.Scrollbar(
    lexeme_frame,
    orient="vertical",
    command=lexeme_frame_table.yview
)

lexeme_frame_table.configure(yscroll=lexeme_scrollbar.set)
lexeme_scrollbar.grid(row=0, column=2, rowspan=2, sticky="nsw")


# Symbols Area

symbols_header = tk.Label(window, text="Symbol Table", width=50, bg="#D3D3D3")
symbols_header.grid(row=0, column=3, padx=8, pady=4)

symbols_frame = tk.Frame(window)
symbols_frame.grid(row=1, column=3, padx=8, pady=4)

symbols_frame_table = ttk.Treeview(
    symbols_frame,
    height=11,
    show="headings",
    columns=["Identifier", "Value"]
)
symbols_frame_table.grid(row=0, column=0)
symbols_frame_table.column("# 0", anchor="center")
symbols_frame_table.column("# 1", anchor="center")
symbols_frame_table.heading("# 1", text="Identifier")
symbols_frame_table.heading("# 2", text="Value")

symbols_scrollbar = ttk.Scrollbar(
    symbols_frame,
    orient="vertical",
    command=symbols_frame_table.yview
)

symbols_frame_table.configure(yscroll=symbols_scrollbar.set)
symbols_scrollbar.grid(row=0, column=2, rowspan=2,sticky="nsw")


# Execute Area

buttom_frame = tk.Frame(window)
buttom_frame.grid(row=2, columnspan=6, padx=8, pady=4)

execute_button = tk.Button(
    buttom_frame,
    text="EXECUTE", 
    width=198, 
    command=lambda: {
        execute_lolcode(retrieve_input(workspace_area), lexeme_frame_table, symbols_frame_table, console_box),
    }
).grid()


# Console Area

# initially uneditable to avoid any changes
console_box = tk.Text(window, width=175, height=20)
console_box.configure(state="disabled")
console_box.grid(row=3, column=0, columnspan=6, padx=8, pady=8)

window.mainloop()   # displays the window
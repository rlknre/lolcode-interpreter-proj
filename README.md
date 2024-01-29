
# LOLCODE INTERPRETER

![Python][py-md-badge]

A **_LOLCODE interpreter_** application written in Python. Note that this project does not fully interprets all of LOLCODE programming language functionalities. For indentation, use _spaces_ instead of tab, you may not include indents as well.
- ``Lexical Analyzer`` uses RegEx to obtain lexeme tokens.
- ``Syntax Analyzer`` catches errors regarding syntax per line.
- ``Semantic Analyzer`` performs the LOLCODE.
- ``main.py`` initializes the user interface.
<br />

## Table of Contents
1. [Requirements](#requirements)
2. [How to Run](#instructions)
3. [Other Notes](#note)
<br />

## Requirements <a name="requirements"></a>
1. Ensure that the system has Python. You may check the Python site for installation. 

2. After installing, open your terminal and type in the following to install the **Tkinter library**.
    - ``pip install tk``

3. When downloading the files, make sure this directory tree is followed:

   ```
    lolcode-interpreter-proj
    ├── main.py
    ├── src
    │   ├── __pycache__
    │   ├── __init__.py
    │   ├── keywords.py
    │   ├── lexical_analyzer.py
    │   ├── semantic_analyzer.py
    │   └── syntax_analyzer.py
    └── README.md
   ```
<br />

## Running Project <a name="instructions"></a>
1. To run the program, proceed to the directory of the files with ``main.py`` and run the project using the command:
    - ``python3 main.py``

2. A screen will pop out, which is the **_LOLCODE Interpreter_** application.

3. The top-leftmost section is your workspace area, take note of the following areas:
    - _File Selector_
        - You may select a LOL file by clicking the *Select File* button
        - The contents of the file will reflect on the workspace 
    - _Workspace Area_
        - This is where the LOLCODE is displayed.
        - Contents in this area is editable.

4. Once you are satisfied with the code in your workspace, click the **execute** button in the middle.
    - The bottom portion is the terminal, input/output/errors will be displayed here.
    - For user input, a dialog box will appear in your screen.

5. The top-righmost section is your data area. Lexeme information and variable values are displayed here upon execution of LOLCODE.
<br />

##
### Author
- Ralph Kenneth Rea

##
### Other Notes <a name="note"></a>
- This project is in fulfillment of the requirements in CMSC 124: Design and Implementation of Programming Languages. UPLB.
- The interpreter is incomplete, missing some semantic rules. Indentation may or may not work at times.
- Note that there are still bugs in the analyzer files.
- The analyzers are not modularized enough.

[py-md-badge]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54

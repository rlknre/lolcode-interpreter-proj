
# LOLCODE INTERPRETER

![Python][py-md-badge]

A **_LOLCODE interpreter_** application written in Python. Note that this project only interprets some functionalities of the LOLCODE programming language and does not fully run all of its available syntax. Use _spaces_ for indentation instead of tab. 

<br />

## Requirements
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

## Running Project
1. To run the program, proceed to the directory of the files with ``main.py`` and run the project using the command:
    - ``python3 main.py``

2. A screen will pop out, which is the **_LOLCODE Interpreter_** application.

3. The top-leftmost section is your workspace area, take note of the following areas:
    - _File Selector_
        - You may select a LOL file by clicking the *Select File* button
        - The contents of the file will reflect on the workspace 
    - _Workspace Area_
        - This is where the LoLcode is displayed.
        - Contents in this area is editable.

4. Once you are satisfied with the LoLcode in your workspace, click the **execute** button in the middle.
    - The bottom portion is the terminal, input/output/errors will be displayed here.
    - For user input, a dialog box will appear in your screen.
<br />

##
### Author
- Ralph Kenneth Rea

##
### Other Notes
- This project is in fulfillment of the requirements in CMSC 124: Design and Implementation of Programming Languages. UPLB.
- The interpreter is incomplete and is missing some of its semantic rules. Indentation may or may not work at times.
- Note that there are still bugs in the other analyzer files.
- The analyzers are not modularized enough.

[py-md-badge]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54

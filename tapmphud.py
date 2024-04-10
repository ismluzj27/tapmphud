# tapmphud.py
# "ta-pum-fud"

import random
import json

from sys import stdin

border_design = "------<><><>------<><>------<><><>------<><>------<><><>------"
border_design1 = "-----<~~~~>-----<~~~~>-----<~~~~>-----<~~~~>-----<~~~~>-----"
border_design2 = "-~-~-</^\\>-~-~-</^\\>-~-~-</^\\>-~-~-</^\\>-~-~-</^\\>-~-~-</^\\>"
border_design3 = "---<<<~~~^^^~~~>>>------<<<~~~^^^~~~>>>------<<<~~~^^^~~~>>>---"


def border():  # choose randomly between the borders and print
    borders = [border_design,  # create a list of borders
                border_design1,
                border_design2,
                border_design3]
    print(random.choice(borders),"\n")


# TODO: implement all asterisks
help = """\033[34mThis is the help menu, all available commands that you can use are here. 

The first category of commands is entitled \033[32m## Universal ##\033[0m: 
\033[34mThese are the most common commands you will use.

The next category of commands is entitled \033[33m## Navigation ##\033[0m:
\033[34mThese are uses to word your way through and around the syllabus which has been pre-made for your convenience.
There is also a display demonstrating the structure of the syllabus.

The following category of commands is entitled \033[35m## Modifying syllabus ##\033[0m:
\033[34mAs the name suggests this will allow you to alter or add to the existing syllabus.

The last category of commands is entitled \033[36m## Exporting and importing to file ##\033[0m:
\033[34mThese commands allow you to make/load a file to/from your computer respectively.\033[0m


\033[32m## Universal ##\033[0m
\033[34m\033[4mexit\033[0m - exit
\033[34m\033[4mhelp\033[0m - list commands
\033[34m\033[4mflashcard-review\033[0m - Generate quiz based on syllabus
\033[34m\033[4msearch [term]\033[0m - Look for and show any matches to term within **your current directory**.
\033[34m\033[4msort\033[0m - bubble sort vocabulary alphabetically

\033[33m## Navigation ##\033[0m
\033[34m\033[4mpwd\033[0m - print working directory
\033[34m\033[4mls\033[0m - list all elements in working directory
\033[34m\033[4mls [element]\033[0m - list all elements in specified list/dictionary
\033[34m\033[4mread [key OR index]\033[0m - print the value of a key/at index of list
\033[34m\033[4minto [element]\033[0m - select an element in current working directory
\033[34m\033[4moutof\033[0m - go up in the working directory into broader element

\033[0mSyllabus structure:
> Unit > Topic > Vocabulary
               > Notecards

\033[35m## Modifying syllabus ##\033[0m
\033[34m\033[4madd-vterm [term name]\033[0m - add vocabulary term w/ def & notes (at working directory's topic)
\033[34m\033[4madd-ncard (asks for user input)\033[0m - add a notecard (at working directory's topic) 
\033[34m\033[4madd-topic [topic name]\033[0m - add a topic (at working directory's unit)
\033[34m\033[4madd-unit [unit name]\033[0m - Make an empty unit with name provided
\033[34m\033[4msetkey [key/index] (asks for user input)\033[0m - replace content at key or index with user input
\033[34m\033[4mdel [element name]\033[0m - delete any key/dict/str. can be a unit, topic, vocab term, note, etc.

\033[36m## Exporting and importing to file ##\033[0m
\033[34m\033[4mwrite-file [filename]\033[0m - Write current syllabus to the specified file (JSON format)
\033[34m\033[4mload-file [filename]\033[0m - Load syllabus from specified file (JSON format)"""  # * = NOT IMPLEMENTED

# SEE: planning.txt for structure.
syllabus = {
    'Python Basics': {  # unit
        'Data Types': {  # topic
            'vocab': {
                'String': {
                    'definition': 'A sequence of characters enclosed within either single quotes (' ') or double quotes (" ").',
                    'notes': "fstring is when you add an 'f' immediately before the quotation mark.\nThis allows for you pyhton to recognize variables in the string under ceartain conditions.",
                },
                'Integers': {
                    'definition': 'Zero, positive or negative whole numbers without a fractional/decimal part.',
                    'notes': "Can't have:\n" +
                    " - Decimal point\n" +
                    " - Letters or other non number characters"
                },
                'Float': {
                    'definition': 'Numbers are decimal values or fractional numbers.',
                    'notes': "Floats don't need to always have a decimal point, it can contain an integer and still be set as a float.",
                },
                'Boolean': {
                    'definition': 'A 1 or 0 value indicating a variety of things.',
                    'notes': "Used commonly for:\n"
                    " - Binary\n" +
                    " - True or False\n" +
                    " - Yes or No"
                }
            },
            'notecards': [  # group relevant information together
                "4 main data types: String, Float, Integer, Boolean",  # 0
                "Datatype Restrictions.\n" +
                " - String\n" +
                "   * All things in string are binded together, difficult to separate things.\n" +
                " - Integer\n" +
                "   * Can't contain decimal point.\n" +
                " - Float\n" +
                "   * Can't contain any other characters but numbers",  # 1
                "Other Data types\n" +
                "Sequence Data Types\n" +
                " 1) list\n" +
                "   * [] and , are used in list data type\n" +
                " 2) tuple\n" +
                "   * () and , are used in tuple data type",  # 2
            ]
        }
    }
}

# print(syllabus['7 Cities']['1 Orig Dist Sys Cities']['notes'][1])
#              >Unit    >Topic
working_dir = ">Python Basics>Data Types"
raw_input_prompt = """
--- Leave blank to cancel ---
---   Type EOF to stop    ---"""

# print(json.dumps(syllabus))

# returns the selected object
# e.g. syllabus['7 Cities']

# Return the object associated with the working directory.
def resolve_wd():
    return resolve_dir(working_dir)

# Given a path, return the object that is at that path.
# e.g. given >Python Basics>Data Types"
#   ...returns syllabus["Python Basics"]["Data Types"]
def resolve_dir(str_):
    # Start off at the syllabus object.
    selected = syllabus
    # discard first '>' to avoid first split being ""
    strx = str_.removeprefix(">")
    if strx == '':
        # If the working directory is just ">",
        # return the syllabus object.
        return syllabus
    # For each term separated by '>',
    for i, v in enumerate(strx.split('>')):
        # if the term is found within the selected object,
        if v in selected:
            # move into the object and continue the loop.
            selected = selected[v]
        else:
            # If not found... print following message and return object.
            print(f"Element {v} not found-- stopping resolve")
            return selected

    # Return the final object.
    return selected

# Extract the topic from the working directory (a string).
def wd_get_topic():
    # Let interpreter know that `working_dir` is found globally
    global working_dir
    # >unit>topic
    # Get the topic from the current working directory.
    # The topic will be the 2nd term (index 1) split by '>'.
    # Split the string by '>'.
    elements = working_dir.removeprefix(">").split('>')
    if len(elements) < 2:
        # If there is only one term e.g. ">Python Basics",
        # the user has not entered a topic first.
        print("Enter *into* a topic first")
        return
    # Resolve and return the topic object
    return syllabus[elements[0]][elements[1]]

# Gets the unit from the working directory
def wd_get_unit():
    # Let interpreter know that `working_dir` is found globally
    global working_dir
    # Same process as above function
    elements = working_dir.removeprefix(">").split('>')
    if len(elements) < 1:
        # If workign directory is just ">",
        # the user has not yet entered into a unit
        print("Enter *into* a unit first")
        return
    return syllabus[elements[0]]

# Add a vocabulary term to the topic's vocabulary dict.
# SEE: planning.txt for example of a structure of a topic.
# use working dir's topic
def add_vocab(vocab, definition, notes):
    # Resolve topic
    topic = wd_get_topic()
    # If topic is None, return None
    if topic is None:
        return
    # SEE: planning.txt for structure
    # Enter "vocab" dictionary of topic and
    # set the vocab term's definition and notes to
    # parameters provided.
    topic['vocab'][vocab] = {
        'definition': definition,
        'notes': notes
    }

# Add a notecard to the topic's notecard list.
# use working dir's topic
def add_ncard():
    # Same as function above
    topic = wd_get_topic()
    if topic is None:
        return
    # Call rawinput function:
    # continuously get input from user for multiple lines
    # until EOF is typed.
    input = rawinput("Writing a new note"+raw_input_prompt)
    # If input is not empty
    if not input == '':
        # add the input to the list of notecards.
        topic['notecards'].append(input)

# use working dir's unit
# Add a topic to the current unit.
def add_topic(topic_name: str):
    # Get working directory's unit
    unit = wd_get_unit()
    # Abort if unit is None
    if unit is None:
        return
    # If the current topic name exists
    if topic_name in unit:
        # Tell the user that the topic already exists and abort.
        print("Warning: topic name already exists in unit. Aborting")
        return
    # CONTROL FLOW:
    # This code will only be reached if the above if statement
    # is false due to its return statement.
    # Add a topic w/ specified name with correct structure
    # SEE: planning.txt
    unit[topic_name] = {
        'vocab': {},
        'notecards': []
    }


# Resolve element at path and delete it.
def del_elem(element: str):
    # Tell intepreter that working_dir is global
    global working_dir
    # Resolve working directory
    dir = resolve_wd()
    # If the element is a list,
    if element.isnumeric() and isinstance(dir, list):
        # convert element to an integer index
        element = int(element)  # convert to index if dir is a list
    # Depending on the type of object selected...
    # If...
    #   element is in the wd (working dir.) IF wd is dictionary
    #   element index is within bounds      IF wd is list...
    if (element in dir) if isinstance(dir, dict) else (element >= 0
                                                       and element < len(dir)):
        # Delete element (either index of list or key of dictionary)
        print(f"Deleting {element} in {working_dir}")
        del dir[element]
    else:
        # Else, tell user that element is not found.
        print("Element not found")


# select and "enter" into element from working directory
def wd_into(element: str):
    global working_dir
    # if the destination exists...
    if element in resolve_wd():
        # Get the destination object and determine
        # if the destination can be entered into.
        # (has children objects: list or dict)
        # (can't be just a string)
        if isinstance(resolve_wd()[element], (list, dict)):
            # Append destination to working directory
            working_dir += ">" + element
        else:
            # Tell user that element can't be entered into.
            print("Element is not a list or dictionary")
    else:
        # Tell user element does not exist.
        print(f"Element {element} does not exist")

# Move *out of* the current element and into the one that contains it.
def wd_outof():
    global working_dir  # tell interpreter working_dir is global

    # discard first > to avoid empty first string in split
    wd_x = working_dir.removeprefix(">")
    elements = wd_x.split('>')
    # if len(elements) < 2: # Units can now be exited
    #     print("Cannot get out of " + elements[0])
    #     return

    # Split working dir. by '>' and
    # remove the last term to effectively
    # get out of the current place into the containing object
    # e.g. ">Python Basics>Data Types"
    # to   ">Python Basics"
    del elements[len(elements) - 1]
    working_dir = ""
    for i, v in enumerate(elements):
        # if i > 0: # now working directory starts with >
        working_dir += ">"+v

# concatenates all but first token with spaces in between
def join_tokens(args):
    element_str = ""
    # run through list of arguments
    for i, v in enumerate(args):
        # skip first argument (the cmd name)
        if i == 0:
            continue
        # add argument to the string
        element_str += v
        # if not last argument, add a space inbetween
        # ^ (to prevent trailing spaces)
        if i < len(args)-1:
            element_str += " "
    # return element_str
    return element_str

# Get user input
def rawinput(prompt):
    print(prompt)
    str_ = ""
    try:
        # Keep getting user input, multiple lines,
        # until user types "EOF"
        for line in stdin:
            if line == "EOF\n":
                # if user types in "EOF"
                # return string WITHOUT adding the "EOF" text
                return str_
            # append line to string
            str_ += line  # line includes trailing \n

    # stop if ^D
    except EOFError:
        return str_

current_search_dir = ""
""" for sef
for ku,vu in syllabus.items(): # iterate through units
    print(ku)
    for kt, vt in vu.items(): # iterate through topics
        print(kt)
        print(vt)
"""


# Set the value of given key or index of dict or list respectively
def setkey(keyorindex):
    # define selected_obj as resolved working direcdtory
    selected_obj = resolve_wd()
    if isinstance(selected_obj, dict):  # dict
        # If the key does not exist... warn user
        if keyorindex not in selected_obj:
            print("WARNING: making new key, structure may be compromised")
        # If key exists but is a dictionary or list, warn user
        if keyorindex in selected_obj and isinstance(selected_obj[keyorindex],
                                                     (list, dict)):
            print("WARNING: current value to be replaced has more" +
                  " nested information ")
        # Get user input as a string
        inputstr = rawinput(f"Writing to key {keyorindex}"+raw_input_prompt)
        if inputstr is None or inputstr == '':
            # Cancel if empty
            print("Cancelling")
            return
        # Set key of dictionary to the user's input.
        selected_obj[keyorindex] = inputstr
    elif isinstance(selected_obj, list):  # list
        # If user did not provide a number, tell and abort
        if not keyorindex.isnumeric():
            print("non-number provided")
            return
        # Get index as a number from user input
        index = int(keyorindex)
        # Check index to be in bounds, if not, abort.
        if index < 0 or index > len(selected_obj):
            print("invalid index")
            return
        # Set the index at list to be the user input.
        inputstr = rawinput(
            f"Writing to index {index} of {len(selected_obj)}"+raw_input_prompt)
        if inputstr is None or inputstr == '':
            print("Cancelling")
            return
        # If index is just one higher than the greatest existing index,
        # append the user input to the list.
        # else, just set the object at index to be input string.
        if index == len(selected_obj):
            selected_obj.append(inputstr)
        else:
            selected_obj[index] = inputstr

    else:
        # (should not happen: wd should always be at a list or dict)
        # (items that have children: see wd_into())
        # warn user regardless of this issue.
        print("working directory is not at a list or dictionary")

# Print the element and its contents in a formatted way
def show(element):
    # element can vary in type
    # e.g.
    # Urbanization [dict]:
    #  key definition [str]
    #  key notes [str]
    #
    # notecards [list]:
    #  [0] Two main f... [str]
    #  [1] Site and s... [str]
    if isinstance(element, list):
        print("list:")
        for i, v in enumerate(element):
            # substring [start:end(not included)]
            print(f" [{i}] {v[0:10]}... [str]")
    elif isinstance(element, dict):
        print("dict:")
        for k, v in element.items():
            print(f" key {k} [{type(v)}]")
    else:
        print(element)


def search_in_item(item, term: str):
    global current_search_dir
    # current_search_dir is global and indicates where function is searching
    # no matter how many recursions deep it is in.
    # do NOT replace, only append

    if isinstance(item, str):
        if item.lower().__contains__(term.lower()):
            # print("Match found: " + item)
            return True # return true if found
            # the printing will be handled by the previous recursion step
        return False

    for k, v in enumerate(item) if isinstance(item, list) else item.items():
        prev_search_dir = current_search_dir  # make backup of current search directory
        # add key to current search directory
        # so deeper recursions of this function will know where we are currently at
        current_search_dir += ">" + str(k)
        # if key has search term OR if value (if str) has search term
        # if value is a list or dict, will search within it for the term (recursion)
        result = search_in_item(v, term)
        keyresult = str(k).lower().__contains__(term.lower())
        # print(f"{current_search_dir}, {result}")
        if result or keyresult:
            # print("\nprev: " + prev_search_dir + "\ncurr: " + current_search_dir)'
            ucsd = current_search_dir.replace('>', ' \033[32m→\033[0m ', -1)
            print(f"\nMatch term \"{term}\": {ucsd}")  # print current match's directory
            if result:  # don't print value if only key and NOT VALUE matches.
                show(v)
        current_search_dir = prev_search_dir


pre_test_wd = working_dir
working_dir = ">"
# search_in_item(syllabus, "boolean")
working_dir = pre_test_wd


def write_to_file(filepath):
    with open(filepath, 'w') as file:
        file.write(json.dumps(syllabus))


def read_from_file(filepath):
    global syllabus
    with open(filepath, 'r') as file:
        syllabus = json.load(file)
        print("Imported: " + str(syllabus))


def quiz(terms, definitions):
    loop = 1
    print("""You have entered the flashcard review system.
    The flashcard review system will display a term or definition depending on what you would like.
    Then once you feel you have the answer you may view the answer and see if you were correct.""")
    print("""Possible inputs for this program:
    blank/press Enter - flip flashcard over
    exit - exit the flashcard review system
    r - reshuffle the terms
    """)
    study_choice = input("""Would you like to study the definitions or the terms? 
    terms - display the terms flip to see definitions
    definitions - display the definitions flip to see terms
    Choose which one you would like to do: """)
    border()
    if study_choice.lower() == "terms":
        # Put the parallel lists together using zip()
        # into a list of tuples.
        flashcards = list(zip(terms, definitions))
        random.shuffle(flashcards)
        # While the study session should keep going...
        while loop == 1:
            # Iterate through tuple of term and definition
            for term, definition in flashcards:
                print("Term:", term)
                input("Press Enter to reveal definition...\n")
                print("Term:", term)
                print("Definition:", definition)
                choice = input("""continue?
1 - yes
2 - no
choose: """)
                if choice.lower() == '1':
                    border()
                    continue
                elif choice.lower() == '2':
                    loop = 0
                    break
                else:
                    print("That is not a valid choice. Please try again")
                return 1
            loop = 0

    elif study_choice.lower() == "definitions":
        # Put the parallel lists together using zip()
        # into a list of tuples.
        flashcards = list(zip(definitions, terms))
        random.shuffle(flashcards)
        # While the study session should keep going...
        while loop == 1:
            # Iterate through tuple of term and definition
            for definitions, terms in flashcards:
                print("Definition:", definitions)
                input("Press Enter to reveal definition...\n")
                print("Definition:", definitions)
                print("terms:", terms)
                choice = input("""continue?
1 - yes
2 - no
choose: """)
                if choice.lower() == '1':
                    border()
                    continue
                elif choice.lower() == '2':
                    loop = 0
                    break
                else:
                    print("That is not a valid choice. Please try again")
                return 1
            loop = 0
    else:
        print("That is not a valid choice. Please try again")
        return 1

def bubble_sort(list):
    swap = True
    while swap:
        swap = False
        for i in range(len(list) - 1):
            if list[i].lower() > list[i + 1].lower():
                # print(list[i].lower(), ">", list[i + 1].lower())
                temp = list[i]
                list[i] = list[i + 1]
                list[i + 1] = temp
                swap = True
            # else:
                # print(list[i].lower(), "<", list[i + 1].lower())
    print("\n",list)


def main():
    global working_dir
    global current_search_dir
    running = True
    # color escape sequence: [32m -- green, [0m -- reset
    print("\033[32mWelcome to the TAPMPHUD Syllabus Manager\n" +
          "Type 'help' and press Enter to list all commands.\033[0m")
    while running:  # while program should run
        border()
        # color all >'s green with terminal color escape sequence
        # (0m to reset color)
        # Get user input with the prompt
        uinput = input(working_dir.replace(
            '>', ' \033[32m→\033[0m ', -1) + " \033[32m%\033[0m ")
        args = uinput.split()  # Arguments (split by words)
        argc = len(args)  # number of elements
        border()
        match args[0].lower():  # First token is command
            case 'exit':
                running = False
            case 'help':
                print(help)
            case 'pwd':  # Print where you are now
                print("This is your current location:\n", working_dir.replace('>', ' \033[32m→\033[0m ', -1))
            case 'outof':  # Moving to the large file
                wd_outof()
            case 'ls':
                if argc == 1:
                    selected = resolve_wd()
                else:
                    selected = resolve_dir(
                        working_dir + ">" + join_tokens(args))

                if isinstance(selected, (dict, list)):
                    show(selected)
                else:  # if the working directory is not a dictionary or list.
                    print("!!!Working directory object invalid type!!!")
                    print(working_dir)

            case 'read':
                # read key of dictionary or list using show()
                input_str = join_tokens(args)
                selected = None
                # empty string
                if input_str == '':
                    print("Invalid command usage: needs key")
                if input_str.isnumeric() and isinstance(resolve_wd(), list):
                    # check list index validity
                    if int(input_str) < 0 or int(input_str) >= len(resolve_wd()):
                        print("Invalid index")
                    else:
                        selected = resolve_wd()[int(input_str)]
                else:
                    # check dict key validity
                    selected = resolve_wd()[
                        input_str] if input_str in resolve_wd() else "Key not found"

                show(selected)

            case 'setkey':
                # see: join_tokens(args)
                setkey(join_tokens(args))

            case 'add-vterm':
                if argc < 2:  # only 'add-vterm'
                    print("Improper usage- needs term name")
                definition = rawinput(
                    "--- Writing definition (type EOF to finish) ---")
                notes = rawinput("--- Writing notes (type EOF to finish) ---")
                add_vocab(join_tokens(args), definition, notes)

            case 'add-ncard':
                add_ncard()

            case 'flashcard-review':
                rerun = 0
                definitions_list = []
                terms_list = []
                for ku, vu in syllabus.items():  # iterate through units
                    for kt, vt in vu.items():  # iterate through topics
                        # vt is a dict of {vocab, notecards} (see planning.txt for structure)
                        # vt["vocab"] will be dict of [key]vocab_term: {definition, notes}
                        # terms will be a tuple of (vocab_term, {definition, notes})
                        terms = vt["vocab"].items()
                        for (term, dict_) in terms:
                            # term will be a string (the vocab term)
                            # dict_ will be dictionary dof definition and notes
                            definitions_list.append( dict_['definition'] ) # access definition
                            terms_list.append( term ) # key will be a string
                            # note from luzj: sorry about the nested dictionary hell ._.
                            # note from Sef: Nah u good, we still got it.

                rerun = quiz(terms_list, definitions_list)
                if rerun == 1:
                    quiz(terms_list, definitions_list)
                else:
                    pass

            case 'add-topic':
                add_topic(join_tokens(args))

            case 'sort':
                terms_list = []
                for ku, vu in syllabus.items():  # iterate through units
                    for kt, vt in vu.items():  # iterate through topics
                        # vt is a dict of {vocab, notecards} (see planning.txt for structure)
                        # vt["vocab"] will be dict of [key]vocab_term: {definition, notes}
                        # terms will be a tuple of (vocab_term, {definition, notes})
                        terms = vt["vocab"].items()
                        for (term, dict_) in terms:
                            # term will be a string (the vocab term)
                            # dict_ will be dictionary dof definition and notes
                            terms_list.append(term)  # key will be a string
                bubble_sort(terms_list)

            case 'add-unit':
                if argc <= 1:
                    print("Improper usage- needs unit name")
                else:
                    syllabus[join_tokens(args)] = {}

            case 'search':
                current_search_dir = working_dir
                if join_tokens(args).strip() == "":
                    print("Improper usage- needs search term")
                else:
                    search_in_item(resolve_wd(), join_tokens(args))

            case 'into':
                wd_into(join_tokens(args))

            case 'del':
                del_elem(join_tokens(args))

            case 'write-file':
                write_to_file(join_tokens(args))
            case 'load-file':
                read_from_file(join_tokens(args))
                working_dir = "" # Set to root directory

            case _:
                print("Invalid command: " + args[0])


if __name__ == '__main__':
    main()
else:
    main()

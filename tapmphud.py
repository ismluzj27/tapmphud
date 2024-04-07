# tapmphud.py
# "ta-pum-fud"

import random
import json

from sys import stdin

border_design = "------<><><>------<><>------<><><>------<><>------<><><>------"
border_design1 = "-----<~~~~>-----<~~~~>-----<~~~~>-----<~~~~>-----<~~~~>-----"
border_design2 = "-~-~-</^\\>-~-~-</^\\>-~-~-</^\\>-~-~-</^\\>-~-~-</^\\>-~-~-</^\\>"
border_design3 = "---<<<~~~^^^~~~>>>------<<<~~~^^^~~~>>>------<<<~~~^^^~~~>>>---"

def border():
    borders = [border_design,
                border_design1,
                border_design2,
                border_design3]
    print(random.choice(borders))


# TODO: implement all asterisks
help = """exit - exit
help - list commands
*quiz - Generate quiz based on syllabus
search [term] - Look for and show any matches to term within **your current directory**.
*sort - bubble sort vocabulary alphabetically

\033[32m## Navigation ##\033[0m
pwd - print working directory
ls - list all elements in working directory
ls [element] - list all elements in specified list/dictionary
read [key OR index] - print the value of a key/at index of list
into [element] - select an element in current working directory
outof - go up in the working directory into broader element

\033[32m## Modifying syllabus ##\033[0m
add-vterm [term name] - add vocabulary term w/ def & notes (at working directory's topic)
add-ncard (asks for user input) - add a notecard (at working directory's topic) 
add-topic [topic name] - add a topic (at working directory's unit)
setkey [key/index] (asks for user input) - replace content at key or index with user input
del [element name] - delete any key/dict/str. can be a unit, topic, vocab term, note, etc.

\033[32m## Exporting and importing to file ##\033[0m
write-file [filename] - Write current syllabus to the specified file
load-file [filename] - Load syllabus from specified file"""  # * = NOT IMPLEMENTED

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

def resolve_wd():
    return resolve_dir(working_dir)

# Given a path, return the object that is at that path.
# e.g. given >Python Basics>Data Types"
#   ...returns syllabus["Python Basics"]["Data Types"]
def resolve_dir(str_):
    selected = syllabus
    # discard first '>' to avoid first split being ""
    strx = str_.removeprefix(">")
    if strx == '':
        return syllabus
    for i, v in enumerate(strx.split('>')):
        if v in selected:
            selected = selected[v]
        else:
            print(f"Element {v} not found-- stopping resolve")
            return selected
    return selected

# Extract the topic from the working directory (a string).
def wd_get_topic():
    global working_dir
    # >unit>topic
    elements = working_dir.removeprefix(">").split('>')
    if len(elements) < 2:
        print("Enter *into* a topic first")
        return
    return syllabus[elements[0]][elements[1]]

# Gets the unit from the working directory
def wd_get_unit():
    global working_dir
    elements = working_dir.removeprefix(">").split('>')
    if len(elements) < 1:
        print("Enter *into* a unit first")
        return
    return syllabus[elements[0]]

# Add a vocabulary term to the topic's vocabulary dict.
# SEE: planning.txt for example of a structure of a topic.
# use working dir's topic
def add_vocab(vocab, definition, notes):
    topic = wd_get_topic()
    if topic is None:
        return
    topic['vocab'][vocab] = {
        'definition': definition,
        'notes': notes
    }

# Add a notecard to the topic's notecard list.
# use working dir's topic
def add_ncard():
    topic = wd_get_topic()
    if topic is None:
        return
    input = rawinput("Writing a new note"+raw_input_prompt)
    if not input == '':
        topic['notecards'].append(input)

# use working dir's unit
# Add a topic to the current unit.
def add_topic(topic_name: str):
    unit = wd_get_unit()
    if unit is None:
        return
    if topic_name in unit:
        print("Warning: topic name already exists in unit. Aborting")
        return
    unit[topic_name] = {
        'vocab': {},
        'notecards': []
    }


# Resolve element at path and delete it.
def del_elem(element: str):
    global working_dir
    dir = resolve_wd()
    if element.isnumeric() and isinstance(dir, list):
        element = int(element)  # convert to index if dir is a list
    if (element in dir) if isinstance(dir, dict) else (element >= 0 
                                                       and element < len(dir)):
        print(f"Deleting {element} in {working_dir}")
        del dir[element]
    else:
        print("Element not found")


# select and "enter" element from working directory
def wd_into(element: str):
    global working_dir
    if element in resolve_wd():
        if isinstance(resolve_wd()[element], (list, dict)):
            working_dir += ">" + element
        else:
            print("Element is not a list or dictionary")
    else:
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
    del elements[len(elements) - 1]
    working_dir = ""
    for i, v in enumerate(elements):
        # if i > 0: # now working directory starts with >
        working_dir += ">"+v

# concatenates all but first token with spaces in between
def join_tokens(args):
    element_str = ""
    for i, v in enumerate(args):
        if i == 0:
            continue
        element_str += v
        if i < len(args)-1:
            element_str += " "
    return element_str

# Get user input
def rawinput(prompt):
    print(prompt)
    str_ = ""
    try:
        for line in stdin:
            if line == "EOF\n":
                return str_
            str_ += line  # line includes trailing \n

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
    selected_obj = resolve_wd()
    if isinstance(selected_obj, dict):  # dict
        if keyorindex not in selected_obj:
            print("WARNING: making new key, structure may be compromised")
        if keyorindex in selected_obj and isinstance(selected_obj[keyorindex],
                                                     (list, dict)):
            print("WARNING: current value to be replaced has more" +
                  " nested information ")

        inputstr = rawinput(f"Writing to key {keyorindex}"+raw_input_prompt)
        if inputstr is None or inputstr == '':
            print("Cancelling")
            return
        selected_obj[keyorindex] = inputstr
    elif isinstance(selected_obj, list):  # list
        if not keyorindex.isnumeric():
            print("non-number provided")
            return
        index = int(keyorindex)
        if index < 0 or index > len(selected_obj):
            print("invalid index")
            return

        inputstr = rawinput(
            f"Writing to index {index} of {len(selected_obj)}"+raw_input_prompt)
        if inputstr is None or inputstr == '':
            print("Cancelling")
            return
        # index is just one higher than the greatest existing index
        if index == len(selected_obj):
            selected_obj.append(inputstr)
        else:
            selected_obj[index] = inputstr

    else:
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
            # substring [start:end(not included]
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

    for k,v in enumerate(item) if isinstance(item, list) else item.items():
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
            print(f"\nMatch term \"{term}\": {current_search_dir}") # print current match's directory
            if result: # don't print value if only key and NOT VALUE matches.
                show(v)
        # revert (remove key from current search directory) after looking at / through value.
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

def quiz():
    pass



def main():
    global working_dir
    global current_search_dir
    running = True
    print("\033[32mWelcome to the TAPMPHUD Syllabus Manager\n" +
          "Type 'help' and press Enter to list all commands.\033[0m")
    while running:  # while program should run
        border()
        # color all >'s grey with terminal color escape sequence
        # (0m to reset color)
        # Get user input with the prompt
        uinput = input(working_dir.replace(
            '>', ' \033[32m→\033[0m ', -1) + " \033[32m%\033[0m ")
        args = uinput.split()  # Arguments (split by words)
        argc = len(args)  # number of elements
        match args[0].lower():  # First token is command
            case 'exit':
                running = False
            case 'help':
                print(help)
            case 'pwd':  # Print where you are now
                print(working_dir)
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
                else:
                    print("!!!Working directory object invalid type!!!")
                    print(working_dir)

            case 'read':
                input_str = join_tokens(args)
                selected = None
                if input_str == '':
                    print("Invalid command usage: needs key")
                if input_str.isnumeric() and isinstance(resolve_wd(), list):
                    if int(input_str) < 0 or int(input_str) >= len(resolve_wd()):
                        print("Invalid index")
                    else:
                        selected = resolve_wd()[int(input_str)]
                else:
                    selected = resolve_wd()[
                        input_str] if input_str in resolve_wd() else "Key not found"

                show(selected)

            case 'setkey':
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

            case 'add-topic':
                add_topic(join_tokens(args))

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

            case _:
                print("Invalid command: " + args[0])


if __name__ == '__main__':
    main()

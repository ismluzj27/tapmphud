# tapmphud.py
# "ta-pum-fud"

from sys import stdin
import re 

help = """exit - exit
help - list commands

pwd - print working directory
ls - list all elements in working directory
ls [element] - list all elements in specified list/dictionary
read [key OR index] - print the value of a key/at index of list
into [element] - select an element in current working directory
outof - go up in the working directory into broader element

add-vterm [term name] - add vocabulary term w/ def & notes (at working directory's topic)
*add-ncard (asks for user input) - add a notecard (at working directory's topic) 
*add-topic [topic name] - add a topic (at working directory's unit)
setkey [key/index] (asks for user input) - replace content at key or index with user input
del [element name] - delete any key/dict/str. can be a unit, topic, vocab term, note, etc.

*write-file [filename] - Write current syllabus to the specified file
*load-file [filename] - Load syllabus from specified file""" # * = NOT IMPLEMENTED

syllabus = {
    '7 Cities': { # unit
        '1 Orig Dist Sys Cities': { # topic
            'vocab': {
                'Urbanization': {
                    'definition': 'the process of developing towns and cities',
                    'notes': '',
                },
                'Site': {
                    'definition': 'physical characteristics of a place',
                    'notes': "includes:\n"+
                        " - climate\n"+
                        " - natural features, especially water"
                },
                'Situation': {
                    'definition': 'location of a place relative to surroundings',
                    'notes': "includes:\n"
                        " - proximity to natural resources\n" +
                        " - proximity to other cities\n" +
                        " - accessibility"
                }
            },
            'notecards': [ # group relevant information together
                "Two main factors influence location of cities: site and situation",
                "Site and situation can also impact how cities function and grow\n"+
                " - Size of cities\n"+
                "   * Εxample: Manila has trouble growing because of physical constraints\n"+
                " - Economic development\n"+
                "   * Example: Singapore got very wealthy due to strategic position on shipping routes\n"+
                " - Political/military history\n"+
                "   * Example: Istanbul as a shatterbelt",
                "Key trend around the world -- cities are getting larger\n"+
                "Causes\n"+
                " 1) Population growth\n"+
                "   * People need somewhere to live\n"+
                " 2) Improvements in transport and communication\n"+
                "   * Allows cities to expand -- just look at Manila",
            ]
        }
    }
}

# print(syllabus['7 Cities']['1 Orig Dist Sys Cities']['notes'][1])
#              >Unit    >Topic
working_dir = ">7 Cities>1 Orig Dist Sys Cities"

# returns the selected object
# e.g. syllabus['7 Cities']
def resolve_wd():
    return resolve_dir(working_dir)

def resolve_dir(str):
    selected = syllabus
    # discard first '>' to avoid first split being ""
    strx = str.removeprefix(">")
    for i, v in enumerate(strx.split('>')):
        if v in selected:
            selected = selected[v]
        else:
            print(f"Element {v} not found-- stopping resolve")
            return selected
    return selected

# use working dir's topic
def add_vocab(vocab, definition, notes):
    #                 unit>topic
    elements = working_dir.removeprefix(">").split('>')
    topic = syllabus[elements[0]][elements[1]]
    topic['vocab'][vocab] = {
            'definition': definition,
            'notes': notes
        }

# use working dir's topic
def add_ncard(note_str):
    pass

# use working dir's unit
def add_topic(topic_name: str):
    pass

def del_elem(element: str):
    global working_dir
    dir = resolve_wd();
    if element in dir:
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

def wd_outof():
    global working_dir # tell interpreter working_dir is global

    wd_x = working_dir.removeprefix(">") # discard first > to avoid empty first string in split
    elements = wd_x.split('>')
    # if len(elements) < 2: # Units can now be exited
    #     print("Cannot get out of " + elements[0])
    #     return
    del elements[len(elements) - 1]
    working_dir = ""
    for i,v in enumerate(elements):
        # if i > 0: # now working directory starts with >
        working_dir += ">"+v

# concatenates all but first token with spaces in between
def join_tokens(args):
    element_str = ""
    for i,v in enumerate(args):
        if i == 0:
            continue
        element_str += v 
        if i < len(args)-1:
            element_str += " "
    return element_str

def rawinput(prompt):
    print(prompt)
    str_ = ""
    try:
        for line in stdin:
            if line == "EOF\n":
                return str_
            str_ += line # line includes trailing \n

    except EOFError:
        return str_

def setkey(keyorindex):
    selected_obj = resolve_wd()
    if isinstance(selected_obj, dict): # dict
        if not keyorindex in selected_obj:
            print("WARNING: making new key, structure may be compromised")
        if keyorindex in selected_obj and isinstance(selected_obj[keyorindex], (list, dict)):
            print("WARNING: current value to be replaced has more nested information ")

        inputstr = rawinput(f"Writing to key {keyorindex}"
                            + "\n--- Leave blank to cancel ---"
                            + "\n---   Type EOF to stop    ---")
        if inputstr == None or inputstr == '':
            print("Cancelling")
            return
        selected_obj[keyorindex] = inputstr
    elif isinstance(selected_obj, list): # list
        if not keyorindex.isnumeric():
            print("non-number provided")
            return
        index = int(keyorindex)
        if index < 0 or index > len(selected_obj):
            print("invalid index")
            return

        inputstr = rawinput(f"Writing to index {index} of {len(selected_obj)}"
                            + "\n--- Leave blank to cancel ---"
                            + "\n---   Type EOF to stop    ---")
        if inputstr == None or inputstr == '':
            print("Cancelling")
            return
        if index == len(selected_obj): # index is just one higher than the greatest existing index
            selected_obj.append(inputstr)
        else:
            selected_obj[index] = inputstr

    else:
        print("working directory is not at a list or dictionary")

def show(element):
    # element can vary in type
    # todo: implement printing format for list, dict, and str
    # e.g.
    # Urbanization [dict]:
    #  key definition [str]
    #  key notes [str]
    #
    # notecards [list]:
    #  [0] Two main f... [str]
    #  [1] Site and s... [str]
    print(element)


def main():
    running = True
    print("Welcome to the TAPMPHUD Syllabus Manager")
    while running: # while program should run
        # color all >'s grey with terminal color escape sequence (0m to reset color)
        uinput = input(working_dir.replace('>', '\033[37m>\033[0m', -1) + "\033[37m$\033[0m ") # Get user input with the prompt
        args = uinput.split() # Arguments (split by words)
        argc = len(args) # number of elements
        match args[0]: # First token is command
            case 'exit':
                running = False
            case 'help':
                print(help)
            case 'pwd':
                print(working_dir)
            case 'outof':
                wd_outof()
            case 'ls':
                if argc == 1:
                    selected = resolve_wd()
                else:
                    selected = resolve_dir(working_dir + ">" + join_tokens(args))

                if isinstance(selected, dict):
                    show(selected.keys())
                elif isinstance(selected, list):
                    show(selected)
                else:
                    print("!!!Working directory object invalid type!!!")
                    print(working_dir)

            case 'read':
                input_str = join_tokens(args)
                if input_str == '':
                    print("Invalid command usage: needs key")
                if input_str.isnumeric() and isinstance(resolve_wd(), list):
                    selected = resolve_wd()[int(input_str)]
                else:
                    selected = resolve_wd()[input_str] if input_str in resolve_wd() else "Key not found"
                
                show(selected) # todo: print prettier

            case 'setkey':
                setkey(join_tokens(args))

            case 'add-vterm':
                if argc < 2: # only 'add-vterm'
                    print("Improper usage- needs term name")
                definition = rawinput("--- Writing definition (type EOF to finish) ---")
                notes      = rawinput("--- Writing notes (type EOF to finish) ---")
                add_vocab(join_tokens(args), definition.strip(), notes.strip())

            case 'into':
                wd_into(join_tokens(args))

            case 'del':
                del_elem(join_tokens(args))

            case _:
                print("Invalid command: " + args[0])




if __name__ == '__main__':
    main()


# tapmphud.py
# "ta-pum-fud"

from sys import stdin

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
#              Unit    >Topic
working_dir = "7 Cities>1 Orig Dist Sys Cities"

# returns the selected object
# e.g. syllabus['7 Cities']
def resolve_working_dir():
    global working_dir
    selected = syllabus
    for i,v in enumerate(working_dir.split('>')):
        selected = selected[v]
    return selected

# use working dir's topic
def add_vocab(vocab, definition, notes):
    pass

# use working dir's topic
def add_ncard(note_str):
    pass

# use working dir's unit
def add_topic(topic_name: str):
    pass

# select and "enter" element from working directory
def wd_into(element: str):
    print
    global working_dir
    if element in resolve_working_dir():
        if isinstance(resolve_working_dir()[element], (list, dict)):
            working_dir += ">" + element
        else:
            print("Element is not a list or dictionary")
    else:
        print(f"Element {element} does not exist")

def wd_outof():
    global working_dir # tell interpreter working_dir is global

    elements = working_dir.split('>')
    if len(elements) < 2:
        print("Cannot get out of "+elements[0])
        return
    del elements[len(elements) -1]
    working_dir = ""
    for i,v in enumerate(elements):
        if i > 0:
            working_dir += ">"
        working_dir += v

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
    for line in stdin:
        str_ += line # line includes trailing \n

def setkey(keyorindex):
    global working_directory
    selected_obj = resolve_working_dir()
    if isinstance(selected_obj, dict):
        if not keyorindex in selected_obj:
            print("WARNING: making new key, structure may be compromised")
        if keyorindex in selected_obj and isinstance(selected_obj[keyorindex], (list, dict)):
            print("WARNING: current value to be replaced has more nested information ")

        inputstr = rawinput(f"--- Writing to key {keyorindex} ---\n--- Leave blank to cancel ---\n---  CTRL+D (^D) to stop  ---")
        if inputstr == None or inputstr == '':
            print("Cancelling")
        else:
            selected_obj[keyorindex] = inputstr
    elif isinstance(selected_obj, list):
        pass
    else:
        print("working directory is not at a list or dictionary")

def show(element):
    # element can vary in type
    # todo: implement printing format for list, dict, and str
    print(element)

def main():
    running = True
    print("Welcome to the TAPMPHUD Syllabus Manager")
    while running: # while program should run
        uinput = input(working_dir + " $ ") # Get user input with the prompt
        args = uinput.split() # Arguments (split by words)
        argc = len(args) # number of elements
        match args[0]: # First token is command
            case 'exit':
                running = False
            case 'pwd':
                print(working_dir)
            case 'outof':
                wd_outof()
            case 'ls':
                selected = resolve_working_dir()
                if isinstance(selected, dict):
                    # todo: print prettier
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
                if input_str.isnumeric() and isinstance(resolve_working_dir(), list):
                    selected = resolve_working_dir()[int(input_str)]
                else:
                    selected = resolve_working_dir()[input_str] if input_str in resolve_working_dir() else "Key not found"
                
                show(selected) # todo: print prettier

            case 'setkey':
                setkey(join_tokens(args))

            case 'into':
                wd_into(join_tokens(args))
                
            case _:
                print("Invalid command: " + args[0])




if __name__ == '__main__':
    main()


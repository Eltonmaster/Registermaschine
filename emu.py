import sys, os
from time import sleep

commands = [None]
storage = [None] * 20
storage[0] = 0

def init():
    global commands, storage

    if len(sys.argv) == 1:
        print("Usage: \nemu.py PATH_TO_FILE \nOptional:\nemu.py PATH_TO_FILE STORAGE_SIZE")
        sys.exit()

    if len(sys.argv) > 1:
        if os.path.isfile(sys.argv[1]):
            path = sys.argv[1]
        else:
            print("The entered path does not point to a file")
            sys.exit()
    
    if len(sys.argv) > 2:
        storage = [None] * int(sys.argv[2])

    path = sys.argv[1]
    print(f"loading file: {path}")
    register_file = open(path, "r+")
    for x in register_file:
        commands.append(x)
    register_file.close()

def parse(line, i):
    global storage, commands
    parts = line.split(" ")

    print(f"{i} - "+line)
    
    if parts[0] == "END":
        print("\nEmulation finished")
        sys.exit()

    elif parts[0] == "LOAD":
        storage[0] = storage[int(parts[1])]
        return None

    elif parts[0] == "STORE":
        storage[int(parts[1])] = storage[0]
        return None

    elif parts[0] == "CLOAD":
        storage[0] = int(parts[1])
        return None

    elif parts[0] == "MULT":
        storage[0] = storage[0]*storage[int(parts[1])]
        return None

    elif parts[0] == "DIV":
        storage[0] = storage[0] // storage[int(parts[1])]
        return None
    
    elif parts[0] == "ADD":
        storage[0] = storage[0]+storage[int(parts[1])]
        return None

    elif parts[0] == "CADD":
        storage[0] = storage[0]+int(parts[1])
        return None

    elif parts[0] == "SUB":
        value = storage[0]-storage[int(parts[1])]
        if value < 0:
            storage[0] = 0
        else:
            storage[0] = value
        return None

    elif parts[0] == "CSUB":
        value = storage[0]-int(parts[1])
        if value < 0:
            storage[0] = 0
        else:
            storage[0] = value
        return None

    elif parts[0] == "GOTO":
        return int(parts[1])

    elif parts[0] == "IF":
        compvalue = int(parts[3])
        if compvalue != 0:
            print("ATTENTION: The if operation only supports the comparison to 0")
            sys.exit()

        if compvalue == storage[0]:
            return parse(str(parts[4])+" "+str(parts[5]), i)


def cycle(i):
    print(print_storage())
    global storage, commands
    value = parse(commands[i], i)
    sleep(.2)
    if value != None:
        cycle(value)
        return
    if (len(commands) > i):
        cycle(i+1)
        return

def print_storage():
    global storage, commands
    temp = ""
    for entry in range(len(storage)):
        if entry == 0:
            temp = temp+f"[{str(storage[entry]) if storage[entry] != None else ' '}]" 
            continue
        temp = temp+f" [{str(storage[entry]) if storage[entry] != None else ' '}]" 
    
    temp +="\n"

    return temp

        
init()
cycle(1)
from pathlib import Path
import json

debugger = False #when enabled, actions and errors will print

COMMAND_FILE_NAME = "commands.json" #default name
COMMAND_FILE = Path(COMMAND_FILE_NAME) #for pathing

def create_command(command): #returns true if command was created
    try:
        commands = _load_commands()
        commands.append(command.strip())
        _save_commands(commands)
        if debugger: print(f"Command created: {command}")
        return True
    except Exception as e:
        if debugger: print(f"An error occurred while creating a command: {e}")
        return False


def delete_command(command): #returns true if command was deleted
    if not COMMAND_FILE.exists():
        if debugger: print(f"Error: {COMMAND_FILE} does not exist")
        return False
        
    command = command.strip()
    
    try:
        commands = _load_commands()
        if command in commands:
            commands.remove(command)
            _save_commands(commands)
            if debugger: print(f"Command deleted: {command}")
            return True
        else:
            if debugger: print(f"Error: {command} not found")
            return False

    except Exception as e:
        if debugger: print(f"An error occurred while deleting a command: {e}")
        return False
    
    
def delete_all_commands(): #wipes COMMAND_FILE. Returns true if completed
    if not COMMAND_FILE.exists():
        if debugger: print(f"Error: {COMMAND_FILE} does not exist")
        return False
    
    try:
        _save_commands([])
        if debugger: print("All commands wiped successfully.")
        return True
    except Exception as e:
        if debugger: print(f"An error has occurred while deleting all commands: {e}")
        return False


def command_matches(command): #returns command matches in an array if match found from left to right
    try:
        commands = _load_commands()
        matches = [cmd for cmd in commands if cmd.startswith(command)]
        if debugger: print(f"Matches found: {matches}")            
        return matches
                
    except Exception as e:
        if debugger: print(f"An error has occurred while trying to match commands: {e}")
        return []
    

def command_matches_no_bounds(command): #same as command_matches but from anywhere within the command
    matches = []
    
    try:
        commands = _load_commands()
        command = command.strip()
        matches = [cmd for cmd in commands if command in cmd]
        if debugger: print(f"Matches found: {matches}")            
        return matches
                
    except Exception as e:
        if debugger: print(f"An error has occurred while trying to match commands without bounds: {e}")
        return []

def choose_command(command_options, choice): #command_options must be an array of strings, choice must be an int. Returns a command
    if choice > len(command_options) or choice <= 0:
        if debugger: print(f"Error: {choice} is invalid")
        return None
    
    return command_options[choice-1]


def change_file_name(name): #assign new file name. NOTE: Does not change file name in system if the file already exists
    global COMMAND_FILE_NAME
    global COMMAND_FILE
    COMMAND_FILE_NAME = f"{name}.json"
    COMMAND_FILE = Path(COMMAND_FILE_NAME)


def complete_command(command): #NOTE: Feature incomplete, read README.md for more information
    if debugger: print("Error: complete_command function has not been implemented")


def set_file_location(location): #for COMMAND_FILE. Intakes a directory or different json file name. 
    global COMMAND_FILE
    if debugger: print(f"Current file path: {COMMAND_FILE.resolve()}")    
    location = Path(location.strip()) 
    
    #check for json file
    if location.suffix == '.json':
        location.parent.mkdir(parents=True, exist_ok=True)
        COMMAND_FILE = location

    #move to new path
    else:
        location.mkdir(parents=True, exist_ok=True)
        COMMAND_FILE = location / COMMAND_FILE_NAME
        
    if debugger: print(f"File path updated to: {COMMAND_FILE.resolve()}\n")


def toggle_debugger(): #toggles debugger on or off
    global debugger
    debugger = not debugger
    if debugger: print(f"Debugger is now on")


#############
#helper funcs
#############

def _load_commands(): #loads commands from COMMAND_FILE
    if not COMMAND_FILE.exists():
        if debugger: print(f"Error: {COMMAND_FILE} does not exist")
        return []
    
    try:
        with COMMAND_FILE.open('r') as file:
            return json.load(file)
        
    except Exception as e:
        if debugger: print(f"An error occurred while running _load_commands: {e}")
        return []


def _save_commands(commands): #saves commands to COMMAND_FILE
    try:
        with COMMAND_FILE.open('w') as file:
            json.dump(commands, file, indent=4)

    except Exception as e:
        if debugger: print(f"An error occurred while running _save_commands: {e}")


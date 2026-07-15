from pathlib import Path
import json

DEBUGGER = False #when enabled, actions and errors will print

COMMAND_FILE_NAME = "commands.json" #default name
COMMAND_FILE = Path(COMMAND_FILE_NAME) #for pathing

def create_command(*command: str, type: str): #returns true if command was created
    try:
        #validation
        if not command:
            if DEBUGGER: print("Error: at least one command name must be provided")
            return False

        commands = _load_commands()

        current_level = commands
        for i, tag in enumerate(command):
            tag = tag.strip()
            is_last_tag = (i == len(command) - 1)
            
            #if no subcommand path, initialize it
            if tag not in current_level:
                current_level[tag] = {
                    "type": type if is_last_tag else "parent_command", 
                    "subcommands": {}
                }
            
            if is_last_tag:
                current_level[tag]["type"] = type
            else:
                #move down the tree
                current_level = current_level[tag]["subcommands"]

        _save_commands(commands)

        if DEBUGGER: 
            chain = " -> ".join(command)
            print(f"Command created: {chain} as {type}")
            
        return True
    
    except Exception as e:
        if DEBUGGER: print(f"An error occurred while creating a command: {e}")
        return False


def delete_command(*command: str): #returns true if command was deleted
    #validation
    if not command:
        if DEBUGGER: print("Error: at least one command name must be provided")
        return False
        
    try:
        commands = _load_commands()
        
        #clean command path
        path = [tag.strip() for tag in command]
        
        def _delete_recursive(current_level, path_list, index=0):
            tag = path_list[index]
            
            #check if exists
            if tag not in current_level:
                return False, False
            
            is_last = (index == len(path_list) - 1)
            
            if is_last:
                #found target and delete
                del current_level[tag]
                return True, True
            else:
                #continue down tree
                subcommands = current_level[tag].get("subcommands", {})
                success, child_deleted = _delete_recursive(subcommands, path_list, index + 1)
                
                #extra pruning
                if success:
                    if child_deleted:
                        node = current_level[tag]
                        if not node.get("subcommands") and node.get("type") == "parent_command":
                            del current_level[tag]
                            return True, True
                    return True, False
                
                return False, False

        success, _ = _delete_recursive(commands, path)
        
        if success:
            _save_commands(commands)
            if DEBUGGER:
                chain = " -> ".join(path)
                print(f"Command deleted: {chain}")
            return True
        else:
            if DEBUGGER:
                chain = " -> ".join(path)
                print(f"Error: Command '{chain}' not found")
            return False

    except Exception as e:
        if DEBUGGER: print(f"An error occurred while deleting a command: {e}")
        return False
    
    
def delete_all_commands(): #wipes COMMAND_FILE. Returns true if completed
    if not COMMAND_FILE.exists():
        if DEBUGGER: print(f"Error: {COMMAND_FILE} does not exist")
        return False
    
    try:
        _save_commands({})
        if DEBUGGER: print("All commands wiped successfully.")
        return True
    except Exception as e:
        if DEBUGGER: print(f"An error has occurred while deleting all commands: {e}")
        return False
    

def command_matches(input_text: str): #returns command matches in an array if match found from left to right
    if not input_text:
        return list(_load_commands().keys())
        
    input_tokens = input_text.split()
    current_level = _load_commands()
    
    #traverse tree
    for token in input_tokens[:-1]:
        #check in current level
        if isinstance(current_level, dict) and token in current_level:
            current_level = current_level[token].get("subcommands", {})
        else:
            return []
            
    last_token = input_tokens[-1]
    
    if isinstance(current_level, dict):
        return [command for command in current_level.keys() if command.startswith(last_token)]
        
    return []


def command_matches_no_bounds(input_text: str): #same as command_matches but from anywhere within the command
    if not input_text:
        return list(_load_commands().keys())
        
    input_tokens = input_text.split()
    current_level = _load_commands()
    
    #traverse tree
    for token in input_tokens[:-1]:
        #check current level
        if isinstance(current_level, dict) and token in current_level:
            current_level = current_level[token].get("subcommands", {})
        else:
            return []
            
    last_token = input_tokens[-1]
    
    if isinstance(current_level, dict):
        return [command for command in current_level.keys() if last_token in command]
        
    return []


def choose_command(command_options, choice: int): #command_options must be an array of strings, choice must be an int. Returns a command
    #check for invalid choice
    if choice > len(command_options) or choice <= 0:
        if DEBUGGER: print(f"Error: {choice} is invalid")
        return None
    
    return command_options[choice-1]


def change_file_name(name: str): #assign new file name. NOTE: Does not change file name in system if the file already exists
    global COMMAND_FILE_NAME
    global COMMAND_FILE
    COMMAND_FILE_NAME = f"{name}.json"
    COMMAND_FILE = Path(COMMAND_FILE_NAME)


def complete_command(command: str): #NOTE: Feature incomplete, read README.md for more information
    if DEBUGGER: print("Error: complete_command function has not been implemented")


def set_file_location(location): #for COMMAND_FILE. Intakes a directory or different json file name. 
    global COMMAND_FILE
    global COMMAND_FILE_NAME

    if DEBUGGER: print(f"Current file path: {COMMAND_FILE.resolve()}") #prints error if COMMAND_FILE hasn't been created (Error: commands.json does not exist)
    location_path = Path(location.strip()) 
    
    #check for json file
    if location_path.suffix == '.json':
        location_path.parent.mkdir(parents=True, exist_ok=True)
        COMMAND_FILE = location_path
        COMMAND_FILE_NAME = location

    #move to new path
    else:
        location_path.mkdir(parents=True, exist_ok=True)
        COMMAND_FILE = location_path / COMMAND_FILE_NAME
        
    if DEBUGGER: print(f"File path updated to: {COMMAND_FILE.resolve()}\n")


def toggle_debugger(): #toggles DEBUGGER on or off
    global DEBUGGER
    DEBUGGER = not DEBUGGER
    if DEBUGGER: print(f"DEBUGGER is now on")


def check_type(*command: str, type: str):
    if DEBUGGER: print("Error: check_type has not been implemented yet")


#############
#helper funcs
#############

def _load_commands(): #loads commands from COMMAND_FILE
    if not COMMAND_FILE.exists():
        if DEBUGGER: print(f"Error: {COMMAND_FILE} does not exist")
        return {}
    
    try:
        with COMMAND_FILE.open('r') as file:
            return json.load(file)
        
    except Exception as e:
        if DEBUGGER: print(f"An error occurred while running _load_commands: {e}")
        return {}


def _save_commands(commands): #saves commands to COMMAND_FILE
    try:
        with COMMAND_FILE.open('w') as file:
            json.dump(commands, file, indent=4)

    except Exception as e:
        if DEBUGGER: print(f"An error occurred while running _save_commands: {e}")
    



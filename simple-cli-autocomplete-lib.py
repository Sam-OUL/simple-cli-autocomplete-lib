from pathlib import Path

COMMAND_FILE_NAME = "commands.txt" #default name
COMMAND_FILE = Path(COMMAND_FILE_NAME) #for pathing

def create_command(command): #returns true if command was created
    try:
        with open(COMMAND_FILE, 'a') as file:
            file.write(command + "\n")
            print(f"Command created: {command}")
        return True
    
    except Exception as e:
        print(f"An error occured: {e}")
        return False



def delete_command(command): #returns true if command is deleted   
    if not COMMAND_FILE.exists():
        print(f"Error: {COMMAND_FILE} does not exist.")
        return False
        
    lines = []
    deleted = False
    command = command.strip()
    
    try:
        with COMMAND_FILE.open('r') as file:
            for line in file:
                if line.strip() != command:
                    lines.append(line)
                else:
                    deleted = True
                    
        with COMMAND_FILE.open('w') as file:
            file.writelines(lines)
            
        if not deleted:
            print(f"Error: {command} not found")
        return deleted

    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    
    
def delete_all_commands(): #wipes COMMAND_FILE. Returns true if completed
    if not COMMAND_FILE.exists():
        print(f"Error: {COMMAND_FILE} does not exist")
        return False
    
    try:
        with COMMAND_FILE.open('w') as file:
            return True
    
    except Exception as e:
        print(f"An error has occured: {e}")
        return False



def command_matches(command): #returns command matches in an array if match found from left to right
    matches = []
    
    try:
        with open(COMMAND_FILE, 'r') as file:
            for line in file:
                command_strip = line.strip()
                
                if command_strip.startswith(command):
                    matches.append(command_strip)

        print(f"Matches found: {matches}")            
        return matches
                
    except FileNotFoundError:
        print(f"Error: {COMMAND_FILE} not found.")
        return []
    

def command_matches_no_bounds(command): #same as command_matches but from anywhere within the command
    matches = []
    
    try:
        with open(COMMAND_FILE, 'r') as file:
            for line in file:
                command_strip = line.strip()
                
                if command.strip() in command_strip:
                    matches.append(command_strip)

        print(f"Matches found: {matches}")            
        return matches
                
    except FileNotFoundError:
        print(f"Error: {COMMAND_FILE} not found.")
        return []


def choose_command(command_options, choice): #command_options must be an array of strings, choice must be an int. Returns a command
    if choice > len(command_options) or choice <= 0:
        print(f"Error: {choice} is invalid")
        return None
    
    else:
        return command_options[choice-1]


def change_file_name(name): #assign new file name. NOTE: Does not change file name in system if the file already exists
    global COMMAND_FILE_NAME
    global COMMAND_FILE
    COMMAND_FILE_NAME = f"{name}.txt"
    COMMAND_FILE = Path(COMMAND_FILE_NAME)


def complete_command(command): #NOTE: Feature incomplete, read README.md for more information
    print("Error: complete_command function has not been implemented")


def set_file_location(location): #for COMMAND_FILE. Intakes a directory or different txt file name. 
    global COMMAND_FILE
    print(f"Current file path: {COMMAND_FILE.resolve()}")    
    location = Path(location.strip()) 
    
    #check for .txt
    if location.suffix == '.txt':
        location.parent.mkdir(parents=True, exist_ok=True)
        COMMAND_FILE = location

    #move to new path
    else:
        location.mkdir(parents=True, exist_ok=True)
        COMMAND_FILE = location / COMMAND_FILE_NAME
        
    print(f"File path updated to: {COMMAND_FILE.resolve()}\n")


# simple-cli-autocomplete-lib
A simple command line interface autocomplete library. Made for creating custom cli's with autocomplete. Current build version: 1.1

## Function List
| Command                                  | Description                                                                                                                                                                                                                                                  |
|------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `create_command(command)`                | Creates a new command to `COMMAND_FILE`. Returns true if successful                                                                                                                                                                                          |
| `delete_command(command)`                | Deletes command from `COMMAND_FILE`. Returns true if successful                                                                                                                                                                                              |
| `delete_all_commands()`                  | Wipes `COMMAND_FILE`. Returns true if successful                                                                                                                                                                                                             |
| `command_matches(command)`               | Checks `COMMAND_FILE` for matches then returns an array of these matches found from left to right (Ex: input is "sup", output is ["super" , "supurb"])                                                                                                       |
| `command_matches_no_bound(command)`      | Same as `command_matches(command)` but from anywhere within the command (Ex: input is "he", output is ["she" , "hello"]                                                                                                                                      |
| `choose_command(command_options, choice)`| Choose a command from `command_options` which is a string array of commands. `choice` is an int and options are chosen starting from an index of 1. Returns chosen command                                                                                   |
| `change_file_name(name)`                 | Assigns a new file name for `COMMAND_FILE` (also changes `COMMAND_FILE_NAME`). Intakes a string(just input the name, don't add .txt to the end). NOTE: Does not change file name in system if the command file already exists                                |
| `complete_command(command)`              | Feature incomplete. Please implement your own complete command system due to the unknown of how a custom cli takes input. Overriding keyboard is an option. Please see [keyboard override implementation](#keyboard-override-implementation) in this README  |
| `set_file_location(location)`            | Changes the path of `COMMAND_FILE`. Intakes a path or a txt file. NOTE: Does not move the command file, instead it selects a new "command file" with either the new txt file name or `COMMAND_FILE_NAME`                                                     |
| `toggle_debugger`                        | Toggles if debugger is eneabled. When enabled actions and errors are printed                                                                                                                                                                                 |
|                                          |                                                                                                                                                                                                                                                              |
| MISC                                     | Description                                                                                                                                                                                                                                                  |
| `COMMAND_FILE`                           | A path to the command file that stores your commands                                                                                                                                                                                                         |
| `COMMAND_FILE_NAME`                      | The name of the command file                                                                                                                                                                                                                                 |

## Installation
* Download simple-cli-autocomplete-lib.py
* Allow whatever script to access this script (an option is to move it into the same directory as the script you would like to access it in)
* Add import `simple-cli-autocomplete-lib.py` to your python script
* Enjoy using simple-cli-autocompete-lib.py

## Keyboard-override-implementation
* An option to implement `complete_command(command)` by overriding users keyboard and types out the command
* Install pyautogui. `pip install pyautogui`
* Within `simple-cli-autocomplete-lib.py` add `import pyautogui`
* Inside of `complete_command(command)` function, add `pyautogui.write(command)` and delete the print error statement
* Save and exit
* This library will now have the feature of completing the command. NOTE: Program may require admin privileges to use due to simulating keyboard inputs, this also does not work with wayland (Check if your os uses wayland first)

## Update plans
* Add "smart" command matching (command order)
* Add fuzzy command matching with scores
* Optimization (load commands once when library initializes instead of always accessing through disc)

## Contact
Contact me at soleitenb@gmail.com for any questions

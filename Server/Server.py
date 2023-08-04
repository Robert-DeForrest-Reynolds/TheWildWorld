from subprocess import *
from sys import platform, exit
from glob import glob
from os import remove, removedirs, getcwd
from os.path import join

ProjectFilePath = join("Source", "Levi.py")

Key = None

with open("Keys.txt"):
    KeyData = open("Keys.txt", "r").readlines()
    Keys = {Line.split("_")[0].lower():Line.split("_")[1] for Line in KeyData}

if platform == 'win32':
    python_path = join(".venv","Scripts","python")
elif platform.startswith('linux'):
    python_path = join(".venv","bin","python3")
    
def Py_Cache_Clean_Up():
    print("\nCommencing PyCache Clean Up")
    project_path = getcwd()
    py_cache_file_path = join(project_path, "**", "*.pyc")
    print(py_cache_file_path)
    py_cache_files = glob(py_cache_file_path, recursive=True)
    print(py_cache_files)
    py_cache_folders = glob(join("**","__pycache__"), recursive=True)
    for file in py_cache_files:
        try:
            remove(file)
        except OSError:
            print("Error removing .pyc files.")
    for directory in py_cache_folders:
        try:
            removedirs(directory)
        except OSError:
            print("Error removing _pycache__ directories.")

def BotExists():
    try:
        Bot
    except NameError:
        return False
    else:
        return True

def Start():
    global Bot
    Bot = Popen([python_path, join(ProjectFilePath), Key, KeySelection])


def Restart():
    global Bot
    if BotExists():
        print("Discord bot stopped")
        Bot.kill()
        Bot = Popen([python_path, join(ProjectFilePath), Key, KeySelection])
        print("Discord bot restarted")
    else:
        print("There isn't a running bot")


def Exit():
    global Bot
    if BotExists() == False:
        Py_Cache_Clean_Up()
        exit()
    else:
        print("There is a running bot")


def Stop():
    global Bot
    if BotExists():
        print("Discord bot stopped")
        Bot.kill()
        del Bot
    else:
        print("There isn't a running bot")


def Emergency_Stop():
    global Bot
    if BotExists() == False:
        print("You used this command wrong. Stopping bot altogether if it's even running, and closing script. Stop using this command if you don't know what you're doing please. Talk to Robert.")
        Py_Cache_Clean_Up()
        exit()

    if BotExists():
        print("Discord bot stopped")
        Bot.kill()
        del Bot
        Py_Cache_Clean_Up()
        exit()

def Clear_Logs():
    for File in glob("Source\\Logs\\*.log"):
        try:
            remove(File)
        except OSError:
            print("Error removing log files for some reason")

CommandDictionary = {"start": Start,
                     "restart": Restart,
                     "exit": Exit,
                     "stop": Stop,
                     "//": Emergency_Stop,
                     "clear logs": Clear_Logs}

while Key is None:
    print(f"Please select the key you'd like to run with.\nSelections:{Keys.keys()}")
    KeySelection = input("> ").lower()
    print(KeySelection)
    if KeySelection in Keys.keys():
        Key = Keys[KeySelection.lower()]
    else:
        print("Improper selection.")

while True:
    admin_input = input()
    print("Input command: ", admin_input)
    try:
        CommandDictionary[admin_input.lower()]()
    except KeyError:
        print("Invalid command.")
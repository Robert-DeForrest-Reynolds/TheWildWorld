from subprocess import *
from sys import platform, exit
from glob import glob
from os import remove, removedirs, getcwd
from os.path import join

key = ''
tester = ''

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
        except FileNotFoundError:
            print("Error removing .pyc files.")
    for directory in py_cache_folders:
        try:
            removedirs(directory)
        except FileNotFoundError:
            print("Error removing _pycache__ directories.")

while True:
    global Bot
    global bot_exists

    admin_input = input()
    print("Input command: ", admin_input)

    if admin_input == "start":
        Bot = Popen([python_path, join("Source", "Levi.py")])

    if admin_input == "restart":
        if Bot:
            print("Discord bot stopped")
            Bot.kill()
            Bot = Popen([python_path, join("Source", "Levi.py")])
            print("Discord bot restarted")
        else:
            print("There isn't a running bot")

    if admin_input == 'exit':
        try:
            Bot
        except NameError:
            bot_exists = False
        else:
            bot_exists = True

        if not bot_exists:
            Py_Cache_Clean_Up()
            exit()
        else:
            print("There is a running bot")

    if admin_input == "stop":
        if Bot:
            print("Discord bot stopped")
            Bot.kill()
            del Bot
        else:
            print("There isn't a running bot")

    if admin_input == '//':
        try:
            Bot
        except NameError:
            bot_exists = False
        else:
            bot_exists = True

        if bot_exists == False:
            print("You used this command wrong. Stopping bot altogether if it's running, and closing script. Stop using this command if you don't know what you're doing please. Talk to Robert.")
            Py_Cache_Clean_Up()
            exit()

        if Bot:
            print("Discord bot stopped")
            Bot.kill()
            del Bot
            Py_Cache_Clean_Up()
            exit()

    if admin_input == "help":
        print("Commands: start, restart, stop, exit, //")

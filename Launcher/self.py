from sys import platform, exit
from os import remove, removedirs, getcwd
from os.path import join
from subprocess import *
from glob import glob


class Launcher:
    def __init__(self):
        self.Key = None
        self.VirtualEnvironmentPath = join(".venv","Scripts","python")
        self.ProjectFilePath = join("Source", "Levi.py")
        self.CommandDictionary = {"start": self.Start,
                                  "restart": self.Restart,
                                  "exit": self.Exit,
                                  "stop": self.Stop,
                                  "//": self.Emergency_Stop,
                                  "clear logs": self.Clear_Logs}
        self.Read_Key_File()
        self.Key_Selection()
        self.User_Input()


    def Read_Key_File(self):
        with open("Keys.txt"):
            self.KeyData = open("Keys.txt", "r").readlines()
            self.Keys = {Line.split("_")[0].lower():Line.split("_")[1] for Line in self.KeyData}


    def Key_Selection(self):
        while self.Key is None:
            print(f"Please select the key you'd like to run with.\nSelections:{self.Keys.keys()}")
            self.KeySelection = input("> ").lower()
            print(self.KeySelection)
            if self.KeySelection in self.Keys.keys():
                self.Key = self.Keys[self.KeySelection.lower()]
            else:
                print("Improper selection.")


    def User_Input(self):
        while True:
            admin_input = input()
            print("Input command: ", admin_input)
            try:
                self.CommandDictionary[admin_input.lower()]()
            except KeyError:
                print("Invalid command.")
    

    def BotExists(self):
        try:
            Bot
        except NameError:
            return False
        else:
            return True


    def Start(self):
        global Bot
        Bot = Popen([self.VirtualEnvironmentPath, join(self.ProjectFilePath), self.Key, self.KeySelection])


    def Restart(self):
        global Bot
        if self.BotExists():
            print("Discord bot stopped")
            Bot.kill()
            Bot = Popen([self.VirtualEnvironmentPath, join(self.ProjectFilePath), self.Key, self.KeySelection])
            print("Discord bot restarted")
        else:
            print("There isn't a running bot")


    def Exit(self):
        global Bot
        if self.BotExists() == False:
            exit()
        else:
            print("There is a running bot")


    def Stop(self):
        global Bot
        if self.BotExists():
            print("Discord bot stopped")
            Bot.kill()
            del Bot
        else:
            print("There isn't a running bot")


    def Emergency_Stop(self):
        global Bot
        if self.BotExists() == False:
            print("Bot is not running it seems, stopping altogether though.")
            exit()

        if self.BotExists():
            print("Discord bot stopped")
            Bot.kill()
            del Bot
            exit()


    def Clear_Logs(self):
        for File in glob("Source\\Logs\\*.log"):
            try:
                remove(File)
            except OSError:
                print("Error removing log files for some reason")
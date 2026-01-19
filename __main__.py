from sys import exit
if __name__ != "__main__": exit()


from EverburnLauncher.Library.EverburnBot import EverburnBot
from EverburnLauncher.Library.Panel import Panel

TheWildWorld:EverburnBot = EverburnBot()
TheWildWorld.Panel = Panel
TheWildWorld.Bot.run(TheWildWorld.Token)

TheWildWorld.Output("stopped")
exit()
from sys import exit
if __name__ != "__main__": exit()


from EverburnLauncher.Library.EverburnBot import EverburnBot
from EverburnLauncher.Library.Dashboard import Dashboard

TheWildWorld:EverburnBot = EverburnBot()
TheWildWorld.Dashboard = Dashboard
TheWildWorld.Bot.run(TheWildWorld.Token)

TheWildWorld.Output("stopped")
exit()
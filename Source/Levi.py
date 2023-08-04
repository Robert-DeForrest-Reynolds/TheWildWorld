from discord import Intents
from discord.ext import commands
from Gameplay.PlayPanel import PlayPanel
from Player import Player
from TWD import TWD
from CreateProfile import CreateProfile
import logging
import logging.handlers
from time import strftime

from sys import argv

Logger = logging.getLogger('discord')
Logger.setLevel(logging.DEBUG)
logging.getLogger('discord.http').setLevel(logging.INFO)
Handler = logging.handlers.RotatingFileHandler(
    filename=f'Source\\Logs\\{strftime("%d_%m_%Y_%H-%M")}.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
Handler.setFormatter(formatter)
Logger.addHandler(Handler)

class GD: # Global Data
    def __init__(self):
        self.FoundsGuilds = {}
        self.FoundMembers = {}
        self.LeviDatabase = None
        self.Key = None
        self.KeyType = None
        self.Debug = False
        self.Unstable = False

GlobalData = GD()

GlobalData.Key = argv[1]
GlobalData.KeyType = argv[2]

if GlobalData.KeyType == "testing":
    GlobalData.Debug = True
    GlobalData.Unstable = False
elif GlobalData.KeyType == "unstable":
    GlobalData.Debug = True
    GlobalData.Unstable = True

intents = Intents.all()
intents.members = True
Levi = commands.Bot(command_prefix=['T', 't'], intents=intents)


@Levi.event
async def on_member_join(Member):
    await CreateProfile(Member, GlobalData, Logger)


@Levi.event
async def on_ready():
    if GlobalData.Debug == True:
        for Guild in Levi.guilds:
            GlobalData.FoundsGuilds.update({str(Guild):Guild})
        for Member in GlobalData.FoundsGuilds["The Wild World - Dev Server"].members:
            GlobalData.FoundMembers.update({Member.name: Player(Member)})
        GlobalData.LeviDatabase = TWD(GlobalData)
    if GlobalData.Unstable == True:
        for Guild in Levi.guilds:
            GlobalData.FoundsGuilds.update({str(Guild):Guild})
        for Member in GlobalData.FoundsGuilds["The Wild World - Unstable"].members:
            GlobalData.FoundMembers.update({Member.name: Player(Member)})
        GlobalData.LeviDatabase = TWD(GlobalData)
    if GlobalData.Debug == False and GlobalData.Unstable == False:
        for Guild in Levi.guilds:
            GlobalData.FoundsGuilds.update({str(Guild):Guild})
        for Member in GlobalData.FoundsGuilds["The Wild World"].members:
            GlobalData.FoundMembers.update({Member.name: Player(Member)})
        GlobalData.LeviDatabase = TWD(GlobalData)

    GlobalData.LeviDatabase.Save_Global_Data(GlobalData)

@Levi.command(aliases=["WW", "ww", "wW", "Ww"])
async def Play_Command(Context):
    PlayPanel(Context, GlobalData)


@Levi.command("create_profile")
@commands.has_permissions(administrator=True)
async def Admin_Create_Profile(Context):
    Member = GlobalData.FoundMembers[Context.author.name].MemberObject
    await CreateProfile(Member, GlobalData, Logger)

@Levi.command("delete_profile")
@commands.has_permissions(administrator=True)
async def Delete_Profile(Context, GivenUsername):
    GlobalData.LeviDatabase.Cursor.execute(f"DELETE FROM Players WHERE Username='{GivenUsername}'")
    GlobalData.LeviDatabase.TWDCONNECTION.commit()
    Logger.info(f"Attempted to delete {GivenUsername}'s profile")
    if GivenUsername in GlobalData.LeviDatabase.Cursor.execute(f"SELECT Username FROM Players WHERE Username='{GivenUsername}'").fetchall()[0]:
        Logger.info(f"Successfully deleted {GivenUsername}'s profile")
    else:
        Logger.info(f"Successfully deleted {GivenUsername}'s profile")

print(f"Running bot as {GlobalData.KeyType}")
Logger.info(f"Running bot as {GlobalData.KeyType}")

Levi.run(GlobalData.Key)
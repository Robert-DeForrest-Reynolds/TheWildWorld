from discord import Intents, Member
from discord.ext import commands
from Gameplay.PlayPanel import PlayPanel
from Player import Player
from TWD import TWD
from CreateProfile import CreateProfile

class GD: # Global Data
    def __init__(self):
        self.LeviGuilds = {}
        self.LeviMembers = {}
        self.LeviDatabase = None

key = open("Keys.txt", "r").readlines()[0]
print(key)

GlobalData = GD()

intents = Intents.all()
intents.members = True
Levi = commands.Bot(command_prefix=['T', 't'], intents=intents)


@Levi.event
async def on_member_join(Member):
    await CreateProfile(Member, GlobalData)


@Levi.event
async def on_ready():
    for Guild in Levi.guilds:
        GlobalData.LeviGuilds.update({str(Guild):Guild})
    for Member in GlobalData.LeviGuilds["The Wild World"].members:
        GlobalData.LeviMembers.update({Member.name: Player(Member)})
    GlobalData.LeviDatabase = TWD(GlobalData)


@Levi.command(aliases=["WW", "ww", "wW", "Ww"])
async def PlayCommand(Context):
    PlayPanel(Context, GlobalData)


@Levi.command("create_profile")
@commands.has_permissions(administrator=True)
async def AdminCreateProfile(Context):
    Member = GlobalData.LeviMembers[Context.author.name].MemberObject
    await CreateProfile(Member, GlobalData)


Levi.run(key)
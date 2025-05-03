import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import json

load_dotenv()

# configuration
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.reactions = True
intents.message_content = True
THEME_COLOUR = discord.Color.from_str("#acc8dd")
REACTION_ID = None

# Officially map every name to emoji to role
color_reaction_roles = {
    "pbred":    (1366844855078227968, 1366845238530015392),
    "pborange": (1366844873155543100, 1366845382373671055),
    "pbyellow": (1366844880416018602, 1366845451566977076),
    "pbgreen":  (1366844890419298404, 1366845543292076134),
    "pbblue":   (1366857171748261978, 1366845823773704313),
    "pbviolet": (1366844897637826571, 1366845563366281366),
    "pbpink":   (1366844905858797630, 1366845571125477387),
    "pbwhite":  (1366844915451040035, 1366845579023486996),
}

def init():
    global REACTION_ID
    try:
        with open("reaction_config.json", "r") as f:
            data = json.load(f)
            REACTION_ID = data.get("message_id", None)
    except (FileNotFoundError, json.JSONDecodeError):
        REACTION_ID = None

emoji_role_map = {emoji_id: role_id for (_, (emoji_id, role_id)) in color_reaction_roles.items()}

bot = commands.Bot(command_prefix="!", intents=intents)
init()

@bot.command(name="info")
async def bot_help(ctx):
    embed = discord.Embed(
        title="📘 Help Menu",
        description="Here are the available commands:",
        color=THEME_COLOUR
    )
    embed.add_field(name="!setup_reaction_roles", value="Set up the reaction roles message.", inline=False)
    embed.add_field(name="!help", value="Display this help menu.", inline=False)
    embed.set_footer(text="jerry sucks")
    embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else discord.Embed.Empty)
    embed.set_image(url="https://media.discordapp.net/attachments/1100555348466741279/1368050518483800116/roles.png?ex=6816cfd4&is=68157e54&hm=ed49a11bd01e00e9767a858976d35a3d22c5910c2f9e8551549b551b5c040273&=&format=webp&quality=lossless&width=1522&height=856")
    await ctx.send(embed=embed)

@bot.command(name="reaction-role-embed")
async def reaction_role_embed(ctx):
    # make descripton
    def make_description(name, emoji_id, role_id):
        role = ctx.guild.get_role(role_id)
        return f"ㅤㅤㅤㅤㅤㅤ« <:bluecup:1366849510629707922> »ㅤㅤㅤ◌ㅤㅤㅤ<:{name}:{emoji_id}> {role.mention if role else '`missing role`'}"
    # send colour reaction role embed
    embed1 = discord.Embed(
      title="",
      description="",
      color = THEME_COLOUR
    )
    embed1.set_image(url="https://media.discordapp.net/attachments/1100555348466741279/1368050518483800116/roles.png?ex=6816cfd4&is=68157e54&hm=ed49a11bd01e00e9767a858976d35a3d22c5910c2f9e8551549b551b5c040273&=&format=webp&quality=lossless&width=1522&height=856")
    await ctx.send(embed=embed1)
    lines = [make_description(name, eid, rid) for name, (eid, rid) in color_reaction_roles.items()]
    embed2 = discord.Embed(
      title="˗ˏˋ ×ㅤㅤㅤPastel Coloursㅤㅤㅤ× ´ˎ˗",
      description="\n".join(lines),
      color = THEME_COLOUR
    )
    msg = await ctx.send(embed=embed2)
    # add reaction to colour embedA
    for emoji_name, (emoji_id, _) in color_reaction_roles.items():
        emoji = bot.get_emoji(emoji_id)
        await msg.add_reaction(f"<:{emoji_name}:{emoji_id}>")
    with open("reaction_config.json", "w") as f: 
        json.dump({"message_id": msg.id}, f)
    global REACTION_ID
    REACTION_ID = msg.id

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id != REACTION_ID:
        return
    role_id = emoji_role_map.get(payload.emoji.id)
    if role_id:
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        role = guild.get_role(role_id)
        print(f"Trying to add role: {role.name} ({role.id}) to {member.display_name} ({member.id})")
        await member.add_roles(role)
        print("Role successfully added (or no error)")

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id != REACTION_ID:
        return
    role_id = emoji_role_map.get(payload.emoji.id)
    if role_id:
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        role = guild.get_role(role_id)
        await member.remove_roles(role)

bot.run(os.getenv("DISCORD_TOKEN"))
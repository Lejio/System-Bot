
'''
    sys.py: The main file of the discord bot. Contains the helper discord class, contains all the discord command interations and functions. Connects all the discord features together here as well.
    
    Abilities:
    Generate embedded messages and if a user reacts using a certain emoji, add a specific role to that user.
    
    Roles gives different accesses to users.
    https://www.youtube.com/watch?v=WQsQERxtD2w&ab_channel=Carberra
    
    
    Commands (basic not including features):
    
    (new) - Default role that is granted for everyone entering the server for the first time. This role would have access to the verify channel and is then prompted to click a button. A admin would have to let that person in.
    
'''
import os
from datetime import datetime
from typing import Any
import tracemalloc

import discord
import logging

from discord import PermissionOverwrite, Embed
from discord.ext import commands

from dotenv import load_dotenv

from Roles.connector import GuildDatabase
from Roles.guildroles import GuildRoles
from Admin.init import Initialize

client = commands.Bot(command_prefix="!sys ", intents=discord.Intents.all())
cogs: list = ["Roles.role", "Admin.admin", "Admin.config"]
load_dotenv()

embed = None


class SystemBot(commands.Bot):

  def __init__(self, command_prefix="!sys", description: str | None = None, intents=discord.Intents.all(), **options: Any) -> None:
     super().__init__(command_prefix, description=description, intents=intents, **options)
     

  async def on_ready(self):
    """
    Client event. Runs when the bot is ready and has successfully logged in.
    """
    tracemalloc.start()

    print(f"\n{datetime.utcnow()}: Logged in successfully as: " + str(client.user) + "\n")

    try:
      
      for cog in cogs:  # Loads each config into the client.

        await client.load_extension(cog)
        print(f"Loaded cog {cog}")

      print("Successfully loaded all Cogs\n")
      
    except commands.ExtensionAlreadyLoaded:
      
      print("Extension already loaded")
      
    a = await self.tree.sync()
    print(f"{len(a)} Synced")
    
  
  async def on_guild_remove(self, guild: discord.Guild):
    
    print("Left guild: " + str(guild.id))
            
    
  async def on_guild_join(self, guild: discord.Guild):
    
    GuildDatabase(guild=guild)
    defroles = GuildRoles(guild=guild)
    
    uvrole = await guild.create_role(name="Archive")
    
    for cat in guild.categories:
      await cat.edit(overwrites={
        guild.default_role: PermissionOverwrite(read_messages=False)
      })
      for chan in cat.channels:
        await chan.edit(sync_permissions=True)
    
    cmdcenter = await guild.create_category(name="System Command Center", overwrites={
      guild.default_role: PermissionOverwrite(read_messages=False)}, position=0)
    
    
    uvrole = await guild.create_role(name=defroles.getGuildProperties()["default_role_unverified_name"])
    vrole = await guild.create_role(name=defroles.getGuildProperties()["default_role_verified_name"])
    
    defroles.editDefaultRole(name=uvrole.name, category="default_role_unverified_id", newVal=str(uvrole.id))
    defroles.editDefaultRole(name=vrole.name, category="default_role_verified_id", newVal=str(vrole.id))
    cmdcenter.position = 0
    
    welcome = await guild.create_category(name="Welcome", overwrites={
      guild.default_role: PermissionOverwrite(read_message=False)
    })
    welcome_channel = await welcome.create_text_channel(name="verify")
    await welcome.set_permissions(target=uvrole, read_messages=True, send_messages=False, add_reactions=False)
    
    welcome_embed = Embed(title=f"Welcome to {guild.name}")
    
    welcome_channel.send()

    
    # Set up view button that sends a another view into the command center for entry approval.
    
    
    init = Initialize(cmdcenter)
    await init.setup()
    

  async def on_member_join(self, member: discord.Member):
    defroles = GuildRoles(guild=member.guild)
    role = discord.utils.get(member.guild.roles, name=defroles.getGuildProperties()["default_role_unverified_name"])
    await member.add_roles(role)
    
    
client = SystemBot()


@client.tree.command(name="hello", description="A hello echoer.")
async def hello(interaction: discord.Interaction, member: discord.Member):
  """
    Test command. Echos back "Hello!".
  """
  embed = discord.Embed(title="test", description=f"{str(member)} said hello!", color=discord.Colour.yellow(), timestamp=datetime.utcnow())
  embed.add_field(name="Hello!", value="yes")
  await interaction.response.send_message(embed=embed)


@hello.error
async def helloError(ctx, error):
  """
    Test error. Should not happen anymore (if nothing major happens).
  """
  print(error)
  await ctx.send("Something is seriously wrong if this gets sent lol.")
  

@client.tree.command(name="role_check", description="Checks the roles of a specific member.")
async def checkRoles(interaction: discord.Interaction, member: discord.Member):
  roles = ""
  
  for role in member.roles:
    if role.name != "@everyone":
      roles += str(role) + "\n"
  
  print(roles)
  await interaction.response.send_message(roles)
  

@client.command("isowner?")
@commands.check_any(commands.is_owner())
async def owner(ctx):
  """
    Checks if the person using the command is the owner of the bot.
  """

  await ctx.send("You are the owner.")
  
@owner.error
async def ownerError(ctx, error):
  
  await ctx.send("You are not the owner.")
  
  
@client.command("initialize")
@commands.check_any(commands.is_owner())
async def initSetup(ctx):
  
  await ctx.send("Initializing bot setup phase.")


@client.command("status")
@commands.check_any(commands.is_owner())
async def statusbot(ctx):
  a, b = tracemalloc.get_traced_memory()
  print("Current Memory [KB]: " + str(round(a/1024)))
  print("Peak Memory [KB]: " + str(round(b/1024)))
  

@client.command("kill")
@commands.check_any(commands.is_owner())
async def killbot(ctx):
  
  tracemalloc.stop()
  
  await exit()
  



"""
  Runs the bot. Sometimes it gets a TooManyRequests error. In which it would promptly kill the program and restart. (This is the only current known fix).
"""
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

client.run(os.environ['OPENAI_KEY'], log_handler=handler)

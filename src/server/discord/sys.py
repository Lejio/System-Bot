
'''
    sys.py: The main file of the discord bot. Contains the helper discord class, contains all the discord command interations and functions. Connects all the discord features together here as well.
    
    Abilities:
    Generate embedded messages and if a user reacts using a certain emoji, add a specific role to that user.
    
    Roles gives different accesses to users.
    https://www.youtube.com/watch?v=WQsQERxtD2w&ab_channel=Carberra
    
    
    Commands (basic not including features):
    
    
'''
import os
from datetime import datetime

import discord
from discord.ext import commands
from dotenv import load_dotenv

client = commands.Bot(command_prefix="!sys ", intents=discord.Intents.all())
cogs: list = ["Roles.role"]
load_dotenv()

embed = None


@client.event
async def on_ready():
    """
    Client event. Runs when the bot is ready and has successfully logged in.
    """

    print(f"\n{datetime.utcnow()}: Logged in successfully as: " + str(client.user) + "\n")

    try:
      
      for cog in cogs:  # Loads each config into the client.
        # try:

        await client.load_extension(cog)
        print(f"Loaded cog {cog}")

      print("Successfully loaded all Cogs\n")
      
    except commands.ExtensionAlreadyLoaded:
      
      print("Extension already loaded")
    
    synced = await client.tree.sync()
    print(f"Synced {len(synced)} commands.")
    

@client.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name='Cybertronian Plebs')
    await member.add_roles(role)


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
  

# @client.tree.command()



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


  
  
  



"""
  Runs the bot. Sometimes it gets a TooManyRequests error. In which it would promptly kill the program and restart. (This is the only current known fix).
"""


client.run(os.environ['OPENAI_KEY'])

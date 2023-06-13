import discord
from discord import app_commands
from discord.emoji import Emoji
from discord.enums import ButtonStyle
from discord.ext import commands
from discord.interactions import Interaction
from discord.partial_emoji import PartialEmoji
from discord.ui import Button, View

from roleEnum import GAMINGROLE
from roleDbConnector import RoleDatabase

class RoleButton(discord.ui.Button):
    
    def __init__(self, role_id: int, guild: discord.Guild):
        
        
        super().__init__(style=discord.ButtonStyle.secondary, emoji="<:emoji_39:935315265468633148>")
        self.label = guild.get_role(role_id)
        self.role = guild.get_role(role_id)
        self.role_id = role_id
        self.guild = guild
        
        
    async def callback(self, interaction: discord.Interaction):
        
        member = interaction.user
        
        if member.get_role(self.role_id) == self.role:
            await interaction.user.remove_roles(self.role)
            await interaction.response.send_message(f"{self.role.name} role removed.", ephemeral=True)
        else:
            await interaction.user.add_roles(self.role)
            await interaction.response.send_message(f"{self.role.name} role added.", ephemeral=True)
    

class Roles(commands.Cog):
    
    
    def __init__(self) -> None:
        super().__init__()
        self.gameRoles = {"COC":None, "LOL":None, "CS:GO":None, "OW":None}
        
        
    @app_commands.command(name="buttontest", description="Button Embed Testing")
    async def buttonTest(self, interaction: discord.Interaction):
        """
        Button testing command. Sys bot displays one button. Upon user clicking on the button, the bot responds with a message.

        Args:
            interaction (discord.Interaction): Discord interaction object. Any "interaction" with commands are discord interactions.
        """

        
        
        # Creates a Discord View object.
        testView = View()
        
        # Creates a button.
        testButton = RoleButton(925962416272052275, interaction.guild)
        
        # Connects the created callback function to the testButton.
        # testButton.callback = callBackTest
        
        # Adds the button to the view.
        testView.add_item(testButton)
        
        # Sends view as interaction.
        await interaction.response.send_message(view=testView)
    
    
    @app_commands.command(name="extractroles", description="Programming purposes.")
    @commands.check_any(commands.is_owner())
    async def extractroles(self, interaction: discord.Interaction):
        
        roleDB = RoleDatabase("role_port")
        
        a = interaction.guild.members
        
        for i in a:
            roleDB.add_member(i)
            
        roleDB.close()
        
        await interaction.response.send_message(f"Role database updated successfully.")
        
    
    # https://discordpy.readthedocs.io/en/stable/api.html?highlight=create_role#discord.Guild.create_role
    @app_commands.command(name="createrole", description="Creates a role based on given parameters.")
    @commands.check_any(commands.is_owner())
    async def createrole(self, interaction: discord.Interaction, name: str, reason: str = None):
        
        await interaction.guild.create_role(name=name, colour=discord.Colour.dark_magenta(), reason=reason)
        
        await interaction.response.send_message(f"Created new role: {name}")
        
        
        
async def setup(bot):

  await bot.add_cog(Roles())
    
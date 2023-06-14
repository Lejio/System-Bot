from typing import Any, Dict, List, Optional, Union
import discord
from discord import app_commands
from discord.app_commands.commands import Group
from discord.app_commands.translator import locale_str
from discord.enums import ButtonStyle
from discord.ext import commands
from discord.interactions import Interaction
from discord.permissions import Permissions
from discord.ui import Button, View
from discord.utils import MISSING

from roleEnum import GAMINGROLE, COLORS
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
    

@app_commands.default_permissions(administrator=True)
class Roles(commands.GroupCog):
    
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        # self.app_command.default_permissions = discord.Permissions.administrator
        gameRoles = {"COC":None, "LOL":None, "CS:GO":None, "OW":None}
        
    @app_commands.command(name="choose", description="Button Embed Testing")
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
    
    
    
    
    @app_commands.command(name="backup_role_database", description="Programming purposes.")
    @commands.check_any(commands.is_owner())
    async def extractroles(self, interaction: discord.Interaction, backup_db_name: str):
        
        roleDB = RoleDatabase(backup_db_name)
        
        a = interaction.guild.members
        
        for i in a:
            roleDB.add_member(i)
            
        roleDB.close()
        
        await interaction.response.send_message(f"Role database updated successfully.")
        
    
    # color.name for color in COLORS
    # https://discordpy.readthedocs.io/en/stable/api.html?highlight=create_role#discord.Guild.create_role
    @app_commands.command(name="create", description="Creates a role based on given parameters.")
    @app_commands.describe(colors="Color selector")
    @app_commands.choices(colors=[discord.app_commands.Choice(name=color.name, value=color.value) for color in COLORS])
    
    # Default permissions mean only admins can access these commands.
    @app_commands.default_permissions(manage_roles=True, manage_permissions=True)
    
    # @app_commands.default_permissions(ban_members=True) Add the permission names and bool as  values to include access.
    async def createrole(self, interaction: discord.Interaction, name: str, colors: discord.app_commands.Choice[int], reason:str):
        
        await interaction.guild.create_role(name=name, colour=discord.Colour(colors.value), reason=reason)
        await interaction.response.send_message(f"Created new role: {name}")
        
    
    
    @app_commands.command(name="remove", description="Removes a Role.")
    @app_commands.default_permissions(manage_roles=True, manage_permissions=True)
    async def checkSocialStatus(self, interaction: discord.Interaction, role: discord.Role, reason: str = None):
        
        await role.delete(reason=reason)
        await interaction.response.send_message(f"Removed role {role.name}")
        
    
    @app_commands.command(name="testcommand", description="Test")
    @app_commands.default_permissions(administrator=True)
    async def test(self, interaction: discord.Interaction):
        
        # print(discord.Permissions._has_flag(discord.Permissions.manage_permissions))
        
        await interaction.response.send_message("You can ban members!")
    
    
        
async def setup(bot: commands.Bot):
    await bot.add_cog(Roles(bot))
    
import discord
from discord import app_commands
from discord.ext import commands

from roleEnum import GAMINGROLE, COLORS
from roleDbConnector import RoleDatabase

# Class decorator. Since GroupCog is the parent, then the permissions of the parent override its children.
@app_commands.default_permissions(administrator=True)
class Admin(commands.GroupCog):
    
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        # self.__cog_name__("role-command")

    
    @app_commands.command(name="backup_role_database", description="Programming purposes.")
    async def extractroles(self, interaction: discord.Interaction, backup_db_name: str):
        
        roleDB = RoleDatabase(backup_db_name)
        
        a = interaction.guild.members
        
        for i in a:
            roleDB.add_member(i)
            
        roleDB.close()
        
        await interaction.response.send_message(f"Role database updated successfully.")
        
    
    # color.name for color in COLORS
    # https://discordpy.readthedocs.io/en/stable/api.html?highlight=create_role#discord.Guild.create_role
    @app_commands.command(name="role-create", description="Creates a role based on given parameters.")
    @app_commands.describe(colors="Color selector")
    @app_commands.choices(colors=[discord.app_commands.Choice(name=color.name, value=color.value) for color in COLORS])
    
    # Default permissions mean only admins can access these commands.
    @app_commands.default_permissions(manage_roles=True, manage_permissions=True)
    
    # @app_commands.default_permissions(ban_members=True) Add the permission names and bool as  values to include access.
    async def createrole(self, interaction: discord.Interaction, name: str, colors: discord.app_commands.Choice[int], reason:str):
        
        await interaction.guild.create_role(name=name, colour=discord.Colour(colors.value), reason=reason)
        await interaction.response.send_message(f"Created new role: {name}")
        
    
    
    @app_commands.command(name="role-remove", description="Removes a Role.")
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
    await bot.add_cog(Admin(bot))
import discord
from discord import app_commands
from discord.ext import commands

from sysenum import REG_COLORS, DARK_COLORS, LIGHT_COLORS
from Roles.guildroles import GuildRoles
# from roleDbConnector import RoleDatabase

# Class decorator. Since GroupCog is the parent, then the permissions of the parent override its children.
@app_commands.default_permissions(administrator=True)
class Admin(commands.GroupCog):
    
    def __init__(self, client: commands.Bot) -> None:
        super().__init__()

        self.client = client;


    # https://discordpy.readthedocs.io/en/stable/api.html?highlight=create_role#discord.Guild.create_role
    @app_commands.command(name="role-create", description="Creates a role based on given parameters.")
    @app_commands.describe(dark_color="Dark color selector", light_color="Light color selector", reg_color="Default colors")
    @app_commands.choices(dark_color=[discord.app_commands.Choice(name=color.name, value=color.value) for color in DARK_COLORS],
                          light_color=[discord.app_commands.Choice(name=color.name, value=color.value) for color in LIGHT_COLORS],
                          reg_color=[discord.app_commands.Choice(name=color.name, value=color.value) for color in REG_COLORS])

    async def createRole(self, interaction: discord.Interaction, name: str, reg_color: discord.app_commands.Choice[int]=None, dark_color: discord.app_commands.Choice[int]=None, light_color: discord.app_commands.Choice[int]=None, reason: str = None):
        
        if ([reg_color, dark_color, light_color].count(None) < 2):
            await interaction.response.send_message("You can only choose one color!")
        
        else:
            
            if reg_color != None:
                await interaction.guild.create_role(name=name, colour=discord.Colour(reg_color.value), reason=reason)
                await interaction.response.send_message(f"Created new role: {name}")
                
            elif light_color != None:
                await interaction.guild.create_role(name=name, colour=discord.Colour(light_color.value), reason=reason)
                await interaction.response.send_message(f"Created new role: {name}")
                
            elif dark_color != None:
                await interaction.guild.create_role(name=name, colour=discord.Colour(dark_color.value), reason=reason)
                await interaction.response.send_message(f"Created new role: {name}")
                
            else:
                await interaction.response.send_message("You need to choose a color!")        
        
    
    
    @app_commands.command(name="role-remove", description="Removes a Role.")
    async def checkSocialStatus(self, interaction: discord.Interaction, role: discord.Role, reason: str = None):
        
        try:
            await role.delete(reason=reason)
            guildroles = GuildRoles(interaction.guild)
            guildroles.removeRole()
            await interaction.response.send_message(f"Removed role {role.name}")
            
        except discord.errors.HTTPException:
            await interaction.response.send_message("Invalid role!")
            
    
    @app_commands.command(name="testcommand", description="Test")
    async def test(self, interaction: discord.Interaction):
                
        await interaction.response.send_message("You can ban members!")
    
    
        
async def setup(bot: commands.Bot):
    await bot.add_cog(Admin(bot))
from discord.ui import Button
from discord import Guild, ButtonStyle, Interaction, app_commands, Colour, utils
from discord.ui import View
from discord.ext import commands
from discord import Embed
# from discord.utils import 

from Roles.connector import GuildDatabase
from Roles.guildRoles import GuildRoles


class RoleButton(Button):
    
    
    def __init__(self, role_id: int, interaction: Interaction, emoji: str = None):
        
        super().__init__(style=ButtonStyle.secondary, emoji=emoji)
        self.role = interaction.guild.get_role(role_id)
        self.role_id = role_id
        self.guild = interaction.guild
        
        
    async def callback(self, interaction: Interaction):
        """Callback function for the role button.

        Args:
            interaction (Interaction): discord.Interaction with the view.
        """
        
        member = interaction.user
        
        if member.get_role(self.role_id) == self.role:
            await interaction.user.remove_roles(self.role)
            await interaction.response.send_message(f"{self.role.name} role removed.", ephemeral=True)
        else:
            await interaction.user.add_roles(self.role)
            await interaction.response.send_message(f"{self.role.name} role added.", ephemeral=True)
            

class Role(commands.Cog):
    
    def __init__(self) -> None:
        super().__init__()
        
    
    @app_commands.command(name="init-roles", description="Button Embed Testing")
    @app_commands.default_permissions(administrator=True)
    async def buttonTest(self, interaction: Interaction):
        """
        Button testing command. Sys bot displays one button. Upon user clicking on the button, the bot responds with a message.

        Args:
            interaction (discord.Interaction): Discord interaction object. Any "interaction" with commands are discord interactions.
        """

        # Creates a Discord View object.
        roleView = View()
        
        guilddatabase = GuildDatabase(interaction.guild)
        guildroles = GuildRoles(interaction.guild)
        
        roles = guildroles.getGuildRoles()
        
        try:
            
            for i in roles:

                roleView.add_item(RoleButton(int(roles[i]['role_id']), interaction, roles[i]['emoji_id']))
        
        except TypeError:
            
            print("Creating default roles.")
            await self.initRoles(interaction.guild, guildroles)
            
            for i in guildroles.getGuildRoles():

                roleView.add_item(RoleButton(int(roles[i]['role_id']), interaction, roles[i]['emoji_id']))
            
        embedBody = ""
        
        for r in roles:
            embedBody += f"{roles[r]['emoji_id']} - {r}\n"
            
        embed = Embed(title="Choose your roles!")
        embed.description = embedBody
        
        # Sends view as interaction.
        await interaction.response.send_message(view=roleView, embed=embed)
        
    
    @app_commands.command(name="removeall", description="REMOVES ALL ROLES")
    @app_commands.default_permissions(administrator=True)
    async def removeallroles(self, interaction: Interaction):
        
        roles = interaction.guild.roles
        
        await interaction.response.send_message("Deleted all roles.")
        
        for r in roles:
            if r != interaction.guild.default_role and not r.permissions.administrator:
                await r.delete()
        
    
    async def initRoles(self, guild: Guild, guildRoles: GuildRoles):
        """Generates the default roles contained in default.json.

        Args:
            guild (Guild): Interaction guild.
            guildRoles (GuildRoles): Guild json connector.
        """
        for r in guildRoles.getGuildRoles():
            await guild.create_role(name=r, colour=Colour.from_str(guildRoles.getGuildRoles()[r]["colour"]), reason="SYS INITIAL ROLE")
            guildRoles.editRole(name=r, category="role_id", newVal=str(utils.get(guild.roles, name=r).id))
            
    @app_commands.command(name="logocheck", description="Checks logo")
    @app_commands.default_permissions(administrator=True)
    async def logocheck(self, interaction: Interaction):
        
        await interaction.response.send_message("<:leagueoflegendslogo:1118578542658203758>")


async def setup(bot: commands.Bot):
    await bot.add_cog(Role())
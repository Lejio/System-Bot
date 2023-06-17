from discord.ui import Button
from discord import Guild, ButtonStyle, Interaction, app_commands, Colour, utils
from discord.ui import View
from discord.ext import commands

from Roles.guildRoles import GuildRoles

class RoleButton(Button):
    
    def __init__(self, role_id: int, interaction: Interaction, emoji: str = None):
        
        
        super().__init__(style=ButtonStyle.secondary, emoji=emoji)
        self.role = interaction.guild.get_role(role_id)

        self.role_id = role_id
        self.guild = interaction.guild
        
        
    async def callback(self, interaction: Interaction):
        
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
        
    
    @app_commands.command(name="choose", description="Button Embed Testing")
    @app_commands.default_permissions(administrator=True)
    async def buttonTest(self, interaction: Interaction):
        """
        Button testing command. Sys bot displays one button. Upon user clicking on the button, the bot responds with a message.

        Args:
            interaction (discord.Interaction): Discord interaction object. Any "interaction" with commands are discord interactions.
        """

        # Creates a Discord View object.
        testView = View()
        
        guildroles = GuildRoles(interaction.guild)
        await self.initRoles(interaction.guild, guildroles)
        
        
        
        for i in guildroles.getGuildRoles():

            testView.add_item(RoleButton(int(guildroles.getGuildRoles()[i]['role_id']), interaction, guildroles.getGuildRoles()[i]['emoji_id']))
        
        # Sends view as interaction.
        await interaction.response.send_message(view=testView)
        
    @app_commands.command(name="remove-all-roles", description="REMOVES ALL ROLES")
    @app_commands.default_permissions(administrator=True)
    async def removeallroles(self, interaction: Interaction):
        
        roles = interaction.guild.roles
        
        await interaction.response.send_message("Deleted all roles.")
        
        for r in roles:
            if r != interaction.guild.default_role and not r.permissions.administrator:
                await r.delete()
        
        
    
    async def initRoles(self, guild: Guild, guildRoles: GuildRoles):
        for r in guildRoles.getGuildRoles():
            # print(r)
            await guild.create_role(name=r, colour=Colour.from_str(guildRoles.getGuildRoles()[r]["colour"]), reason="SYS INITIAL ROLE")
            guildRoles.editRole(name=r, category="role_id", newVal=str(utils.get(guild.roles, name=r).id))
            
    @app_commands.command(name="test-role", description="Test")
    @app_commands.default_permissions(administrator=True)
    async def removeallroles(self, interaction: Interaction):
            
            await interaction.response.send_message(interaction.guild.get_role(1119443557724467252).name)


async def setup(bot: commands.Bot):
    await bot.add_cog(Role())
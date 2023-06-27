from discord import Guild, ButtonStyle, Interaction, app_commands, Colour, utils, Embed, PermissionOverwrite
from discord.ext import commands
from discord.interactions import Interaction
from discord.ui import Button, View
from discord.enums import ButtonStyle


from Roles.connector import GuildDatabase
from Roles.guildRoles import GuildRoles
    

class RoleButton(Button):
    
    def __init__(self, role_id: int, guild: Guild, emoji: str = None, custom_id: str = str):
        
        super().__init__(style=ButtonStyle.secondary, emoji=emoji)
        self.role = guild.get_role(role_id)
        self.role_id = role_id
        self.guild = guild
        self.custom_id = custom_id
        
        
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


class RoleView(View):
    
    def __init__(self, guild: Guild):
        super().__init__(timeout=None)
        
        GuildDatabase(guild)
        self.__guildroles = GuildRoles(guild)
        self.__roles = self.__guildroles.getGuildRoles()
        self.__guild = guild
        
        self.createButtons()
        
    
    def createButtons(self):
            
            for i in self.__guildroles.getGuildRoles():

                self.add_item(RoleButton(int(self.__roles[i]['role_id']), self.__guild, self.__roles[i]['emoji_id'], self.__roles[i]['custom_id']))
                
                
    def getRoles(self) -> dict:
        
        return self.__roles
    
    
    def getGuildRoles(self) -> GuildRoles:
        
        return self.__guildroles
        

class Role(commands.Cog):
    
    def __init__(self) -> None:
        super().__init__()
        
    
    @app_commands.command(name="inititialize-role-selector", description="Button Embed Testing")
    @app_commands.default_permissions(administrator=True)
    async def buttonTest(self, interaction: Interaction):
        """
        Button testing command. Sys bot displays one button. Upon user clicking on the button, the bot responds with a message.

        Args:
            interaction (discord.Interaction): Discord interaction object. Any "interaction" with commands are discord interactions.
        """

        # Creates a Discord View object.
        guildroles = GuildRoles(interaction.guild)
        
        if not (guildroles.__status__()):
            await self.initRoles(interaction.guild, guildroles)
            guildroles.__changestatus__()
        
        roleView = RoleView(interaction.guild)
        roles = roleView.getRoles()
            
        embedBody = ""
        
        for r in roles:
            embedBody += f"{roles[r]['emoji_id']} - {r}\n"
            
        embed = Embed(title="Choose your roles!")
        embed.description = embedBody
        
        channel = await self.createRoleTextChannel(interaction.guild)
        
        # Sends view as interaction.
        await channel.send(view=roleView, embed=embed)
        await interaction.response.send_message("Created new roles channel.")
    
    
    async def initRoles(self, guild: Guild, guildRoles: GuildRoles):
        """Generates the default roles contained in default.json.

        Args:
            guild (Guild): Interaction guild.
            guildRoles (GuildRoles): Guild json connector.
        """
        for r in guildRoles.getGuildRoles():
            await guild.create_role(name=r, colour=Colour.from_str(guildRoles.getGuildRoles()[r]["colour"]), reason="SYS INITIAL ROLE")
        
        for r in guildRoles.getGuildRoles():          
            role_id = str(utils.get(guild.roles, name=r).id)
            
            guildRoles.editRole(name=r, category="role_id", newVal=role_id)
            guildRoles.editRole(name=r, category="custom_id", newVal=str(guild.id) + str(role_id))
    
    
    async def createRoleTextChannel(self, guild: Guild):
        
        # To delete the role channel, I have to keep track of the channel ID, pref in a json.
        
        overwrites = {
        guild.default_role: PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=False, use_application_commands=False, send_voice_messages=False, mention_everyone=False),
        guild.me: PermissionOverwrite(read_messages=True)
        }

        return await guild.create_text_channel(name='choose-your-role', overwrites=overwrites)
        
    
    @app_commands.command(name="remove-all-roles", description="REMOVES ALL ROLES SYSTEM BOT RELATED ROLES")
    @app_commands.default_permissions(administrator=True)
    async def removeallroles(self, interaction: Interaction):
        
        await self.removeRoles(interaction=interaction)
        
        await interaction.response.send_message("Deleted all System related roles.")
        
        
    
    async def removeRoles(self, interaction: Interaction):
        
        roles = interaction.guild.roles
        guildrole = GuildRoles(interaction.guild)
                
        for r in roles:
            
            if r != interaction.guild.default_role and not r.permissions.administrator:
                try:
                    if (r.id == int(guildrole.getGuildRoles()[r.name]['role_id'])):
                        await r.delete()
                except KeyError:
                    pass
            
            
    @app_commands.command(name="remove-system", description="REMOVES ALL ROLES")
    @app_commands.default_permissions(administrator=True)
    async def forceremove(self, interaction: Interaction):
        
        await self.removeRoles(interaction)
        
        guild = interaction.guild
        
        roleChannel = utils.get(guild.channels, name="choose-your-role")
        
           # if the channel exists
        if roleChannel is not None:
            await roleChannel.delete()
        # if the channel does not exist, inform the user
        else:
            await interaction.response.send_message(f'No channel named, choose-your-role, was found')
            
        await interaction.response.send_message("Complete removal of System from server completed.")



async def setup(bot: commands.Bot):
    await bot.add_cog(Role())
    
    guilds = bot.guilds
    
    for g in guilds:
        gd = GuildDatabase(g)
        gr = GuildRoles(g)
        if gr.__status__():
            bot.add_view(RoleView(g))
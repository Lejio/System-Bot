from discord.ui import Button
from discord import Guild, ButtonStyle, Interaction, app_commands
from discord.ui import View
from discord.ext import commands

from roleEnum import GAMINGROLE, COLORS
from roleDbConnector import RoleDatabase


class RoleButton(Button):
    
    def __init__(self, role_id: int, guild: Guild, emoji: str = None):
        
        
        super().__init__(style=ButtonStyle.secondary, emoji=emoji)
        self.label = guild.get_role(role_id)
        self.role = guild.get_role(role_id)
        self.role_id = role_id
        self.guild = guild
        
        
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
    async def buttonTest(self, interaction: Interaction):
        """
        Button testing command. Sys bot displays one button. Upon user clicking on the button, the bot responds with a message.

        Args:
            interaction (discord.Interaction): Discord interaction object. Any "interaction" with commands are discord interactions.
        """

        # Creates a Discord View object.
        testView = View()
        
        # Creates a button.
        testButton = RoleButton(925962416272052275, interaction.guild, "<:emoji_39:935315265468633148>")
        
        # Connects the created callback function to the testButton.
        # testButton.callback = callBackTest
        
        # Adds the button to the view.
        testView.add_item(testButton)
        
        # Sends view as interaction.
        await interaction.response.send_message(view=testView)
    


    
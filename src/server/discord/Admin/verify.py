from discord import PermissionOverwrite, Embed, ButtonStyle, Interaction, utils, Member, Guild
from discord.ui import View, Button

from Roles.guildroles import GuildRoles

class ConfirmButton(Button):
    
    def __init__(self, member: Member) -> None:
        super().__init__()
        
        self.member = member
        
    async def callback(self, interaction: Interaction):
        
        gr = GuildRoles(interaction.guild)
        
        verified_role = interaction.guild.get_role(role_id=gr.getGuildProperties()["default_role_verified_id"])
        
        await self.member.add_roles(verified_role)
        

class ConfirmView(View):
    
    def __init__(self, member: Member):
        super().__init__(timeout=None)
        
        self.add_item(ConfirmButton(member=member))


class VerifyButton(Button):
    
    def __init__(self, guild: Guild) -> None:
        super().__init__(style=ButtonStyle.primary, emoji="<:emoji_39:935315265468633148>", label="Bruh")

        self.custom_id = str(guild.id) + str(guild.name)
        
    async def callback(self, interaction: Interaction):
        
        verify_channel = utils.get(interaction.guild.channels, name="verification-requests")
        
        # confirm_view = ConfirmView(interaction.user)
        # confirm_embed = Embed(title=f"{interaction.user.name} is requesting for verification", description=f"Click on the button below to grant {interaction.user.name} access to the server.")
        # await verify_channel.send(embed=confirm_embed, view=confirm_view)
        await verify_channel.send("Hello")
        # await interaction.response.send_message("Test")


class VerifyView(View):
    
    def __init__(self, guild: Guild):
        super().__init__(timeout=None)
        
        vb = VerifyButton(guild)
        
        self.add_item(vb)

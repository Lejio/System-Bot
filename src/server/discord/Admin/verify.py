from discord import PermissionOverwrite, Embed, ButtonStyle, Interaction, utils, Member, Guild
from discord.ui import View, Button

from Roles.guildroles import GuildRoles

class ConfirmButton(Button):
    
    def __init__(self, member: Member) -> None:
        super().__init__(style=ButtonStyle.primary, emoji="<:check_blue:1125608256153337987>")
        
        self.member = member
        
    async def callback(self, interaction: Interaction):
        
        gr = GuildRoles(interaction.guild)
        # print(gr.getGuildProperties())
        roleid = int(gr.getGuildProperties()["default_role_verified_id"])
        verified_role = interaction.guild.get_role(roleid)
        unverified_role = interaction.guild.get_role(int(gr.getGuildProperties()["default_role_unverified_id"]))
        # print(verified_role.name, verified_role.id)
        approve_embed = Embed(title=f"{self.member} has been approved!", description="Go ahead and welcome them into the family")
        await interaction.response.send_message(embed=approve_embed)
        
        await self.member.add_roles(verified_role)
        await self.member.remove_roles(unverified_role)
        

class ConfirmView(View):
    
    def __init__(self, member: Member):
        super().__init__(timeout=None)
        
        self.add_item(ConfirmButton(member=member))


class VerifyButton(Button):
    
    def __init__(self, guild: Guild) -> None:
        super().__init__(style=ButtonStyle.primary, emoji="<:check_green:1125605364340097044>")

        self.custom_id = str(guild.id) + str(guild.name)
        
    async def callback(self, interaction: Interaction):
        
        verify_channel = utils.get(interaction.guild.channels, name="verification-requests")
        confirm_view = ConfirmView(interaction.user)
        confirm_embed = Embed(title=f"{interaction.user.name} is requesting for verification", description=f"Click on the button below to grant {interaction.user.name} access to the server.")
        await verify_channel.send(embed=confirm_embed, view=confirm_view)
        
        sent_embed = Embed(title="Request Sent", description="Please wait patiently while someone approves your request.")
        await interaction.response.send_message(embed=sent_embed, ephemeral=True)


class VerifyView(View):
    
    def __init__(self, guild: Guild):
        super().__init__(timeout=None)
        
        vb = VerifyButton(guild)
        
        self.add_item(vb)

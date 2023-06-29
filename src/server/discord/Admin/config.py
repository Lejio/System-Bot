from discord import app_commands, Interaction, Embed, Colour
from discord.ext import commands

from Admin.serverconfig import ServerConfig
from sysenum import REG_COLORS, DARK_COLORS, LIGHT_COLORS

@app_commands.default_permissions(administrator=True)
class Config(commands.GroupCog):
    
    def __init__(self, client: commands.Bot) -> None:
        super().__init__()
        
        self.client = client
        
    
    @app_commands.command(name="administration", description="Displays server administration settings")
    async def viewAdmin(self, interaction: Interaction):
        
        serverconf = ServerConfig(interaction.guild)

        
        embed = Embed(title="Admin Configuration", colour=Colour.from_str(serverconf.__getsystemconfig__()["embed_color"]))
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1118363465103458366/1123752160295927859/Screen_Shot_2023-06-27_at_3.55-PhotoRoom.png")
                
        embed.add_field(name="Command Category", value=serverconf.__getadminconfig__()["cmd_category_name"], inline=True)
        embed.add_field(name="Command Text Channel", value=serverconf.__getadminconfig__()["server_command_name"], inline=True)
        embed.add_field(name="System Bot News", value=serverconf.__getadminconfig__()["server_bot_news"], inline=True)
        embed.add_field(name="Admin Channel", value=serverconf.__getadminconfig__()["server_admin_channel"], inline=True)
        
        embed.add_field(name="Welcome Category", value=serverconf.__getservergate__()["welcome_category_name"], inline=True)
        embed.add_field(name="Unverified Channel", value=serverconf.__getservergate__()["unverified_channel_name"], inline=True)
        embed.add_field(name="Unverified Text", value=serverconf.__getservergate__()["unverified_channel_text"], inline=True)
        embed.add_field(name="Verified Channel", value=serverconf.__getservergate__()["verified_channel_name"], inline=True)
        embed.add_field(name="Verified Text", value=serverconf.__getservergate__()["verified_channel_text"], inline=True)
        embed.add_field(name="Role Text", value=serverconf.__getroleconfig__()["text"], inline=True)
        embed.add_field(name="Embed Color", value=serverconf.__getsystemconfig__()["embed_color"], inline=True)
        
        await interaction.response.send_message(embed=embed)
        
    
    @app_commands.command(name="embed-color", description="Changes the default embed color for your server.")
    @app_commands.describe(dark_color="Dark color selector", light_color="Light color selector", reg_color="Default colors")
    @app_commands.choices(dark_color=[app_commands.Choice(name=color.name, value=color.value) for color in DARK_COLORS],
                          light_color=[app_commands.Choice(name=color.name, value=color.value) for color in LIGHT_COLORS],
                          reg_color=[app_commands.Choice(name=color.name, value=color.value) for color in REG_COLORS])
    async def changeEmbedColor(self, interaction: Interaction, reg_color: app_commands.Choice[int]=None, light_color: app_commands.Choice[int]=None, dark_color: app_commands.Choice[int]=None):
        
        if ([reg_color, dark_color, light_color].count(None) < 2):
            await interaction.response.send_message("You can only choose one color!")
        
        else:
            
            serverconf = ServerConfig(interaction.guild)
            
            if reg_color != None:
                serverconf.editSystemConfig(category="embed_color", new_value=Colour(reg_color.value))

                await interaction.response.send_message(f"Changed embed color to {reg_color.name}")
                
            elif light_color != None:
                serverconf.editSystemConfig(category="embed_color", new_value=Colour(light_color.value))
                await interaction.response.send_message(f"Changed embed color to {light_color.name}")
                
            elif dark_color != None:
                serverconf.editSystemConfig(category="embed_color", new_value=Colour(dark_color.value))
                await interaction.response.send_message(f"Changed embed color to {dark_color.name}")
                
            else:
                await interaction.response.send_message("You need to choose a color!") 
        

        
        
async def setup(bot: commands.Bot):
    await bot.add_cog(Config(bot))
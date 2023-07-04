from discord import CategoryChannel,  Embed

from Admin.serverconfig import ServerConfig

class Initialize:
    
    def __init__(self, category: CategoryChannel) -> None:
        
        self.category = category

        
    async def setups(self):
        
        servconf = ServerConfig(self.category.guild)
        servconf = servconf.__getadminconfig__()
        
        await self.__createTextChannel(self.category, "verification-requests")
        
        cmd_channel = await self.__createTextChannel(self.category, servconf["server_command_name"])
        cmd_channel_embed = Embed(title=f"Greetings people of {self.category.guild.name}!", description="Thank you for choosing System bot to be the solution for all of your moderation needs! Here are some quick steps to get the bot setup.")
        await cmd_channel.send(embed=cmd_channel_embed)
        
        news_channel = await self.__createTextChannel(self.category, servconf["server_bot_news"])
        news_channel_embed = Embed(title="Future Updates", description="This channel would send updates to inform you of any maintenance, and any up and coming updates!")
        await news_channel.send(embed=news_channel_embed)
        
        admin_channel = await self.__createTextChannel(self.category, servconf["server_admin_channel"])
        admin_channel_embed = Embed(title="Command Center", description="This is where you can freely use commands without alerting your fellow members! Feel free to send me orders from here!")
        await admin_channel.send(embed=admin_channel_embed)
        
        await self.__createVoiceChannel(self.category, servconf["server_admin_vc"])
    
    
    async def __createTextChannel(self, category: CategoryChannel, channel_name: str):
        
        return await category.create_text_channel(name=channel_name)
        
    
    async def __createVoiceChannel(self, category: CategoryChannel, channel_name: str):
        
        return await category.create_voice_channel(name=channel_name)
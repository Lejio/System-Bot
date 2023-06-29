from typing import Optional
from discord import PermissionOverwrite, Embed, Button, ButtonStyle, Interaction
from discord.types.components import ButtonComponent as ButtonComponentPayload
from discord.ui import View


class VerifyButton(Button):
    
    def __init__(self) -> None:
        super().__init__()
        self.label = "Y"
        
    async def callback(self, interaction: Interaction):
        
        pass

class VerifyView(View):
    
    def __init__(self):
        super().__init__(timeout=None)
        
    
    async def setup(self):
        
        vb = VerifyButton()
        
        self.add_item(vb)
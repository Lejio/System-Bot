from enum import Enum

class Game:
    
    def __init__(self, name: str, role_id: int) -> None:
        
        self.name = name
        self.role_id = role_id
        

class SocialStatus():
    
    def __init__(self, name: str, role_id: int) -> None:
        
        self.name = name
        self.role_id = role_id
        
class ROLE(Enum):
    
    Executive = 6483368039460631


class GAMINGROLE(Enum):
    
    COC = Game("Clash of Clans", 0)
    LOL = Game("League of Legends", 0)
    CSGO = Game("Counter Strike: Global Offensive", 0)
    OW = Game("Overwatch", 0)
    MC = Game("Minecraft", 0)
    
    
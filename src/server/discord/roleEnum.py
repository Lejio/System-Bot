from enum import Enum
from discord.colour import Colour
        

class SocialStatus():
    
    def __init__(self, name: str, role_id: int) -> None:
        
        self.name = name
        self.role_id = role_id
        
class REG_COLORS(Enum):
    
    BLUE = Colour.blue().value
    BLURPLE = Colour.blurple().value
    DEFAULT = Colour.default().value
    FUCHSIA = Colour.fuchsia().value
    GOLD = Colour.gold().value
    GREEN = Colour.green().value
    BRAND_GREEN = Colour.brand_green().value
    BRAND_RED = Colour.brand_red().value
    MAGENTA = Colour.magenta().value
    OG_BLURPLE = Colour.og_blurple().value
    ORANGE = Colour.orange().value
    PURPLE = Colour.purple().value
    RED = Colour.red().value
    TEAL = Colour.teal().value
    
    RANDOM = Colour.random().value
    
    
class DARK_COLORS(Enum):
    
    DARK_BLUE = Colour.dark_blue().value
    DARK_EMBED = Colour.dark_embed().value
    DARK_GOLD = Colour.dark_gold().value
    DARK_GRAY = Colour.dark_gray().value
    DARK_GREEN = Colour.dark_green().value
    DARK_GREY = Colour.dark_grey().value
    DARK_MAGENTA = Colour.dark_magenta().value
    DARK_ORANGE = Colour.dark_orange().value
    DARK_PURPLE = Colour.dark_purple().value
    DARK_RED = Colour.dark_red().value
    DARK_TEAL = Colour.dark_teal().value
    
    
class LIGHT_COLORS(Enum):
    
    LIGHT_EMBED = Colour.light_embed().value
    LIGHT_GRAY = Colour.light_gray().value
    LIGHTER_GRAY = Colour.lighter_gray().value
    LIGHT_GREY = Colour.light_grey().value
    LIGHTER_GREY = Colour.lighter_grey().value
    


        
class ROLE(Enum):
    
    Executive = 6483368039460631

    
    
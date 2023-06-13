
# https://bulbapedia.bulbagarden.net/wiki/Experience#Experience_at_each_level

# Database with all types of XP noted down already.

class level:
    
    def __init__(self, level: int = 0, xp: int = 0) -> None:
        
        self.__level = level
        self.__xp = xp
        self.__max = self.__level
        
    
    def increase(inc: int):
        
        pass
        
    
    @getattr
    def getLevel(self):
        
        return self.__level
    
    
    @getattr
    def getXp(self):
        
        return self.__xp
        
        
    
    
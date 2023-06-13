from level import level
from pokemonMoves import moves
'''
    Pokemon Class: A pokemon object that contains all the information about a pokemon.
    All pokemon information is obtained from sraping websites.
'''


class Pokemon:
    
    def __init__(self, name: str, num: int, level: level, moves: moves) -> None:
        """
        _summary_: A Pokemon object.
        """
        
        self.name = name
        self.num = num
        self.level = level
        self.moves = moves
    
    
    def __str__(self) -> str:
        
        return self.name
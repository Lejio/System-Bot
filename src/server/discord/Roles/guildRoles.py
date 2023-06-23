import json
from os import path

from discord import Guild, Colour

"""
    Incomplete. next step is to generate server profiles.
    Assume at initialization, no guildRoles json file will be present.
    Have json init generate new role json for server.
    
"""
class GuildRoles:
    """Manages the roles of a given guild.
    """
    
    
    def __init__(self, guild: Guild) -> None:
        """Manages and stores the roles of a given guild. Must have guild profile already setup. Stores guild information in roles.json in the guild profile. Creates a role database if one is not exist in a exisiting guild profile. Default roles will be implemented.

        Args:
            guild (Guild): Guild that needed to be edited.

        Raises:
            Exception: Guild default template not found (file missing).
        """
        
        self.DATABASE_NAME = str(guild.id)
        self.DEFAULT_TEMPLATE_PATH = "Roles/default.json"
        self.DATABASE_PATH = f"../database/{self.DATABASE_NAME}/roles.json"
        
        # Checks for the existance of default.json file.
        if path.isfile(self.DEFAULT_TEMPLATE_PATH) is False:
            raise Exception("File not found")
        
        # Attempts to open guild roles.json.
        try:
            with open(self.DATABASE_PATH) as fp:
                self.__guildroles = json.load(fp)
        # Throws exception when guild profile not found.
        except FileNotFoundError:
            raise Exception("Guild profile does not exist.")
        
        # Checks if the size of the guild profile is zero. If it is, create a default guild role profile.
        if self.__sizeof__() == 0:
            self.__initRoles()
    
    
    def __initRoles(self) -> None:
        """Role profile initializer. Must have guild profile setup already before initializing GuildRoles.

        Raises:
            Exception: If file is not found, throws an exception.
        """
        
        if path.isfile(self.DEFAULT_TEMPLATE_PATH) is False:
            raise Exception("File not found")
        

        with open(self.DEFAULT_TEMPLATE_PATH) as fp:
            self.__roleObj = json.load(fp)
            
        self.__guildroles = self.__roleObj
        
        with open(self.DATABASE_PATH , 'w') as json_file:
            json.dump(self.__guildroles, json_file, indent=2, separators=(',',': '))
            
    
    def createRole(self, name: str, role_id: int = None,emoji_id: str = None,  colour: str = Colour.random()) -> None:
        """Creates a role. Default none-types must be checked.

        Args:
            name (str): Name of the role.
            role_id (int, optional): Role id that is connected to discord.Role. Defaults to None.
            custom_id (str, optional): Custom id that needs to be set in order for persistent buttons.
            emoji_id (str, optional): Emoji that is related to the role. Defaults to None.
            colour (str, optional): The color of the role. Gives random color if none is given. Defaults to Colour.random().
        """
        
        self.__guildroles['roles'][name] = {'role_id': role_id, "emoji_id": emoji_id, "custom_id": self.DATABASE_NAME + role_id, 'colour': colour}
        
        with open(self.DEFAULT_TEMPLATE_PATH, 'w') as json_file:
            json.dump(self.__guildroles, json_file, indent=2, separators=(',',': '))
            
    
    def removeRole(self, name: str) -> True:
        """Removes a role. Always returns true. There are no checks. Exceptions could be thrown when retrieving roles if not handled correctly.

        Args:
            name (str): Role name.
        """
        del self.__guildroles['roles'][name]
        
        with open(self.DATABASE_PATH , 'w') as json_file:
            json.dump(self.__guildroles, json_file, indent=2, separators=(',',': '))
            
        return True
            
            
    def editRole(self, name: str, category: str, newVal) -> None:
        """Edit existing role_id or emoji_id values of a exisiting role.

        Args:
            name (str): Name of role.
            category (str): role_id or emoji_id.
            newVal (_type_): New value you wish to input. No checks on correct values performed.

        Raises:
            Exception: If category other than role_id/emoji_id/colour is inputted, exception is raised.
        """
        if not (["role_id", "custom_id", "emoji_id", "colour"].__contains__(category)):
            
            raise Exception("Category not supported.")
            
        self.__guildroles['roles'][name][category] = newVal
        
        with open(self.DATABASE_PATH , 'w') as json_file:
            json.dump(self.__guildroles, json_file, indent=2, separators=(',',': '))
            
    
    def getGuildRoles(self) -> dict:
        """Returns the guild roles as a two dimensional dictionary.

        Returns:
            dict: Current roles and its properties.
        """
        
        return self.__guildroles["roles"]


    def __status__(self) -> bool:
        
        return self.__guildroles['properties']['initialized']
    
    
    def __changestatus__(self) -> None:
        
        self.__guildroles['properties']['initialized'] = not self.__guildroles['properties']['initialized']

        with open(self.DATABASE_PATH , 'w') as json_file:
            json.dump(self.__guildroles, json_file, indent=2, separators=(',',': '))
    
    def __sizeof__(self) -> int:
        return len(self.__guildroles)
    
    
    def __str__(self) -> str:
        return str(self.__guildroles)


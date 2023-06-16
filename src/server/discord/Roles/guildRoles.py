import json
from os import path
from typing import Any

"""
    Incomplete. next step is to generate server profiles.
    Assume at initialization, no guildRoles json file will be present.
    Have json init generate new role json for server.
    
"""
class GuildRoles:
    
    def __init__(self) -> None:
        
        if path.isfile("Roles/guildRoles.json") is False:
            raise Exception("File not found")
        
        with open("Roles/guildRoles.json") as fp:
            self.__guildroles = json.load(fp)
        
        
        if self.__sizeof__() == 0:
            self.initRoles()
    
    
    def initRoles(self):
        
        if path.isfile("Roles/default.json") is False:
            raise Exception("File not found")
        

        with open("Roles/default.json") as fp:
            self.__roleObj = json.load(fp)
        
        
        self.__guildroles = self.__roleObj
        
        with open("Roles/guildRoles.json", 'w') as json_file:
            json.dump(self.__guildroles, json_file, indent=2, separators=(',',': '))
            
    
    def createRole(self, name: str, role_id: int = None, emoji_id: str = None) -> None:
        
        self.__guildroles[name] = {'role_id': role_id, "emoji_id": emoji_id}
        
        with open("Roles/guildRoles.json", 'w') as json_file:
            json.dump(self.__guildroles, json_file, indent=2, separators=(',',': '))
            
    
    def removeRole(self, name: str):
        
        del self.__guildroles[name]
        
        with open("Roles/guildRoles.json", 'w') as json_file:
            json.dump(self.__guildroles, json_file, indent=2, separators=(',',': '))
            
            
    def editRole(self, name: str, category: str, newVal):
        """Edit existing role_id or emoji_id values of a exisiting role.

        Args:
            name (str): Name of role.
            category (str): role_id or emoji_id.
            newVal (_type_): New value you wish to input.

        Raises:
            Exception: If category other than role_id/emoji_id is inputted, exception is raised.
        """
        if not (["role_id", "emoji_id"].__contains__(category)):
            
            raise Exception("Category not supported.")
            
        self.__guildroles[name][category] = newVal
        
        with open("Roles/guildRoles.json", 'w') as json_file:
            json.dump(self.__guildroles, json_file, indent=2, separators=(',',': '))
            
    
    def getGuildRoles(self):
        
        return self.__guildroles
            
    
    def __sizeof__(self) -> int:
        return len(self.__guildroles)
    
    
    def __str__(self) -> str:
        return str(self.__guildroles)
        
        
    
    
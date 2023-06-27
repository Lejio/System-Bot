from discord import Guild

import json

class ServerConfig:
    
    def __init__(self, guild: Guild) -> None:
        
        self.DEFAULT_CONFIG_NAME = "defaultconfig.json"
        self.ADMIN_CONFIG = "admin_config"
        self.SERVER_CONFIG = "server_config"
        self.SERVER_GATE = "server_gate"
        self.ROLE_CONFIG = "role_config"
        self.SYSTEM_CONFIG = "system_config"
        self.JSON_PATH = f"../database/{str(guild.id)}/roles.json"
        self.INDENT = 4
        
        self.__server_config = {}
        self.__guild = guild.id
        
        try:
            with open(self.JSON_PATH) as fp:
                self.__server_config = json.load(fp)
        # Throws exception when guild profile not found.
        except FileNotFoundError:
            raise Exception("Guild profile does not exist.")
        
        if len(self.__server_config) == 0:
            try:
                with open(self.DEFAULT_CONFIG_NAME) as fp:
                    self.__server_config = json.load(fp)
                    
                with open(self.JSON_PATH , 'w') as json_file:
                    json.dump(self.__server_config, json_file, indent=self.INDENT, separators=(',',': '))
            # Throws exception when guild profile not found.
            except FileNotFoundError:
                raise Exception("Default config does not exist.")
    

    def __getadminconfig__(self) -> dict:
        
        return self.__default_config[self.ADMIN_CONFIG]
    
    
    def editAdminConfig(self, category: str, new_value: str):
        
        self.__edit(config=self.ADMIN_CONFIG, category=category, new_value=new_value)
    
    
    def __getserverconfig__(self) -> dict:
        
        return self.__default_config[self.SERVER_CONFIG]
    
    
    def __getservergate__(self) -> dict:
        
        return self.__getserverconfig__()[self.SERVER_GATE]
    
    
    def editServerGate(self, category: str, new_value: str):
        
        self.__edit(config=self.SERVER_GATE, category=category, new_value=new_value)
    
    
    def __getroleconfig__(self) -> dict:
        
        return self.__getserverconfig__()[self.ROLE_CONFIG]
    
    
    def editRoleConfig(self, category: str, new_value: str):
        
        self.__edit(config=self.ROLE_CONFIG, category=category, new_value=new_value)
            
    
    def __getsystemconfig__(self) -> dict:
        
        return self.__getserverconfig__()[self.SYSTEM_CONFIG]
    
    
    def editSystemConfig(self, category: str, new_value: str):
        
        self.__edit(config=self.SYSTEM_CONFIG, category=category, new_value=new_value)
            
    
    def __edit(self, config, category, new_value):
        
        self.__server_config[config][category] = new_value
        
        with open(self.JSON_PATH , 'w') as json_file:
            json.dump(self.__server_config, json_file, indent=self.INDENT, separators=(',',': '))
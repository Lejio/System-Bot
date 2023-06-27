import os
import sqlite3
import json

from discord import Member, Guild

class GuildDatabase:
    
    
    def __init__(self, guild: Guild = None) -> None:
        
        self.DATABASE_PATH = "../database"
        self.DATABASE_NAME = str(guild.id) + ".db"
        self.DIR_NAME = str(guild.id)
        
        self.ROLE = "role.json"
        self.CONFIG = "config.json"
        
        self.DATABASE_STATUS = self.check_dir()
        
        if not self.DATABASE_STATUS:
            
            print(f"Database {self.DATABASE_PATH}/{self.DIR_NAME} does not exist. Setting up new Database.")
        
            self.database_setup()
            
        else:
            
            self.__conn = sqlite3.connect(f"{self.DATABASE_PATH}/{self.DIR_NAME}/{self.DATABASE_NAME}")
            self.__cursor = self.__conn.cursor()
            print(f"{self.DIR_NAME} Connection Stable.")
            

    
    def check_dir(self) -> bool:
        """Checks if the database id has a file with the same name.

        Returns:
            bool: Database exists or not.
        """

        db_list = os.listdir(self.DATABASE_PATH + "/"
)
        
        for db in db_list:
            
            if str(self.DIR_NAME) in db:

                return True

        return False
    
    
    def database_setup(self):
        
        os.mkdir(self.DATABASE_PATH + "/" + self.DIR_NAME)
        open(f"{self.DATABASE_PATH}/{self.DIR_NAME}/{self.ROLE}", "w")
        open(f"{self.DATABASE_PATH}/{self.DIR_NAME}/{self.CONFIG}", "w")

        with open(self.DATABASE_PATH + "/" + self.DIR_NAME + "/" + self.ROLE, "w") as fp:
            fp.write(json.dumps({}, indent=2))
            
        with open(self.DATABASE_PATH + "/" + self.DIR_NAME + "/" + self.CONFIG, "w") as fp:
            fp.write(json.dumps({}, indent=2))
        
        self.__conn = sqlite3.connect(f"{self.DATABASE_PATH}/{self.DIR_NAME}/{self.DATABASE_NAME}")
        self.__cursor = self.__conn.cursor()
        
        self.__conn.execute('''CREATE TABLE MEMBERS 
        (MEMBER_ID INTEGER NOT NULL,
        DISPLAY_NAME TEXT NOT NULL,
        ROLE_ID INTEGER NOT NULL
        );''')
        

        
    def add_member(self, member: Member) -> bool:
        
        try:
            
            self.__conn.execute(f"INSERT INTO MEMBERS (MEMBER_ID, DISPLAY_NAME, ROLE_ID) VALUES ('{member.id}', '{member.display_name}', '{member.top_role}');")
            self.__conn.commit()
            return True
            
        except Exception as e:
            
            print(member.name)
            print(e)
            return False
        
    
    def get_info_for(self, member: Member):
        
        self.__cursor.execute(f"SELECT * FROM MEMBERS WHERE MEMBER_ID = {member.id}")
        return self.__cursor.fetchone()
    
    
    def deleteDB(self) -> bool:
        
        self.close()
        
        db_list = os.listdir(self.DATABASE_PATH + "/" + self.DIR_NAME)

        for db in db_list:
            os.remove(self.DATABASE_PATH + "/" + self.DIR_NAME + "/" + db)
        
        try:
            print("Removing database..")
            os.rmdir(self.DATABASE_PATH + "/" + self.DIR_NAME)
            print(f"{self.DIR_NAME} Removed.")
            return True
        except Exception as e:
            print(e)
            return False
    
    
    def close(self):
        
        self.__conn.close()
        

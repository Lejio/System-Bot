import os
import sqlite3

from discord import Member, Guild
import discord

class GuildDatabase:
    
    
    def __init__(self, guild: Guild = None) -> None:
        
        self.DATABASE_PATH = "../database"
        self.DATABASE_NAME = guild.id + ".db"
        self.DIR_NAME = guild.id
        self.DATABASE_STATUS = self.check_dir()
        
        if not self.DATABASE_STATUS:
            
            print(f"Database {self.DATABASE_PATH}/{self.DIR_NAME} does not exist. Setting up new Database.")
        
            self.database_setup()
            
        else:
            
            self.conn = sqlite3.connect(f"{self.DATABASE_PATH}/{self.DIR_NAME}/{self.DATABASE_NAME}")
            self.cursor = self.conn.cursor()
            

    
    def check_dir(self):
        """
        Checks if the database id has a file with the same name.
        return:
        True - If the database exists
        False - If the database doesn't exits.
        """

        db_list = os.listdir(self.DATABASE_PATH + "/")
        
        print(db_list)

        for db in db_list:

            if str(self.DIR_NAME) in db:

                return True

        return False
    
    
    def database_setup(self):
        
        os.mkdir(self.DATABASE_PATH + "/" + self.DIR_NAME)
        
        self.conn = sqlite3.connect(f"{self.DATABASE_PATH}/{self.DIR_NAME}/{self.DATABASE_NAME}")
        self.cursor = self.conn.cursor()
        
        self.conn.execute('''CREATE TABLE MEMBERS 
        (MEMBER_ID INTEGER NOT NULL,
        DISPLAY_NAME TEXT NOT NULL,
        ROLE_ID INTEGER NOT NULL
        );''')
        

        
    def add_member(self, member: Member):
        
        try:
            
            self.conn.execute(f"INSERT INTO MEMBERS (MEMBER_ID, DISPLAY_NAME, ROLE_ID) VALUES ('{member.id}', '{member.display_name}', '{member.top_role}');")
            
        except Exception as e:
            
            print(member.name)
            print(e)
        
        self.conn.commit()
        
    
    def get_info_for(self, member: Member):
        
        self.cursor.execute(f"SELECT * FROM MEMBERS WHERE MEMBER_ID = {member.id}")
        return self.cursor.fetchone()
    
    def deleteDB(self) -> bool:
        
        self.close()
        
        db_list = os.listdir(self.DATABASE_PATH + "/" + self.DIR_NAME)

        for db in db_list:
            os.remove(self.DATABASE_PATH + "/" + self.DIR_NAME + "/" + db)
        
        try:
            print("Removing database..")
            os.rmdir(self.DATABASE_PATH + "/" + self.DIR_NAME)
            return True
        except Exception as e:
            print(e)
            return False
    
    
    def close(self):
        
        self.conn.close()
        

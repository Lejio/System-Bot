import os
import sqlite3

from discord import Member

class RoleDatabase:
    
    
    def __init__(self, database_id: str) -> None:
        
        self.DATABASE_PATH = "../database"
        self.DATABASE_NAME = database_id + ".db"
        self.DATABASE_STATUS = self.check_database()
        
        self.conn = sqlite3.connect(f"{self.DATABASE_PATH}/{self.DATABASE_NAME}")
        self.cursor = self.conn.cursor()
        
        if not self.DATABASE_STATUS:
            
            print(f"Database {self.DATABASE_PATH} does not exist. Setting up new Database.")
        
            self.database_setup()

    
    def check_database(self):
        """
        Checks if the database id has a file with the same name.
        return:
        True - If the database exists
        False - If the database doesn't exits.
        """

        db_list = os.listdir(self.DATABASE_PATH)
        
        print(db_list)

        for db in db_list:

            if str(self.DATABASE_NAME) in db:

                return True

        return False
    
    
    def database_setup(self):
        
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
    
    
    def close(self):
        
        self.conn.close()
import os
import sqlite3


class database:

  def __init__(self, database_id, members=None):
    """
    Constructor.
    Creates connection with the specified database id.
    If that database does not exist, create a new database (this would require the members parameter to be filled out).
    :param: database_id - The database id for that specific discord. Is unique for each server.
    :param: members=None - Only put when bot is joining new server. This is needed to add all current members of that server
    to the database.
    """

    self.MEMBERS = members
    self.DATABASE_PATH = "databases"
    self.DATABASE_NAME = database_id
    self.DATABASE_STATUS = self.check_database()

    self.conn = sqlite3.connect(f"{self.DATABASE_PATH}/{self.DATABASE_NAME}.db")
    self.cursor = self.conn.cursor()

    if not self.DATABASE_STATUS:  # If fails database check (meaning database does not already exist). Create these tables.
      print(f"Database {self.DATABASE_NAME} does not exist. Setting up new Database.")
      self.database_setup()
      print("Setting up Members.")
      self.add_all_members()  # Adds all the users into the new database.

  
  def add_all_members(self):
    """
    Adds all members into the database and adds it with default values.
    """

    for member in self.MEMBERS:

      self.add_user(int(member), 0, 1000, ":video_game:")


  def database_setup(self):
    """
    Creates these two default tables.
    """

    self.conn.execute('''CREATE TABLE USERS
         (ID INT PRIMARY KEY     NOT NULL,
         LEVEL            INT     NOT NULL,
         BANGERS        INT,
         BADGE       TEXT
         );''')

    self.conn.execute('''CREATE TABLE ROULETTE
         (RUN INTEGER PRIMARY KEY AUTOINCREMENT,
         COLOR           TEXT    NOT NULL,
         NUMBER          INT NOT NULL
         );''')

  
  def check_database(self):
    """
    Checks if the database id has a file with the same name.
    return:
    True - If the database exists
    False - If the database doesn't exits.
    """

    db_list = os.listdir(self.DATABASE_PATH)

    for db in db_list:

      if str(self.DATABASE_NAME) in db:

        return True

    return False

  
  def add_user(self, id, level, bangers, badge):
    """
    Creates a new user with these parameters as entries.
    :param: id - The user's discord id.
    :param: level - The user's default level
    :param: bangers - The user's default currency amount
    :param: bagde - The user's default badge
    """

    self.conn.execute(
      f"INSERT INTO USERS (ID, LEVEL, BANGERS, BADGE) VALUES ('{id}', '{level}', '{bangers}', '{badge}' )"
    )

    self.conn.commit()  # Commits the changes.

  
  def change_bangers(self, bangers, id):
    """
    Updates the currency amount. To subtract, just insert a negative currency amount.
    :param: bangers - The amount of currency you want to change.
    :param: id - The id of the user.
    """

    records = self.get_user(id)

    new_bangers = int(records[2]) + int(bangers)

    self.conn.execute(
      f"UPDATE USERS set BANGERS = '{new_bangers}' where ID = '{id}'")
    self.conn.commit()
    

  def get_user(self, id):
    """
    Retrieves the user information.
    :param: id - The user's id whom you want to retrieve information for.
    :return: records - A list of these five elements [name, nickname, level, bangers, badge]
    """

    sql_select_query = f"SELECT * FROM USERS WHERE ID = '{id}'"
    self.cursor.execute(sql_select_query)
    records = self.cursor.fetchone()

    return records

  
  def get_user_bangers(self, id):
    """
    Gets the user's currency.
    :param: id - The user id.
    :return: The user's bangers amount.
    """

    return self.get_user(id)[3]


  def add_query_roulette(self, color, number):

    self.conn.execute(
      f"INSERT INTO ROULETTE (COLOR, NUMBER) VALUES ('{color}', '{number}')")

    self.conn.commit()

  def last_results(self, num):

    self.cursor.execute(f"SELECT * FROM ROULETTE WHERE RUN > (SELECT COUNT(*) FROM ROULETTE) - {str(num)}")
    records = self.cursor.fetchall()
    return records

    
  def close(self):

    self.conn.close()

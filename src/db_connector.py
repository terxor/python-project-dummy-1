import mysql.connector, sys

def perror(s):
  print("ERROR: " + s)
  sys.exit(1)

class DBConnector:
  def __init__(self):
    # Constants
    host = "localhost"
    user = "root"
    password = ""
    dbname = "PASSMGR"
    
    try:
      tmp = mysql.connector.connect(
        host=host,
        user=user,
        password=password
      )
      cursor = tmp.cursor()
      cursor.execute("CREATE DATABASE IF NOT EXISTS " + dbname)
    except:
      perror("Could not establish connection")
    
    # Connect to db now
    try:
      self.conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        db=dbname
      )
      if not self.conn.is_connected(): raise Exception
    except:
      perror("Could not connect to database")

    try:
      cursor = self.conn.cursor()
      cursor.execute("CREATE TABLE IF NOT EXISTS `masterpass` (`value` VARCHAR(50) NOT NULL)")
      query = "CREATE TABLE IF NOT EXISTS `passwords` ("
      query += "`id` INTEGER PRIMARY KEY AUTO_INCREMENT" + ","
      query += "`name` VARCHAR(50) NOT NULL" + ","
      query += "`userid` VARCHAR(50) NOT NULL" + ","
      query += "`password` VARCHAR(50) NOT NULL" + ")"
      cursor.execute(query)
    except:
      perror("Some error")

    print("Database is OK")

  def is_initialized(self):
    cursor = self.conn.cursor()
    cursor.execute("SELECT count(*) FROM masterpass")
    return (cursor.fetchone()[0] == 1)

  def initialize(self, password):
    # Initialize with master password
    assert not self.is_initialized()
    cursor = self.conn.cursor()
    cursor.execute("INSERT INTO masterpass (value) VALUES (%s)", (password,))
    self.conn.commit()
 
  def is_correct_password(self, password):
    assert self.is_initialized()
    cursor = self.conn.cursor()
    cursor.execute("SELECT * FROM masterpass")
    return (password == cursor.fetchone()[0])

  def add_entry(self, name, userid, password):
    cursor = self.conn.cursor()
    cursor.execute("INSERT INTO passwords (name,userid,password) VALUES (%s,%s,%s)", (name,userid,password))
    self.conn.commit()

  def remove_entry(self, index):
    cursor = self.conn.cursor()
    cursor.execute("DELETE FROM passwords WHERE id = %s", (index,))
    self.conn.commit()

  def get_entries(self):
    cursor = self.conn.cursor()
    cursor.execute("SELECT * FROM passwords")
    rows = cursor.fetchall()
    return rows

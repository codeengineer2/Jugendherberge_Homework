import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.files
from anvil.files import data_files
import anvil.server
import sqlite3

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
@anvil.server.callable
def say_hello(name):
  print("Hello, " + name + "!")
  return 42


@anvil.server.callable
def get_jugendherbergen(rows="x"):
  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
  cursor = conn.cursor()
  res = list(cursor.execute("SELECT name,JID FROM jugendherbergen"))
  print(res)
  return res
@anvil.server.callable
def get_rooms(rows="x"):
  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
  cursor = conn.cursor()
  res = list(cursor.execute("SELECT zimmernummer, bettenanzahl, preis_pro_nacht, gebucht, JID, ZID FROM zimmer"))
  print(res)
  return res
  
@anvil.server.callable
def get_user(rows="x"):
  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
  cursor = conn.cursor()
  res = list(cursor.execute("SELECT GID,PID FROM gast"))
  print(res)
  return res
  
@anvil.server.callable
def get_preiskat(rows="x"):
  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
  cursor = conn.cursor()
  res = list(cursor.execute("SELECT PID,name,price FROM preiskategorie"))
  print(res)
  return res
  
  




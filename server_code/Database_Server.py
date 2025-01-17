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
  
@anvil.server.callable
def write_booking(daten_liste):
    conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
    cursor = conn.cursor()
    
    GID = daten_liste[0]
    ZID = daten_liste[1]
    startdatum = daten_liste[2]
    enddatum = daten_liste[3]
    
    try:
        cursor.execute("INSERT INTO bucht (GID, ZID, startdatum, enddatum) VALUES (?, ?, ?, ?)", (GID, ZID, startdatum, enddatum))
        cursor.execute(f"UPDATE zimmer SET gebucht=1 WHERE zimmernummer = {ZID}")
        conn.commit()
        print("Insertion successful")
    except Exception as e:
        print("Error during insertion:", e)
    finally:
        conn.close()

@anvil.server.callable
def get_booking(row="x"):
    conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
    cursor = conn.cursor()
    res = list(cursor.execute("SELECT BID, GID, ZID, startdatum, enddatum FROM bucht"))
    conn.close()
    print("Booking data retrieved:", res)
    return res
  

@anvil.server.callable
def write_bookingothers(guestlistdatas):
    global counterguestadd  # Declare counterguestadd as global to modify it within the function
    conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
    cursor = conn.cursor()
    
    try:
        res = cursor.execute("SELECT MAX(BID) FROM bucht").fetchone()
        if res is not None and res[0] is not None:
          res = int(res[0])
        else:
          res = 0
        print(res)
        for i in guestlistdatas:
          
          cursor.execute("INSERT INTO buchmit (BID, GID) VALUES (?, ?)", (res, i))
        
        conn.commit()
        print("Insertion successful")
    except Exception as e:
        print("Error during insertion:", e)
    finally:
        conn.close()

@anvil.server.callable
def get_bookingwithguest(row="x"):
  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
  cursor = conn.cursor()
  res = list(cursor.execute("SELECT BMID, BID, GID FROM buchmit"))
  conn.close()
  print("Booking data retrieved:", res)
  return res
  
  
  
  
  

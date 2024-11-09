from ._anvil_designer import StartseiteTemplate
from anvil import *
import anvil.server
from anvil.tables import app_tables


class Startseite(StartseiteTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.rooms = [
    (zimmernummer, bettenanzahl, preis_pro_nacht, gebucht, JID, ZID)
    for zimmernummer, bettenanzahl, preis_pro_nacht, gebucht, JID, ZID in anvil.server.call("get_rooms")
    ]
    
    # Any code you write here will run before the form opens.
    self.drop_down_1.items = [("Feldkirch", 0), ("Hohenems", 1)]
    print(anvil.server.call("say_hello", "42"))
    self.drop_down_1.items = anvil.server.call("get_jugendherbergen", "name, JID")
# If needed, transform the items for display or store multiple values in a way that's compatible
    self.user = [(GID, PID) for GID, PID in anvil.server.call("get_user")]
    self.get_users()
  def get_users(self):
    users_list = []
    for x in self.user:
      print(self.user)
      users_list.append(f"Gast {x[0]}  -  Preiskategorie: {x[1]}")
    self.drop_down_2.items = users_list

  
  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    matching_rooms = []
    selected_value = self.drop_down_1.selected_value
    for i in self.rooms:
      print(self.rooms)
      if i[4] == selected_value:
        print(i[4])
        matching_rooms.append(f"Zimmernummer:{i[0]}  -  Bettenanzahl: {i[1]}  -  Preis p. Nacht = {i[2]}  -  Gebucht: {i[3]}")
    self.dropdownzimmer.items = matching_rooms
    
    print("Selected Index:", selected_value)
    pass
    


#def users(self):
 #   users_list = []
  #  for x in self.user:
   #   print(self.user)
    #  users_list.append(f"Gast {x[0]}  -  Preiskategorie: {x[1]}")
    #self.drop_down_2.items = users_list
#self.user = [(GID, PID) for GID, PID in anvil.server.call("get_user")]
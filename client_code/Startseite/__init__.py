from ._anvil_designer import StartseiteTemplate
from anvil import *
import anvil.server
from anvil.tables import app_tables


class Startseite(StartseiteTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        
        # Fetch and store room data
        self.rooms = [
            (zimmernummer, bettenanzahl, preis_pro_nacht, gebucht, JID, ZID)
            for zimmernummer, bettenanzahl, preis_pro_nacht, gebucht, JID, ZID in anvil.server.call("get_rooms")
        ]
        
        # Fetch and store pricing categories
        self.preiskat = [(PID, name, price) for PID, name, price in anvil.server.call("get_preiskat")]
        
        # Initialize dropdown items
        self.drop_down_1.items = [("Feldkirch", 0), ("Hohenems", 1)]
        print(anvil.server.call("say_hello", "42"))
        
        # Populate drop_down_1 with items from get_jugendherbergen
        self.drop_down_1.items = anvil.server.call("get_jugendherbergen", "name, JID")
        
        # Fetch and store user data
        self.user = [(GID, PID) for GID, PID in anvil.server.call("get_user")]
        
        # Populate drop_down_2 with user list
        self.get_users()
    
    def get_users(self):
        """Populate drop_down_2 with user data"""
        users_list = []
        
        for x in self.user:
            # Format each user entry
            users_list.append(f"Gast {x[0]} - Preiskategorie: {x[1]}")
        
        # Set drop_down_2 items
        self.drop_down_2.items = users_list
    def drop_down_1_change(self, **event_args):
        """This method is called when an item is selected in drop_down_1"""
        # Store the selected value from drop_down_1 in a class attribute
        self.selected_jugendherberge = self.drop_down_1.selected_value
        print("Selected Jugendherberge JID:", self.selected_jugendherberge)
      
    def drop_down_2_change(self, **event_args):
        """This method is called when an item is selected in drop_down_2"""
        
        matching_rooms = []
        selected_value = self.drop_down_2.selected_value
        
        # Ensure drop_down_1 selected value is available
        if self.selected_jugendherberge is None:
            print("No Jugendherberge selected from drop_down_1")
            return
        
        # Iterate over users and match with selected_value
        for i in self.user:
            if selected_value == f"Gast {i[0]} - Preiskategorie: {i[1]}":  # Match with formatted text
                PID = i[1]  # Extract PID for further matching
                
                # Find matching price category
                for x in self.preiskat:
                    if PID == x[0]:  # Match PID with PID in preiskat
                        price = x[2]  # Extract price for matching rooms
                        
                        # Find rooms with matching price and jugendherberge (JID)
                        for y in self.rooms:
                            if y[2] == price and y[4] == self.selected_jugendherberge:  # Check if room price and JID match
                                # Append formatted room information
                                matching_rooms.append(f"Zimmernummer: {y[0]} - Bettenanzahl: {y[1]} - Preis p. Nacht = {y[2]} - Gebucht: {y[3]}")
                  
        # Set dropdownzimmer items after collecting all matches
        self.dropdownzimmer.items = matching_rooms

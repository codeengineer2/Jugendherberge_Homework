from ._anvil_designer import StartseiteTemplate
from anvil import *
import anvil.server
from anvil.tables import app_tables


class Startseite(StartseiteTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.drop_down_1.items = [("Feldkirch", 0), ("Hohenems", 1)]
    print(anvil.server.call("say_hello", "42"))
    self.drop_down_1.items = anvil.server.call("get_jugendherbergen", "name, JID")
# If needed, transform the items for display or store multiple values in a way that's compatible
    self.dropdownzimmer.items = [(f"Zimmer {zimmernummer} - {bettenanzahl} Betten  - Preis pro Nacht: {preis_pro_nacht} - Verfügbarkeit: {gebucht}", ZID) for zimmernummer, bettenanzahl, preis_pro_nacht, gebucht, JID, ZID in anvil.server.call("get_rooms")]

# Fügt die Daten zur Data Table hinzu
    


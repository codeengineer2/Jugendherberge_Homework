from ._anvil_designer import StartseiteTemplate
from anvil import *
import anvil.server

class Startseite(StartseiteTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.drop_down_1.items = [("Feldkirch", 0), ("Hohenems", 1)]
    print(anvil.server.call("say_hello", "42"))
    self.drop_down_1.items = anvil.server.call("get_jugendherbergen", "name, JID")

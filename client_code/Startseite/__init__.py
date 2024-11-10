from ._anvil_designer import StartseiteTemplate
from anvil import *
import anvil.server
from anvil.tables import app_tables
import datetime


class Startseite(StartseiteTemplate):
    def __init__(self, **properties):
      
        self.init_components(**properties)
        
        self.selectedguestlist = []
        self.counterguests = 0
        self.bettenzahl = 0
        self.rooms = [
            (zimmernummer, bettenanzahl, preis_pro_nacht, gebucht, JID, ZID)
            for zimmernummer, bettenanzahl, preis_pro_nacht, gebucht, JID, ZID in anvil.server.call("get_rooms")
        ]
        today = datetime.date.today()
        self.date_picker_start.date = today
        self.date_picker_start.min_date = today 

        self.date_picker_end.date = None
        self.date_picker_end.min_date = today + datetime.timedelta(days=1)


      
       
        self.preiskat = [(PID, name, price) for PID, name, price in anvil.server.call("get_preiskat")]
        
        
        self.drop_down_1.items = [("Feldkirch", 0), ("Hohenems", 1)]
        print(anvil.server.call("say_hello", "42"))
        
       
        self.drop_down_1.items = anvil.server.call("get_jugendherbergen", "name, JID")
        
   
        self.user = [(GID, PID) for GID, PID in anvil.server.call("get_user")]
        
     
        self.get_users()
      
    def get_users(self):
        """Populate drop_down_2 with user data"""
        users_list = []
        user_listadd = []
        for x in self.user:
       
            users_list.append(f"Gast {x[0]} - Preiskategorie: {x[1]}")
            user_listadd.append(f"{x[0]}")
          
        self.drop_down_gastliste.items = user_listadd
        self.drop_down_2.items = users_list
    def drop_down_1_change(self, **event_args):
        """This method is called when an item is selected in drop_down_1"""
      
        self.selected_jugendherberge = self.drop_down_1.selected_value
        print("Selected Jugendherberge JID:", self.selected_jugendherberge)
        
    def drop_down_2_change(self, **event_args):
        """This method is called when an item is selected in drop_down_2"""
        
        matching_rooms = []
        selected_value = self.drop_down_2.selected_value
        
 
        if self.selected_jugendherberge is None:
            print("No Jugendherberge selected from drop_down_1")
            return

        for i in self.user:
            if selected_value == f"Gast {i[0]} - Preiskategorie: {i[1]}":  
                PID = i[1]  
                
         
                for x in self.preiskat:
                    if PID == x[0]: 
                        price = x[2]
                        
                
                        for y in self.rooms:
                            if y[2] == price and y[4] == self.selected_jugendherberge and y[3] == 0:  
                                
                              
                                matching_rooms.append(f"Zimmernummer: {y[0]} - Bettenanzahl: {y[1]} - Preis p. Nacht = {y[2]} - Gebucht: {y[3]}")
                  
        self.dropdownzimmer.items = matching_rooms

    def button_1_click(self, **event_args):
      """This method is called when the button is clicked"""
      nutzerid = ""
      zimmerid = ""
      self.selected_jugendherberge = self.drop_down_1.selected_value
      selected_value_user = self.drop_down_2.selected_value
      selected_value_zimmer = self.dropdownzimmer.selected_value
      
      for i in self.user:
          if selected_value_user == f"Gast {i[0]} - Preiskategorie: {i[1]}":
              nutzerid = str(i[0])  
  
      for y in self.rooms:
          if selected_value_zimmer == f"Zimmernummer: {y[0]} - Bettenanzahl: {y[1]} - Preis p. Nacht = {y[2]} - Gebucht: {y[3]}":
              zimmerid = str(y[0])
              
      
      selected_datestart = self.date_picker_start.date
      selected_dateend = self.date_picker_end.date
      
      print("Selected Start Date:", selected_datestart)
      print("Selected End Date:", selected_dateend)         
      print("Nutzerid:", nutzerid)
      print("Zimmerid:", zimmerid)
      
      daten_liste = [nutzerid, zimmerid, selected_datestart, selected_dateend]
      
      try:
          anvil.server.call('write_booking', daten_liste)
          alert("Daten erfolgreich in die Tabelle eingefügt!")
      except Exception as e:
          alert(f"Fehler beim Einfügen der Daten: {e}")

      
      for guest_id in self.selectedguestlist:  
        guestlistdatas = [guest_id]
        try:
            anvil.server.call('write_bookingothers', guestlistdatas)
            print(f"Guest {guest_id} erfolgreich in die Tabelle eingefügt!")
        except Exception as e:
            print(f"Fehler beim Einfügen von Gast {guest_id}: {e}")
     
      self.bookings = [
          (BID, GID, ZID, startdatum, enddatum)
          for BID, GID, ZID, startdatum, enddatum in anvil.server.call("get_booking")
      ]
      
      
      
      self.drop_down_3.items = [
          f"BuchungsID: {reservation[0]} - GästeID: {reservation[1]} - ZimmerID: {reservation[2]} - Anreise: {reservation[3]} - Abreise: {reservation[4]}"
          for reservation in self.bookings
      ]

      #da soll jetzt die Buchungen mit allen hin
      
      self.bookingswithother = [
          (BMID,BID,GID)
          for BMID, BID, GID in anvil.server.call("get_bookingwithguest")
      ]
      self.drop_down_4.items = [f"BuchunngsmitgästeID: {buchung[0]} - BuchungsID: {buchung[1]} - Gast: {buchung[2]}" for buchung in self.bookingswithother]
      self.selectedguestlist = []
      self.counterguests = 0

      self.drop_down_addedguests.items = []
      
              
              
            
            
            
            
            

          
          
          
          
      
      

    def date_picker_start_change(self, **event_args):
      """This method is called when the selected date changes"""
     
      self.date_picker_end.min_date = self.date_picker_start.date + datetime.timedelta(days=1)

    def date_picker_end_change(self, **event_args):
      """This method is called when the selected date changes"""
      if self.date_picker_end.date <= self.date_picker_start.date:
        self.date_picker_end.date = self.date_picker_start.date + datetime.timedelta(days=1)

    def button_2_click(self, **event_args):
      """This method is called when the button is clicked."""
      selectedroom = self.dropdownzimmer.selected_value
      selected_guest = self.drop_down_gastliste.selected_value
      for y in self.rooms:  
          if (selectedroom == f"Zimmernummer: {y[0]} - Bettenanzahl: {y[1]} - Preis p. Nacht = {y[2]} - Gebucht: {y[3]}"):
            self.bettenzahl = y[1]
            print(self.counterguests)
      if (self.counterguests+1 < self.bettenzahl):
        self.counterguests+=1
        self.selectedguestlist.append(selected_guest)
        
      
      print(selected_guest)
      print(self.selectedguestlist)
            
      self.drop_down_addedguests.items = self.selectedguestlist
      
      
      
      
      
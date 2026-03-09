class Kategorie:
    def __init__(self, nummer, name):
        self.nummer = nummer
        self.name = name
    
           
class Raum:
    def __init__(self, raumnummer, raumname):
        self.raumnummer = raumnummer
        self.raumname = raumname
    
            
class Person:
    def __init__(self, email, vorname, nachname):
        self.email = email
        self.vorname = vorname
        self.nachname = nachname
        

class Schueler(Person):
    def __init__(self, klasse, wahl):
        self.klasse = klasse
        self.klasse = wahl
        
       
class Organisator(Person):
   pass
r = Raum("123", "Gruppenraum")

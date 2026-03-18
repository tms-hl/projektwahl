import mysql.connector
from mysql.connector import pooling
from contextlib import contextmanager
    
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

class Projekt:
    def __init__(self):
        self.name = None
        self.beschreibung = None
        self.plaetze_min = None
        self.plaetze_max = None
        self.klasse_min = None
        self.klasse_max = None
        
        self.raum = None
        self.organisatoren = []
        self.mitglieder = []
       
class Organisator(Person):
   pass

class Db:
    def __init__(self, host, user, password, database, pool_size=5):
        # Initialisierung des Verbindungs-Pools
        self.pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name="mypool",
            pool_size=pool_size,
            host=host,
            user=user,
            password=password,
            database=database
        )
    
    @contextmanager
    def get_cursor(self):
        """Erstellt einen Cursor für den Kontext-Manager"""
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            yield cursor
        finally:
            cursor.close()
            conn.close()  # Verbindung zurück in den Pool geben
            
    def get_connection(self):
        """Methode, um eine Verbindung aus dem Pool zu erhalten"""
        return self.pool.get_connection()
    
    def get_project(self, pid):
        
        with self.get_cursor() as cursor:  # Verbindung im 'with'-Block
            query = "SELECT * FROM projekt WHERE pid = %s"
            cursor.execute(query, [pid])
            result = cursor.fetchall()
            if len(result) == 0:
                return None
            else:
                p = Projekt()
                p.name = result[0]['name']
                p.beschreibung = result[0]['beschreibung']
                p.plaetze_min = result[0]['plätze_min']
                p.plaetze_max = result[0]['plätze_max']
                p.klasse_min = result[0]['klasse_min']
                p.klasse_max = result[0]['klasse_max']
                
                # TODO: Raum mit hinzufügen
                # TODO: Orginator(en) hinzufügen
                # TODO: Teilnehmer hinzufügen
                
                return p

    def get_projects(self):
        '''
            Gibt alle Projekte zurück
            
            Author:
            Max, Bendix
        '''
    
    def get_choice(self, uid)
        '''
            Gibt die drei Projekte zurück, die der Benutzer gewählt hat
            
            Author:
            Louis
        '''

    def get_user(self, uid):
        '''
            Gibt den Schüler mit der ID uid zurück
            
            Author:
            Mats
        '''
        pass
    
    def get_rooms(self):
        '''
            Gibt eine Liste mit allen Räumen zurück
            
            Author:
            Louis
        '''
        pass
    
    def add_project(self, p):
        '''
            Erstellt ein neues Projekt
            
            Author:
            Mats, Louis
        '''
        
    def add_choice(self, uid, pid1, pid2, pid3):
        '''
            Erstellt eine neue Wahl
            
            Author:
            Max, Bendix
        '''
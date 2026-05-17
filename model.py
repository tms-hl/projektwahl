import mysql.connector
from mysql.connector import pooling
from contextlib import contextmanager
    
class Raum:
    def __init__(self, raumnummer, raumname):
        self.raumnummer = raumnummer
        self.raumname = raumname
    
            
class Person:
    def __init__(self, uid=None, email=None, vorname=None, nachname=None):
        self.uid = uid
        self.email = email
        self.vorname = vorname
        self.nachname = nachname

class Schueler(Person):
    def __init__(self):
        super().__init__()
        self.klasse = None
        self.stufe = None

class Projekt:
    def __init__(self):
        self.pid = None
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

class Wahl:
    def __init__(self):
        self.user = None
        self.projects = []
        
class Db:
    def __init__(self, host, database, user, password, pool_size=5):
        # Initialisierung des Verbindungs-Pools
        self.pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name=f"mypool_{id(self)}",
            pool_size=pool_size,
            host=host,
            user=user,
            password=password,
            database=database
        )
    
    @contextmanager
    def get_cursor(self):
        """Erstellt einen Cursor für den Kontext-Manager"""
        conn = self.pool.get_connection()  # Direkt aus dem Pool holen
        conn.autocommit = True
        
        try:
            cursor = conn.cursor(dictionary=True)
            try:
                yield cursor
            finally:
                cursor.close()
        finally:
            conn.close()  # Verbindung sicher zurück in den Pool
    
    @contextmanager
    def get_connection(self):
        """Methode, um eine Verbindung aus dem Pool zu erhalten"""
        conn = self.pool.get_connection()
        try:
            yield conn
        except Exception as e:
            conn.rollback()  # Bei Fehler: Transaktion zurückrollen
            raise e
        finally:
            if conn is not None:
                conn.close()
    
    def get_project(self, pid):
        
        with self.get_cursor() as cursor:  # Verbindung im 'with'-Block
            query = "SELECT * FROM projekt WHERE pid = %s"
            cursor.execute(query, [pid])
            result = cursor.fetchall()
            if len(result) == 0:
                return None
            else:
                p = Projekt()
                p.pid = result[0]['pid']
                p.name = result[0]['name']
                p.beschreibung = result[0]['beschreibung']
                p.plaetze_min = result[0]['plätze_min']
                p.plaetze_max = result[0]['plätze_max']
                p.klasse_min = result[0]['klasse_min']
                p.klasse_max = result[0]['klasse_max']
                
                query = "SELECT user.uid, email, lastname, firstname FROM user JOIN leitet ON leitet.uid = user.uid WHERE leitet.pid = %s"
                result = cursor.execute(query, [p.pid])
                p.organisatoren = [
                    Person(
                        row['uid'],
                        row['email'],
                        row['firstname'],
                        row['lastname']
                    ) for row in cursor.fetchall()
                ]
                
                return p

    def get_projects(self, stufe=None):
        '''
            Gibt alle Projekte zurück
            
            Author:
            Max, Bendix
        '''
        with self.get_cursor() as cursor:  # Verbindung im 'with'-Block
            if stufe is None:
                query = "SELECT * FROM projekt"
                cursor.execute(query)
            else:
                query = "SELECT * FROM projekt WHERE %s >= klasse_min AND %s <= klasse_max"
                cursor.execute(query, (stufe, stufe))
            
            projects = []
            for row in cursor.fetchall():
                p = Projekt()
                p.pid = row ['pid']
                p.name = row ['name']
                p.beschreibung = row['beschreibung']
                p.plaetze_min = row['plätze_min']
                p.plaetze_max = row['plätze_max']
                p.klasse_min = row['klasse_min']
                p.klasse_max = row['klasse_max']
                projects.append(p)
                
        return projects
    
    def get_choice(self, uid):
        '''
            Gibt die drei Projekte zurück, die der Benutzer gewählt hat
            
            Author:
            Mats
        '''
        with self.get_cursor() as cursor:  # Verbindung im 'with'-Block
            query = "SELECT * FROM wählt JOIN projekt ON projekt.pid = wählt.pid WHERE uid = %s ORDER BY no"
            cursor.execute(query, [uid])
            projects = []
            for row in cursor.fetchall():
                p = Projekt()
                p.pid = row ['pid']
                p.name = row ['name']
                p.beschreibung = row['beschreibung']
                p.plaetze_min = row['plätze_min']
                p.plaetze_max = row['plätze_max']
                p.klasse_min = row['klasse_min']
                p.klasse_max = row['klasse_max']
                projects.append(p)
                
        return projects

    def has_choice(self, uid):
        with self.get_cursor() as cursor:
            query = "SELECT 1 FROM wählt WHERE uid = %s LIMIT 1"
            cursor.execute(query, [uid])
            return cursor.fetchone() is not None
            
    def get_user(self, uid):
        '''
            Gibt den Schüler mit der ID uid zurück
            
            Author:
            Louis
        '''
        with self.get_cursor() as cursor:
            query = "SELECT * FROM `user` WHERE uid = %s AND active = 1 LIMIT 1"
            cursor.execute(query, [uid])
            result = cursor.fetchone()

            if result is None:
                return None
            else:
                return self.add_user_info(result)
    
    def add_user_info(self, result):
        uid = result['uid']
        with self.get_cursor() as cursor:
            query = 'SELECT 1 FROM gruppenmitglied JOIN gruppe ON gruppe.gid = gruppenmitglied.gId WHERE gruppenmitglied.uId = %s AND gruppe.account = "lehrer" LIMIT 1'
            cursor.execute(query, [uid])
            if cursor.fetchone() is None:       # Schüler
                query = "SELECT name FROM klasse JOIN klassenmitglied ON klassenmitglied.cId = klasse.cId WHERE uId = %s LIMIT 1"
                cursor.execute(query, [uid])
                row = cursor.fetchone()
                p = Schueler()
                p.klasse = row['name']
                if p.klasse.lower().startswith('q2'):
                    p.stufe = 13
                elif p.klasse.lower().startswith('q1'):
                    p.stufe = 12
                elif p.klasse.lower().startswith('e'):
                    p.stufe = 11
                else:
                    p.stufe = int(p.klasse[0])
                
            else:                               # Lehrer
                p = Organisator()

            p.uid = result['uid']
            p.email = result['email']
            p.vorname = result['firstname']
            p.nachname = result['lastname']
            
            return p
        
    def get_user_by_email(self, email):
        '''
            Gibt den Schüler mit der email zurück
            
            Author:
            Louis
        '''
        with self.get_cursor() as cursor:
            query = "SELECT * FROM `user` WHERE email = %s AND active = 1 LIMIT 1"
            cursor.execute(query, [email])
            result = cursor.fetchone()

            if result is None:
                return None
            else:
                return self.add_user_info(result)
                
    def get_users(self, uid_list=None):
        '''
            Gibt eine Liste von Benutzern zurück. Wenn uid_list eine Liste (nicht None) ist, werden nur die Nutzer mit den uids der Liste zurückgegeben
        '''
        query = "SELECT uid, email, firstname, lastname FROM user WHERE active = 1 ORDER BY lastname, firstname"
        
        if uid_list is not None:
            id_str = ",".join([int(uid) for uid in uid_list])
            query += " WHERE uid IN ({id_str})"
        
        with self.get_cursor() as cursor:
            cursor.execute(query)
            return [
                Person(
                    row['uid'],
                    row['email'],
                    row['firstname'],
                    row['lastname']
                ) for row in cursor.fetchall()
            ]
                
    def get_rooms(self):
        '''
            Gibt eine Liste mit allen Räumen zurück
            
            Author:
            Louis
        '''
    
    def add_project(self, p):
        '''
            Erstellt ein neues Projekt
            
            Author:
            Mats, Louis
        '''
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                query = "INSERT INTO projekt (name, beschreibung, plätze_min, plätze_max, klasse_min, klasse_max) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(query, [p.name, p.beschreibung, p.plaetze_min, p.plaetze_max, p.klasse_min, p.klasse_max])
                pid = cursor.lastrowid
                for o in p.organisatoren:
                    cursor.execute("INSERT INTO leitet (pId, uId) VALUES (%s, %s)", (pid, o.uid))
                conn.commit()
                return pid
    
    def can_choice(self, pid, stufe):
        with self.get_cursor() as cursor:
            query = "SELECT 1 FROM projekt WHERE pid = %s AND %s >= klasse_min AND %s <= klasse_max LIMIT 1"
            cursor.execute(query, (pid, stufe, stufe))
            return cursor.fetchone() is not None
            
    def add_choice(self, uid, pid1, pid2, pid3):
        '''
            Erstellt eine neue Wahl
            
            Author:
            Max, Bendix
        '''
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                query = "INSERT INTO wählt (uid, pid, no) VALUES (%s, %s, %s)"
                cursor.executemany(query, [
                    [uid, pid1, 1],
                    [uid, pid2, 2],
                    [uid, pid3, 3]
                ])
                conn.commit()

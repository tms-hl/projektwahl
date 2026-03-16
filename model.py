import mysql.connector
from mysql.connector import pooling
from contextlib import contextmanager

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
            return result
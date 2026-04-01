import sqlite3
from pathlib import Path
from core.config import ConfigManager

class DatabaseConnection:
    """Maneja la conexión a la base de datos"""
    
    _instance = None
    _connection = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def connect(self):
        """Establece la conexión a la base de datos"""
        if self._connection is not None:
            return self._connection
        
        config = ConfigManager()
        db_path = config.get_db_path()
        
        # Verificar si la base de datos existe y tiene las tablas
        from database.init_db import check_database, init_database
        if not check_database(db_path):
            init_database(db_path)
        
        self._connection = sqlite3.connect(db_path)
        self._connection.row_factory = sqlite3.Row  # Permite acceder por nombre de columna
        return self._connection
    
    def get_cursor(self):
        """Obtiene un cursor para la conexión"""
        conn = self.connect()
        return conn.cursor()
    
    def execute(self, query, params=None):
        """Ejecuta una consulta y retorna el cursor"""
        cursor = self.get_cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        self._connection.commit()
        return cursor
    
    def close(self):
        """Cierra la conexión"""
        if self._connection:
            self._connection.close()
            self._connection = None
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
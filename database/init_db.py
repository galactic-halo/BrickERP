import sqlite3
from pathlib import Path

def init_database(db_path):
    """Crea las tablas iniciales del sistema"""
    
    # Asegurar que el directorio existe
    db_dir = Path(db_path).parent
    db_dir.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Tabla de empresa (metadatos)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS empresa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            razon_social TEXT NOT NULL,
            cuit TEXT,
            domicilio TEXT,
            telefono TEXT,
            email TEXT,
            fecha_inicio_actividades DATE
        )
    ''')
    
    # Tabla de configuración fiscal
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS config_fiscal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pais TEXT,
            moneda TEXT,
            ejercicio_inicio DATE,
            iva_alicuota_general REAL
        )
    ''')
    
    # Tabla de obras (básica, se expandirá después)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS obras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            direccion TEXT,
            cliente TEXT,
            fecha_inicio DATE,
            fecha_fin_estimada DATE,
            estado TEXT DEFAULT 'presupuestada',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla de hitos (para gestión de plazos)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hitos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            obra_id INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            fecha_compromiso DATE,
            fecha_real DATE,
            es_contractual BOOLEAN DEFAULT 0,
            penalizacion_dias INTEGER DEFAULT 0,
            monto_penalizacion REAL DEFAULT 0,
            FOREIGN KEY (obra_id) REFERENCES obras(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    
    return True

def check_database(db_path):
    """Verifica si la base de datos existe y tiene las tablas necesarias"""
    if not Path(db_path).exists():
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='empresa'")
        result = cursor.fetchone()
        conn.close()
        return result is not None
    except:
        return False
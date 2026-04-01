from PySide6.QtCore import QSettings
from pathlib import Path

class ConfigManager:
    """Maneja la configuración persistente usando QSettings"""
    
    def __init__(self):
        self.settings = QSettings("Fabrickasa", "BrickERP")
    
    def is_configured(self):
        """Verifica si el sistema ya fue configurado"""
        return self.settings.value("setup_completed", False, type=bool)
    
    def get_company_data(self):
        """Obtiene los datos de la empresa"""
        return {
            "business_type": self.settings.value("business_type", ""),
            "legal_name": self.settings.value("legal_name", ""),
            "tax_id": self.settings.value("tax_id", ""),
            "address": self.settings.value("address", ""),
            "phone": self.settings.value("phone", ""),
            "email": self.settings.value("email", ""),
            "logo_path": self.settings.value("logo_path", "")
        }
    
    def save_company_data(self, data):
        """Guarda los datos de la empresa"""
        for key, value in data.items():
            self.settings.setValue(key, value)
        self.settings.setValue("setup_completed", True)
    
    def get_db_path(self):
        """Obtiene la ruta de la base de datos"""
        db_path = self.settings.value("db_path", "")
        if not db_path:
            data_dir = Path(__file__).parent.parent / "data"
            data_dir.mkdir(exist_ok=True)
            db_path = str(data_dir / "brickerp.db")
        return db_path
    
    def set_db_path(self, path):
        self.settings.setValue("db_path", path)
    
    def get_license(self):
        return {
            "license_type": self.settings.value("license_type", "trial"),
            "registered_to": self.settings.value("registered_to", ""),
            "license_key": self.settings.value("license_key", "")
        }
    
    def save_license(self, license_type, registered_to, license_key):
        self.settings.setValue("license_type", license_type)
        self.settings.setValue("registered_to", registered_to)
        self.settings.setValue("license_key", license_key)
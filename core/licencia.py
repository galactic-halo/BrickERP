from datetime import datetime, timedelta
from core.version import VERSION

class LicenciaManager:
    """Manejo básico de licencias (simulado para fase inicial)"""
    
    def __init__(self):
        self.trial_days = 30
    
    def validate_license(self, license_type, license_key=None):
        """Valida el tipo de licencia"""
        if license_type == "trial":
            return self._validate_trial()
        elif license_type == "professional":
            return self._validate_professional(license_key)
        elif license_type == "free":
            return True
        return False
    
    def _validate_trial(self):
        """Verifica si el período de prueba sigue vigente"""
        # En una implementación real, guardar fecha de primera ejecución
        # Por ahora, siempre válido
        return True
    
    def _validate_professional(self, license_key):
        """Valida una clave profesional (placeholder)"""
        # Implementación real después
        return license_key == "BRICK-ERP-PRO-2026"
    
    def get_license_info(self):
        """Retorna información de la licencia actual"""
        return {
            "version": VERSION,
            "type": "trial",
            "expires": (datetime.now() + timedelta(days=self.trial_days)).strftime("%Y-%m-%d"),
            "features": ["obras_ilimitadas", "presupuestos", "costos_reales", "hitos"]
        }
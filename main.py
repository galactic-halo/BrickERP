#!/usr/bin/env python
"""
BrickERP - Punto de entrada principal
"""

import sys
import os
from pathlib import Path

# Asegurar que podemos importar módulos locales
sys.path.insert(0, str(Path(__file__).parent))

from PySide6.QtWidgets import QApplication, QMessageBox, QWizard
from PySide6.QtCore import Qt

from core.config import ConfigManager
from core.version import SOFTWARE_NAME, VERSION
from ui.setup_wizard import SetupWizard
from ui.main_window import MainWindow


def main():
    """Punto de entrada principal"""
    
    app = QApplication(sys.argv)
    app.setApplicationName(SOFTWARE_NAME)
    app.setApplicationVersion(VERSION)
    app.setOrganizationName("Fabrickasa")
    
    # Verificar si ya está configurado
    config = ConfigManager()
    
    if not config.is_configured():
        # Primera ejecución: mostrar wizard
        wizard = SetupWizard()
        if wizard.exec() == QWizard.Accepted:
            # Configuración exitosa, iniciar ventana principal
            company_data = config.get_company_data()
            main_window = MainWindow(company_data.get("legal_name", "Usuario"))
            main_window.show()
        else:
            # Usuario canceló
            sys.exit(0)
    else:
        # Configuración existente, ir directo a ventana principal
        company_data = config.get_company_data()
        main_window = MainWindow(company_data.get("legal_name", "Usuario"))
        main_window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
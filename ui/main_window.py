from PySide6.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QWidget, QMenuBar, QMenu,
    QMessageBox, QPushButton, QHBoxLayout, QFrame,QWizard
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction,QPixmap

from core.version import SOFTWARE_NAME, VERSION
from core.config import ConfigManager


class MainWindow(QMainWindow):
    """Ventana principal de BrickERP"""
    
    # Señal para indicar que se necesita reconfigurar
    reconfigurar_signal = Signal()
    
    def __init__(self, company_name):
        super().__init__()
        self.company_name = company_name
        self.config = ConfigManager()
        
        self.setWindowTitle(f"{SOFTWARE_NAME} v{VERSION} - {company_name}")
        self.setMinimumSize(1024, 768)
        
        self._setup_menu()
        self._setup_central_widget()
        self._setup_statusbar()
        
        # Conectar señal
        self.reconfigurar_signal.connect(self._reconfigurar)
    
    def _setup_menu(self):
        """Configura la barra de menú"""
        menubar = self.menuBar()
        
        # Menú Archivo
        file_menu = menubar.addMenu("&Archivo")
        
        # Submenú Configuración
        config_action = QAction("&Datos de la empresa", self)
        config_action.triggered.connect(self._mostrar_datos_empresa)
        file_menu.addAction(config_action)
        
        reconfig_action = QAction("&Reconfigurar BrickERP", self)
        reconfig_action.triggered.connect(self._confirmar_reconfigurar)
        file_menu.addAction(reconfig_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("&Salir", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Menú Obras (placeholder)
        obras_menu = menubar.addMenu("&Obras")
        nueva_obra_action = QAction("&Nueva obra", self)
        nueva_obra_action.triggered.connect(self._mostrar_mensaje_desarrollo)
        obras_menu.addAction(nueva_obra_action)
        
        listar_obras_action = QAction("&Listar obras", self)
        listar_obras_action.triggered.connect(self._mostrar_mensaje_desarrollo)
        obras_menu.addAction(listar_obras_action)
        
        # Menú Ayuda
        ayuda_menu = menubar.addMenu("&Ayuda")
        acerca_action = QAction("&Acerca de", self)
        acerca_action.triggered.connect(self._mostrar_acerca_de)
        ayuda_menu.addAction(acerca_action)
    
    def _setup_central_widget(self):
        """Configura el widget central con información del proyecto"""
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # Header con logo y datos de empresa
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                border-bottom: 2px solid #3498db;
            }
        """)
        header_layout = QHBoxLayout(header)
        
        # Logo (si existe)
        logo_path = self.config.get_company_data().get("logo_path", "")
        if logo_path:
            try:
                logo_label = QLabel()
                pixmap = QPixmap(logo_path)
                if not pixmap.isNull():
                    logo_label.setPixmap(pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                    header_layout.addWidget(logo_label)
            except:
                pass
        
        # Título y subtítulo
        title_layout = QVBoxLayout()
        title = QLabel(f"{SOFTWARE_NAME}")
        title.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        title_layout.addWidget(title)
        
        subtitle = QLabel(f"Bienvenido, {self.company_name}")
        subtitle.setStyleSheet("color: #bdc3c7; font-size: 14px;")
        title_layout.addWidget(subtitle)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        layout.addWidget(header)
        
        # Contenido principal
        content = QWidget()
        content_layout = QVBoxLayout(content)
        
        # Mensaje de bienvenida
        welcome = QLabel("Panel de control")
        welcome.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 20px;")
        welcome.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(welcome)
        
        # Información de la empresa
        company_info = self._get_company_info_text()
        info_label = QLabel(company_info)
        info_label.setWordWrap(True)
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet("margin: 20px; padding: 20px; background-color: #ecf0f1; border-radius: 8px;")
        content_layout.addWidget(info_label)
        
        # Botones de acceso rápido (placeholder)
        buttons_layout = QHBoxLayout()
        
        btn_obras = QPushButton("📋 Gestión de Obras")
        btn_obras.setMinimumHeight(60)
        btn_obras.clicked.connect(self._mostrar_mensaje_desarrollo)
        buttons_layout.addWidget(btn_obras)
        
        btn_presupuesto = QPushButton("💰 Presupuestos")
        btn_presupuesto.setMinimumHeight(60)
        btn_presupuesto.clicked.connect(self._mostrar_mensaje_desarrollo)
        buttons_layout.addWidget(btn_presupuesto)
        
        btn_reportes = QPushButton("📊 Reportes")
        btn_reportes.setMinimumHeight(60)
        btn_reportes.clicked.connect(self._mostrar_mensaje_desarrollo)
        buttons_layout.addWidget(btn_reportes)
        
        content_layout.addLayout(buttons_layout)
        content_layout.addStretch()
        
        layout.addWidget(content)
    
    def _setup_statusbar(self):
        """Configura la barra de estado"""
        self.statusBar().showMessage("Listo - BrickERP versión profesional")
    
    def _get_company_info_text(self):
        """Obtiene texto con información de la empresa"""
        data = self.config.get_company_data()
        license_info = self.config.get_license()
        
        license_type_map = {
            "trial": "🔓 Trial (30 días)",
            "professional": "⭐ Profesional",
            "free": "🆓 Gratuita"
        }
        
        info = f"""
        <b>Empresa:</b> {data.get('legal_name', 'No registrado')}<br>
        <b>CUIT/RFC:</b> {data.get('tax_id', 'No registrado')}<br>
        <b>Domicilio:</b> {data.get('address', 'No registrado')}<br>
        <b>Teléfono:</b> {data.get('phone', 'No registrado')}<br>
        <b>Email:</b> {data.get('email', 'No registrado')}<br>
        <b>Licencia:</b> {license_type_map.get(license_info.get('license_type'), 'Desconocida')}
        """
        return info
    
    def _mostrar_datos_empresa(self):
        """Muestra un diálogo con los datos de la empresa"""
        data = self.config.get_company_data()
        license_info = self.config.get_license()
        
        info = f"""Datos de la empresa:

Razón social: {data.get('legal_name', 'No registrado')}
CUIT/RFC: {data.get('tax_id', 'No registrado')}
Domicilio: {data.get('address', 'No registrado')}
Teléfono: {data.get('phone', 'No registrado')}
Email: {data.get('email', 'No registrado')}
Tipo de licencia: {license_info.get('license_type', 'Desconocida')}
Versión: {SOFTWARE_NAME} {VERSION}
"""
        QMessageBox.information(self, "Datos de la empresa", info)
    
    def _confirmar_reconfigurar(self):
        """Confirma y ejecuta la reconfiguración"""
        reply = QMessageBox.question(
            self,
            "Reconfigurar BrickERP",
            "¿Estás seguro de que deseas reconfigurar BrickERP?\n\n"
            "Esto borrará la configuración actual y se abrirá el asistente de configuración.\n"
            "Los datos de la base de datos NO se eliminarán.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.reconfigurar_signal.emit()
    
    def _reconfigurar(self):
        """Reinicia la configuración y lanza el wizard"""
        # Borrar configuración
        self.config.settings.clear()
        
        # Cerrar ventana actual y lanzar wizard
        self.close()
        
        # Importar aquí para evitar circular imports
        from ui.setup_wizard import SetupWizard
        import sys
        from PySide6.QtWidgets import QApplication
        
        wizard = SetupWizard()
        if wizard.exec() == QWizard.Accepted:
            # Reiniciar aplicación
            QApplication.quit()
            # Lanzar nueva instancia (esto depende del SO)
            import subprocess
            subprocess.Popen([sys.executable, sys.argv[0]])
        else:
            # Si cancela, salir
            sys.exit(0)
    
    def _mostrar_mensaje_desarrollo(self):
        """Muestra mensaje de funcionalidad en desarrollo"""
        QMessageBox.information(
            self,
            "En desarrollo",
            "Esta funcionalidad estará disponible en la próxima versión.\n\n"
            "Próximamente: módulo de gestión de obras."
        )
    
    def _mostrar_acerca_de(self):
        """Muestra el diálogo Acerca de"""
        QMessageBox.about(
            self,
            f"Acerca de {SOFTWARE_NAME}",
            f"<b>{SOFTWARE_NAME}</b><br>"
            f"Versión {VERSION}<br><br>"
            f"ERP de construcción 4.0<br>"
            f"Diseñado para pequeñas y medianas empresas del sector.<br><br>"
            f"© 2026 Fabrickasa - Todos los derechos reservados.<br><br>"
            f"<i>Integración con Revit, Neodata y MSProject</i>"
        )
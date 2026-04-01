from PySide6.QtWidgets import (
    QWizard, QWizardPage, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QComboBox, QDateEdit, QPushButton, QFileDialog,
    QMessageBox, QRadioButton, QButtonGroup, QGroupBox, QFormLayout
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QPixmap
from pathlib import Path
import sys

from core.config import ConfigManager
from core.licencia import LicenciaManager
from database.init_db import init_database, check_database
from core.version import SOFTWARE_NAME, VERSION

class BienvenidaPage(QWizardPage):
    """Página 1: Bienvenida y presentación"""
    
    def __init__(self):
        super().__init__()
        self.setTitle(f"Bienvenido a {SOFTWARE_NAME}")
        
        layout = QVBoxLayout()
        
        # Logo o título
        title = QLabel(f"{SOFTWARE_NAME} v{VERSION}")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Descripción
        desc = QLabel(
            "Este asistente te guiará en la configuración inicial de BrickERP.\n\n"
            "BrickERP es un sistema de gestión para empresas de construcción "
            "diseñado para ayudarte a administrar obras, presupuestos, costos "
            "y certificaciones de manera integrada.\n\n"
            "Completa los siguientes pasos para comenzar."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("font-size: 12px; margin: 20px;")
        desc.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc)
        
        self.setLayout(layout)
    
    def nextId(self):
        return 1


class EmpresaPage(QWizardPage):
    """Página 2: Datos de la empresa o persona física"""
    
    def __init__(self):
        super().__init__()
        self.setTitle("Datos de la empresa")
        self.setSubTitle("Ingresa la información de tu empresa o datos personales")
        
        layout = QFormLayout()
        
        # Tipo de contribuyente
        self.business_type = QComboBox()
        self.business_type.addItems(["Persona Física", "Persona Moral"])
        layout.addRow("Tipo:", self.business_type)
        
        # Razón social / Nombre
        self.legal_name = QLineEdit()
        self.legal_name.setPlaceholderText("Ej: Fabrickasa S.A. o Juan Pérez")
        layout.addRow("Razón social / Nombre:", self.legal_name)
        
        # CUIT / RFC
        self.tax_id = QLineEdit()
        self.tax_id.setPlaceholderText("Ej: 30-12345678-9")
        layout.addRow("RFC / CUIT:", self.tax_id)
        
        # Domicilio
        self.address = QLineEdit()
        layout.addRow("Domicilio fiscal:", self.address)
        
        # Teléfono
        self.phone = QLineEdit()
        layout.addRow("Teléfono:", self.phone)
        
        # Email
        self.email = QLineEdit()
        layout.addRow("Email:", self.email)
        
        # Logo (opcional)
        logo_layout = QHBoxLayout()
        self.logo_path = QLineEdit()
        self.logo_path.setReadOnly(True)
        self.logo_path.setPlaceholderText("Ruta del logo (opcional)")
        logo_btn = QPushButton("Seleccionar")
        logo_btn.clicked.connect(self.select_logo)
        logo_layout.addWidget(self.logo_path)
        logo_layout.addWidget(logo_btn)
        layout.addRow("Logo:", logo_layout)
        
        self.setLayout(layout)
        
        # Registrar campos como obligatorios
        self.registerField("business_type*", self.business_type)
        self.registerField("legal_name*", self.legal_name)
        self.registerField("tax_id", self.tax_id)
        self.registerField("address", self.address)
        self.registerField("phone", self.phone)
        self.registerField("email", self.email)
        self.registerField("logo_path", self.logo_path)
    
    def select_logo(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar logo", "", "Imágenes (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            self.logo_path.setText(file_path)
    
    def nextId(self):
        return 2


class DatabasePage(QWizardPage):
    """Página 3: Configuración de base de datos"""
    
    def __init__(self):
        super().__init__()
        self.setTitle("Base de datos")
        self.setSubTitle("Configura dónde se almacenarán los datos")
        
        layout = QVBoxLayout()
        
        # Grupo de opciones
        group = QGroupBox("Ubicación de la base de datos")
        group_layout = QVBoxLayout()
        
        # Radio buttons
        self.use_default = QRadioButton("Usar ubicación por defecto (./data/brickerp.db)")
        self.use_custom = QRadioButton("Usar ubicación personalizada")
        self.use_default.setChecked(True)
        
        self.custom_path = QLineEdit()
        self.custom_path.setEnabled(False)
        self.custom_path.setPlaceholderText("Ruta completa para brickerp.db")
        
        browse_btn = QPushButton("Seleccionar carpeta")
        browse_btn.clicked.connect(self.select_folder)
        browse_btn.setEnabled(False)
        
        # Conectar radio buttons
        self.use_custom.toggled.connect(lambda checked: self.custom_path.setEnabled(checked))
        self.use_custom.toggled.connect(lambda checked: browse_btn.setEnabled(checked))
        
        path_layout = QHBoxLayout()
        path_layout.addWidget(self.custom_path)
        path_layout.addWidget(browse_btn)
        
        group_layout.addWidget(self.use_default)
        group_layout.addWidget(self.use_custom)
        group_layout.addLayout(path_layout)
        group.setLayout(group_layout)
        
        layout.addWidget(group)
        self.setLayout(layout)
        
        self.registerField("db_path", self.custom_path)
        self.registerField("use_default_db", self.use_default)
    
    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta para la base de datos")
        if folder:
            self.custom_path.setText(str(Path(folder) / "brickerp.db"))
    
    def nextId(self):
        return 3


class FiscalPage(QWizardPage):
    """Página 4: Configuración fiscal inicial"""
    
    def __init__(self):
        super().__init__()
        self.setTitle("Configuración fiscal")
        self.setSubTitle("Parámetros fiscales básicos")
        
        layout = QFormLayout()
        
        # País
        self.pais = QComboBox()
        self.pais.addItems(["México", "Argentina", "Colombia", "Chile", "Perú", "Otro"])
        layout.addRow("País:", self.pais)
        
        # Moneda
        self.moneda = QComboBox()
        self.moneda.addItems(["MXN", "ARS", "COP", "CLP", "PEN", "USD"])
        layout.addRow("Moneda funcional:", self.moneda)
        
        # Inicio del ejercicio
        self.ejercicio_inicio = QDateEdit()
        self.ejercicio_inicio.setDate(QDate.currentDate())
        self.ejercicio_inicio.setCalendarPopup(True)
        layout.addRow("Inicio del ejercicio:", self.ejercicio_inicio)
        
        # IVA general (placeholder)
        self.iva = QLineEdit()
        self.iva.setPlaceholderText("Ej: 16")
        self.iva.setText("16")
        layout.addRow("IVA general (%):", self.iva)
        
        self.setLayout(layout)
        
        self.registerField("pais", self.pais)
        self.registerField("moneda", self.moneda)
        self.registerField("ejercicio_inicio", self.ejercicio_inicio)
        self.registerField("iva", self.iva)
    
    def nextId(self):
        return 4


class LicenciaPage(QWizardPage):
    """Página 5: Licencia"""
    
    def __init__(self):
        super().__init__()
        self.setTitle("Licencia")
        self.setSubTitle("Configuración de licencia")
        
        layout = QVBoxLayout()
        
        # Grupo de tipo de licencia
        group = QGroupBox("Tipo de licencia")
        group_layout = QVBoxLayout()
        
        self.license_type = QButtonGroup()
        self.radio_free = QRadioButton("Gratuita (funcionalidades básicas)")
        self.radio_trial = QRadioButton("Trial 30 días (todas las funcionalidades)")
        self.radio_pro = QRadioButton("Profesional (requiere clave)")
        
        self.radio_trial.setChecked(True)
        self.license_type.addButton(self.radio_free)
        self.license_type.addButton(self.radio_trial)
        self.license_type.addButton(self.radio_pro)
        
        group_layout.addWidget(self.radio_free)
        group_layout.addWidget(self.radio_trial)
        group_layout.addWidget(self.radio_pro)
        
        # Campo para clave profesional
        self.license_key = QLineEdit()
        self.license_key.setPlaceholderText("Ingresar clave de licencia")
        self.license_key.setEnabled(False)
        self.radio_pro.toggled.connect(self.license_key.setEnabled)
        
        group_layout.addWidget(QLabel("Clave profesional:"))
        group_layout.addWidget(self.license_key)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
        
        # Info de versión
        info = QLabel(f"Versión: {SOFTWARE_NAME} {VERSION}")
        info.setStyleSheet("color: gray; margin-top: 20px;")
        layout.addWidget(info)
        
        self.setLayout(layout)
        
        self.registerField("license_type_free", self.radio_free)
        self.registerField("license_type_trial", self.radio_trial)
        self.registerField("license_type_pro", self.radio_pro)
        self.registerField("license_key", self.license_key)
    
    def nextId(self):
        return 5


class ResumenPage(QWizardPage):
    """Página 6: Resumen y finalización"""
    
    def __init__(self):
        super().__init__()
        self.setTitle("Resumen de configuración")
        self.setSubTitle("Verifica los datos antes de finalizar")
        
        self.layout = QVBoxLayout()
        self.resumen_text = QLabel()
        self.resumen_text.setWordWrap(True)
        self.resumen_text.setStyleSheet("font-family: monospace; padding: 10px; background-color: #f5f5f5;")
        self.layout.addWidget(self.resumen_text)
        
        self.setLayout(self.layout)
    
    def initializePage(self):
        """Se ejecuta al mostrar la página"""
        wizard = self.wizard()
        empresa_data = {
            "Tipo": wizard.field("business_type"),
            "Razón social": wizard.field("legal_name"),
            "CUIT/RFC": wizard.field("tax_id"),
            "Domicilio": wizard.field("address"),
            "Teléfono": wizard.field("phone"),
            "Email": wizard.field("email"),
        }
        
        # Base de datos
        if wizard.field("use_default_db"):
            db_path = str(Path(__file__).parent.parent / "data" / "brickerp.db")
        else:
            db_path = wizard.field("db_path")
        
        # Licencia
        if wizard.field("license_type_trial"):
            license_type = "Trial 30 días"
        elif wizard.field("license_type_pro"):
            license_type = "Profesional"
        else:
            license_type = "Gratuita"
        
        resumen = "DATOS DE EMPRESA:\n"
        resumen += "-" * 30 + "\n"
        for key, value in empresa_data.items():
            resumen += f"{key}: {value}\n"
        
        resumen += "\nBASE DE DATOS:\n" + "-" * 30 + "\n"
        resumen += f"Ruta: {db_path}\n"
        
        resumen += "\nCONFIGURACIÓN FISCAL:\n" + "-" * 30 + "\n"
        resumen += f"País: {wizard.field('pais')}\n"
        resumen += f"Moneda: {wizard.field('moneda')}\n"
        resumen += f"Ejercicio: {wizard.field('ejercicio_inicio').toString('dd/MM/yyyy')}\n"
        resumen += f"IVA general: {wizard.field('iva')}%\n"
        
        resumen += "\nLICENCIA:\n" + "-" * 30 + "\n"
        resumen += f"Tipo: {license_type}\n"
        
        self.resumen_text.setText(resumen)
        self.db_path = db_path
    
    def nextId(self):
        return -1  # Finalizar


class SetupWizard(QWizard):
    """Wizard de configuración inicial"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{SOFTWARE_NAME} - Configuración inicial")
        self.setWizardStyle(QWizard.ModernStyle)
        self.setMinimumSize(600, 500)
        
        # Agregar páginas
        self.addPage(BienvenidaPage())
        self.addPage(EmpresaPage())
        self.addPage(DatabasePage())
        self.addPage(FiscalPage())
        self.addPage(LicenciaPage())
        self.addPage(ResumenPage())
        
        self.button(QWizard.FinishButton).clicked.connect(self.finish_setup)
    
    def finish_setup(self):
        """Guarda la configuración y crea la base de datos"""
        
        # Obtener datos
        config = ConfigManager()
        
        # Datos de empresa
        company_data = {
            "business_type": self.field("business_type"),
            "legal_name": self.field("legal_name"),
            "tax_id": self.field("tax_id"),
            "address": self.field("address"),
            "phone": self.field("phone"),
            "email": self.field("email"),
            "logo_path": self.field("logo_path")
        }
        config.save_company_data(company_data)
        
        # Ruta de base de datos
        if self.field("use_default_db"):
            db_path = str(Path(__file__).parent.parent / "data" / "brickerp.db")
        else:
            db_path = self.field("db_path")
        config.set_db_path(db_path)
        
        # Licencia
        if self.field("license_type_trial"):
            license_type = "trial"
            license_key = ""
        elif self.field("license_type_pro"):
            license_type = "professional"
            license_key = self.field("license_key")
        else:
            license_type = "free"
            license_key = ""
        
        config.save_license(license_type, self.field("legal_name"), license_key)
        
        # Crear base de datos
        try:
            init_database(db_path)
            QMessageBox.information(
                self, "Configuración completa",
                f"¡Configuración completada con éxito!\n\n"
                f"Base de datos creada en:\n{db_path}\n\n"
                f"BrickERP se iniciará ahora."
            )
            self.accept()
        except Exception as e:
            QMessageBox.critical(
                self, "Error",
                f"No se pudo crear la base de datos:\n{str(e)}"
            )
"""
Módulo: ventana_principal.py
Descripción: Ventana principal de la aplicación. Gestiona la navegación
             entre las distintas vistas mediante un QStackedWidget.
"""

from PyQt5.QtWidgets import (
    QMainWindow, QStackedWidget, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

from vistas.vista_selector_nota import VistaSelectorNota
from vistas.vista_formulario_paciente import VistaFormularioPaciente
from vistas.vista_procedimientos import VistaProcedimientos
from vistas.vista_resumen import VistaResumen
from vistas.vista_revaloracion import VistaRevaloracion
from vistas.vista_turno import VistaEntregaTurno, VistaReciboTurno
from modelos.nota import NotaClinica


# Índices de vistas en el stack
VISTA_SELECTOR = 0
VISTA_PACIENTE = 1
VISTA_PROCEDIMIENTOS = 2
VISTA_RESUMEN = 3
VISTA_REVALORACION = 4
VISTA_ENTREGA_TURNO = 5
VISTA_RECIBO_TURNO = 6


class VentanaPrincipal(QMainWindow):
    """
    Ventana principal que contiene el stack de vistas y la barra de estado.
    Centraliza la navegación entre pantallas de la aplicación.
    """

    def __init__(self, controlador_app):
        super().__init__()
        self.controlador_app = controlador_app
        self.controlador_app.establecer_ventana_principal(self)
        self._configurar_ventana()
        self._construir_interfaz()

    def _configurar_ventana(self):
        """Configura las propiedades básicas de la ventana principal."""
        self.setWindowTitle("Sistema de Notas de Enfermería - Urgencias")
        self.setMinimumSize(850, 650)
        self.resize(950, 720)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ecf0f1;
            }
            QGroupBox {
                border: 1px solid #bdc3c7;
                border-radius: 6px;
                margin-top: 8px;
                padding: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: #2c3e50;
            }
            QLineEdit, QComboBox, QTextEdit {
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                padding: 4px 6px;
                background-color: white;
            }
            QLineEdit:focus, QComboBox:focus, QTextEdit:focus {
                border: 1px solid #3498db;
            }
        """)

    def _construir_interfaz(self):
        """Construye la interfaz principal con encabezado y stack de vistas."""
        widget_central = QWidget()
        diseno_central = QVBoxLayout()
        diseno_central.setContentsMargins(0, 0, 0, 0)
        diseno_central.setSpacing(0)

        # Barra superior
        barra_superior = QFrame()
        barra_superior.setFixedHeight(50)
        barra_superior.setStyleSheet("background-color: #2c3e50;")
        diseno_barra = QHBoxLayout()
        diseno_barra.setContentsMargins(20, 0, 20, 0)

        lbl_app = QLabel("🏥 Sistema de Notas de Enfermería")
        lbl_app.setFont(QFont("Arial", 13, QFont.Bold))
        lbl_app.setStyleSheet("color: white;")

        self.lbl_tipo_nota = QLabel("")
        self.lbl_tipo_nota.setFont(QFont("Arial", 10))
        self.lbl_tipo_nota.setStyleSheet("color: #bdc3c7;")

        diseno_barra.addWidget(lbl_app)
        diseno_barra.addStretch()
        diseno_barra.addWidget(self.lbl_tipo_nota)
        barra_superior.setLayout(diseno_barra)

        # Indicador de pasos
        self.barra_pasos = BarraPasos()

        # Stack de vistas
        self.stack = QStackedWidget()

        self.vista_selector = VistaSelectorNota(self.controlador_app)
        self.vista_paciente = VistaFormularioPaciente(self.controlador_app)
        self.vista_procedimientos = VistaProcedimientos(self.controlador_app)
        self.vista_resumen = VistaResumen(self.controlador_app)

        self.vista_revaloracion = VistaRevaloracion(self.controlador_app)
        self.vista_entrega_turno = VistaEntregaTurno(self.controlador_app)
        self.vista_recibo_turno = VistaReciboTurno(self.controlador_app)

        self.stack.addWidget(self.vista_selector)        # índice 0
        self.stack.addWidget(self.vista_paciente)        # índice 1
        self.stack.addWidget(self.vista_procedimientos)  # índice 2
        self.stack.addWidget(self.vista_resumen)         # índice 3
        self.stack.addWidget(self.vista_revaloracion)    # índice 4
        self.stack.addWidget(self.vista_entrega_turno)   # índice 5
        self.stack.addWidget(self.vista_recibo_turno)    # índice 6

        diseno_central.addWidget(barra_superior)
        diseno_central.addWidget(self.barra_pasos)
        diseno_central.addWidget(self.stack)

        widget_central.setLayout(diseno_central)
        self.setCentralWidget(widget_central)

    # ------------------------------------------------------------------
    # Métodos de navegación
    # ------------------------------------------------------------------

    def navegar_a_selector(self):
        """Navega a la vista de selección de tipo de nota."""
        self.vista_selector.actualizar_estadisticas()
        self.stack.setCurrentIndex(VISTA_SELECTOR)
        self.lbl_tipo_nota.setText("")
        self.barra_pasos.establecer_paso(0)

    def navegar_a_formulario_paciente(self):
        """Navega a la vista de datos del paciente, adaptando UI según tipo de nota."""
        nota = self.controlador_app.controlador_nota.nota_actual
        if nota:
            self.lbl_tipo_nota.setText(f"│ {nota.tipo}")
            # Activar/desactivar modo revaloración en el formulario
            if nota.tipo == NotaClinica.TIPO_REVALORACION:
                self.vista_paciente.activar_modo_revaloracion()
            else:
                self.vista_paciente.desactivar_modo_revaloracion()
        self.stack.setCurrentIndex(VISTA_PACIENTE)
        self.barra_pasos.establecer_paso(1)

    def navegar_a_procedimientos(self):
        """
        Navega a la vista adecuada según el tipo de nota:
        - Revaloración → vista_revaloracion
        - Entrega de turno → vista_entrega_turno
        - Recibo de turno → vista_recibo_turno
        - Resto → vista_procedimientos normal
        """
        nota = self.controlador_app.controlador_nota.nota_actual
        tipo = nota.tipo if nota else ""

        if tipo == NotaClinica.TIPO_REVALORACION:
            self.stack.setCurrentIndex(VISTA_REVALORACION)
        elif tipo == NotaClinica.TIPO_ENTREGA_TURNO:
            self.stack.setCurrentIndex(VISTA_ENTREGA_TURNO)
        elif tipo == NotaClinica.TIPO_RECIBO_TURNO:
            self.stack.setCurrentIndex(VISTA_RECIBO_TURNO)
        else:
            self.stack.setCurrentIndex(VISTA_PROCEDIMIENTOS)
            if hasattr(self, "vista_procedimientos"):
                self.vista_procedimientos.sincronizar_semanas_gestante()
        self.barra_pasos.establecer_paso(2)

    def navegar_a_paciente(self):
        """Navega de regreso al formulario del paciente."""
        self.stack.setCurrentIndex(VISTA_PACIENTE)
        self.barra_pasos.establecer_paso(1)

    def navegar_a_resumen(self):
        """Navega a la vista de resumen y carga la nota generada."""
        self.vista_resumen.cargar_nota()
        self.stack.setCurrentIndex(VISTA_RESUMEN)
        self.barra_pasos.establecer_paso(3)

    def limpiar_todas_las_vistas(self):
        """Limpia campos de todas las vistas al crear una nota nueva."""
        self.vista_paciente._limpiar_campos()
        self.vista_procedimientos.limpiar_campos()
        self.vista_revaloracion.limpiar_campos()
        self.vista_entrega_turno.limpiar_campos()
        self.vista_recibo_turno.limpiar_campos()


class BarraPasos(QFrame):
    """
    Barra visual que indica el paso actual del flujo de creación de nota.
    """

    PASOS = ["Tipo de nota", "Datos del paciente", "Procedimientos", "Nota generada"]

    def __init__(self):
        super().__init__()
        self.setFixedHeight(36)
        self.setStyleSheet("background-color: #f2f3f4; border-bottom: 1px solid #d5d8dc;")
        self.diseno = QHBoxLayout()
        self.diseno.setContentsMargins(20, 0, 20, 0)
        self.diseno.setSpacing(4)

        self.etiquetas_paso = []
        for i, nombre in enumerate(self.PASOS):
            lbl = QLabel(f"{i + 1}. {nombre}")
            lbl.setFont(QFont("Arial", 9))
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet("color: #aab7b8; padding: 4px 10px;")
            self.etiquetas_paso.append(lbl)
            self.diseno.addWidget(lbl)
            if i < len(self.PASOS) - 1:
                flecha = QLabel("›")
                flecha.setStyleSheet("color: #aab7b8;")
                self.diseno.addWidget(flecha)

        self.setLayout(self.diseno)
        self.establecer_paso(0)

    def establecer_paso(self, paso_activo: int):
        """Resalta el paso activo y atenúa los demás."""
        for i, lbl in enumerate(self.etiquetas_paso):
            if i == paso_activo:
                lbl.setStyleSheet("""
                    color: #2980b9;
                    font-weight: bold;
                    background-color: #d6eaf8;
                    border-radius: 4px;
                    padding: 4px 10px;
                """)
            elif i < paso_activo:
                lbl.setStyleSheet("color: #27ae60; padding: 4px 10px;")
            else:
                lbl.setStyleSheet("color: #aab7b8; padding: 4px 10px;")

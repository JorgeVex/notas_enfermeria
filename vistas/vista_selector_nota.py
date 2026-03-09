"""
Módulo: vista_selector_nota.py
Descripción: Vista inicial de la aplicación donde el usuario selecciona
             el tipo de nota clínica a generar.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QPushButton, QGroupBox, QCheckBox, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from modelos.nota import NotaClinica


class VistaSelectorNota(QWidget):
    """
    Pantalla inicial donde se selecciona el tipo de nota.
    Incluye opción para activar el flujo SOAT.
    """

    def __init__(self, controlador_app):
        super().__init__()
        self.controlador_app = controlador_app
        self._construir_interfaz()

    def _construir_interfaz(self):
        """Construye todos los componentes visuales de la vista."""
        diseno_principal = QVBoxLayout()
        diseno_principal.setSpacing(20)
        diseno_principal.setContentsMargins(40, 40, 40, 40)

        # Encabezado
        etiqueta_titulo = QLabel("Sistema de Notas de Enfermería")
        etiqueta_titulo.setFont(QFont("Arial", 18, QFont.Bold))
        etiqueta_titulo.setAlignment(Qt.AlignCenter)
        etiqueta_titulo.setStyleSheet("color: #2c3e50;")

        etiqueta_subtitulo = QLabel("Servicio de Urgencias")
        etiqueta_subtitulo.setFont(QFont("Arial", 12))
        etiqueta_subtitulo.setAlignment(Qt.AlignCenter)
        etiqueta_subtitulo.setStyleSheet("color: #7f8c8d;")

        # Separador
        separador = QFrame()
        separador.setFrameShape(QFrame.HLine)
        separador.setStyleSheet("color: #bdc3c7;")

        # Grupo selección de nota
        grupo_nota = QGroupBox("Seleccionar tipo de nota")
        grupo_nota.setFont(QFont("Arial", 11, QFont.Bold))
        diseno_grupo = QVBoxLayout()

        etiqueta_tipo = QLabel("Tipo de nota:")
        etiqueta_tipo.setFont(QFont("Arial", 10))

        self.combo_tipo_nota = QComboBox()
        self.combo_tipo_nota.setFont(QFont("Arial", 10))
        self.combo_tipo_nota.setMinimumHeight(35)
        self.combo_tipo_nota.addItem("-- Seleccione un tipo de nota --")
        for tipo in NotaClinica.TIPOS_DISPONIBLES:
            self.combo_tipo_nota.addItem(tipo)

        diseno_grupo.addWidget(etiqueta_tipo)
        diseno_grupo.addWidget(self.combo_tipo_nota)
        grupo_nota.setLayout(diseno_grupo)

        # Grupo SOAT
        grupo_soat = QGroupBox("Flujo especial")
        grupo_soat.setFont(QFont("Arial", 11, QFont.Bold))
        diseno_soat = QVBoxLayout()

        self.checkbox_soat = QCheckBox(
            "Paciente accidentado cubierto por SOAT"
        )
        self.checkbox_soat.setFont(QFont("Arial", 10))

        diseno_soat.addWidget(self.checkbox_soat)
        grupo_soat.setLayout(diseno_soat)

        # Estadísticas rápidas
        grupo_estadisticas = QGroupBox("Estadísticas de hoy")
        grupo_estadisticas.setFont(QFont("Arial", 11, QFont.Bold))
        diseno_estadisticas = QHBoxLayout()

        resumen = self.controlador_app.obtener_resumen_estadisticas()
        self.etiqueta_notas_hoy = QLabel(
            f"Notas generadas hoy: {resumen.get('notas_hoy', 0)}"
        )
        self.etiqueta_notas_hoy.setFont(QFont("Arial", 10))

        self.etiqueta_notas_mes = QLabel(
            f"Notas este mes: {resumen.get('notas_este_mes', 0)}"
        )
        self.etiqueta_notas_mes.setFont(QFont("Arial", 10))

        diseno_estadisticas.addWidget(self.etiqueta_notas_hoy)
        diseno_estadisticas.addWidget(self.etiqueta_notas_mes)
        grupo_estadisticas.setLayout(diseno_estadisticas)

        # Botón continuar
        self.boton_continuar = QPushButton("Continuar →")
        self.boton_continuar.setFont(QFont("Arial", 12, QFont.Bold))
        self.boton_continuar.setMinimumHeight(45)
        self.boton_continuar.setStyleSheet("""
            QPushButton {
                background-color: #2980b9;
                color: white;
                border-radius: 6px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #3498db;
            }
            QPushButton:pressed {
                background-color: #1a6fa3;
            }
        """)
        self.boton_continuar.clicked.connect(self._al_continuar)

        # Ensamblar diseño
        diseno_principal.addWidget(etiqueta_titulo)
        diseno_principal.addWidget(etiqueta_subtitulo)
        diseno_principal.addWidget(separador)
        diseno_principal.addWidget(grupo_nota)
        diseno_principal.addWidget(grupo_soat)
        diseno_principal.addWidget(grupo_estadisticas)
        diseno_principal.addStretch()
        diseno_principal.addWidget(self.boton_continuar)

        self.setLayout(diseno_principal)

    def _al_continuar(self):
        """Valida la selección y navega a la siguiente vista."""
        indice = self.combo_tipo_nota.currentIndex()
        if indice == 0:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(
                self,
                "Campo requerido",
                "Por favor seleccione el tipo de nota antes de continuar."
            )
            return

        tipo_nota = self.combo_tipo_nota.currentText()
        es_soat = self.checkbox_soat.isChecked()

        self.controlador_app.controlador_nota.iniciar_nueva_nota(tipo_nota)
        self.controlador_app.controlador_nota.nota_actual.es_soat = es_soat

        if self.controlador_app.ventana_principal:
            self.controlador_app.ventana_principal.navegar_a_formulario_paciente()

    def actualizar_estadisticas(self):
        """Actualiza las estadísticas mostradas en pantalla."""
        resumen = self.controlador_app.obtener_resumen_estadisticas()
        self.etiqueta_notas_hoy.setText(
            f"Notas generadas hoy: {resumen.get('notas_hoy', 0)}"
        )
        self.etiqueta_notas_mes.setText(
            f"Notas este mes: {resumen.get('notas_este_mes', 0)}"
        )

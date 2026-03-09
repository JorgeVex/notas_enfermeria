"""
Módulo: vista_resumen.py
Descripción: Vista final donde se muestra el texto generado de la nota clínica,
             se permite copiar al portapapeles y exportar como archivo .txt.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTextEdit, QPushButton, QGroupBox, QCheckBox,
    QComboBox, QFrame, QMessageBox, QFileDialog,
    QRadioButton, QButtonGroup
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QClipboard
from PyQt5.QtWidgets import QApplication
from modelos.nota import NotaClinica


class _AreaNotaProtegida(QTextEdit):
    """QTextEdit que bloquea toda selección de texto — solo lectura visual."""

    def mousePressEvent(self, event):
        """Ignorar clics para no iniciar selección."""
        pass

    def mouseDoubleClickEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        pass

    def keyPressEvent(self, event):
        """Bloquear Ctrl+A y cualquier otra tecla que seleccione."""
        from PyQt5.QtCore import Qt
        if event.key() in (Qt.Key_A, Qt.Key_C) and event.modifiers() & Qt.ControlModifier:
            return  # bloquear Ctrl+A y Ctrl+C directo sobre el widget
        pass  # ignorar todo lo demás


class VistaResumen(QWidget):
    """
    Pantalla final del flujo. Muestra la nota clínica generada,
    permite configurar el egreso, copiar al portapapeles y exportar.
    """

    def __init__(self, controlador_app):
        super().__init__()
        self.controlador_app = controlador_app
        self._construir_interfaz()

    def _construir_interfaz(self):
        """Construye todos los componentes visuales de la vista."""
        diseno_principal = QVBoxLayout()
        diseno_principal.setSpacing(12)
        diseno_principal.setContentsMargins(30, 25, 30, 25)

        etiqueta_titulo = QLabel("Nota Clínica Generada")
        etiqueta_titulo.setFont(QFont("Arial", 16, QFont.Bold))
        etiqueta_titulo.setStyleSheet("color: #2c3e50;")

        separador = QFrame()
        separador.setFrameShape(QFrame.HLine)
        separador.setStyleSheet("color: #bdc3c7;")

        # --- Grupo cierre de nota (egreso u observación) ---
        self.grupo_egreso = QGroupBox("Cierre de la nota")
        self.grupo_egreso.setFont(QFont("Arial", 10, QFont.Bold))
        diseno_egreso = QVBoxLayout()
        diseno_egreso.setSpacing(6)

        # Selector de tipo de cierre
        lbl_cierre = QLabel("¿Cómo finaliza la atención?")
        lbl_cierre.setFont(QFont("Arial", 10))
        self.grupo_tipo_cierre = QButtonGroup()

        self.radio_sin_cierre = QRadioButton("Sin definir")
        self.radio_sin_cierre.setFont(QFont("Arial", 10))
        self.radio_sin_cierre.setChecked(True)
        self.radio_egreso = QRadioButton("Médico ordena egreso")
        self.radio_egreso.setFont(QFont("Arial", 10))
        self.radio_observacion = QRadioButton("Paciente queda en observación (espera revaloración)")
        self.radio_observacion.setFont(QFont("Arial", 10))
        self.radio_observacion.setStyleSheet("color: #8e44ad;")

        self.grupo_tipo_cierre.addButton(self.radio_sin_cierre)
        self.grupo_tipo_cierre.addButton(self.radio_egreso)
        self.grupo_tipo_cierre.addButton(self.radio_observacion)

        diseno_radios_cierre = QHBoxLayout()
        diseno_radios_cierre.addWidget(self.radio_sin_cierre)
        diseno_radios_cierre.addWidget(self.radio_egreso)
        diseno_radios_cierre.addWidget(self.radio_observacion)
        diseno_radios_cierre.addStretch()

        # Panel egreso (visible solo si radio_egreso)
        self.panel_egreso = QWidget()
        self.panel_egreso.setVisible(False)
        diseno_panel_egreso = QVBoxLayout()
        diseno_panel_egreso.setContentsMargins(8, 4, 0, 0)
        diseno_panel_egreso.setSpacing(4)

        self.check_recomendaciones = QCheckBox("Se entregan recomendaciones al paciente")
        self.check_recomendaciones.setFont(QFont("Arial", 10))
        self.check_signos_alarma = QCheckBox("Se explican signos de alarma")
        self.check_signos_alarma.setFont(QFont("Arial", 10))

        lbl_modo_salida = QLabel("Modo de salida:")
        lbl_modo_salida.setFont(QFont("Arial", 10))
        self.grupo_modo_salida = QButtonGroup()
        diseno_modo_salida = QHBoxLayout()
        for modo in NotaClinica.MODOS_SALIDA:
            radio = QRadioButton(modo.replace("EN ", "").capitalize())
            radio.setFont(QFont("Arial", 10))
            radio.setProperty("valor_real", modo)
            self.grupo_modo_salida.addButton(radio)
            diseno_modo_salida.addWidget(radio)
        diseno_modo_salida.addStretch()

        lbl_estado_egreso = QLabel("Estado al egreso:")
        lbl_estado_egreso.setFont(QFont("Arial", 10))
        self.combo_estado_egreso = QComboBox()
        self.combo_estado_egreso.setFont(QFont("Arial", 10))
        self.combo_estado_egreso.addItems(["ESTABLES", "MEJORÍA", "REGULARES"])

        diseno_panel_egreso.addWidget(self.check_recomendaciones)
        diseno_panel_egreso.addWidget(self.check_signos_alarma)
        diseno_panel_egreso.addWidget(lbl_modo_salida)
        diseno_panel_egreso.addLayout(diseno_modo_salida)
        diseno_panel_egreso.addWidget(lbl_estado_egreso)
        diseno_panel_egreso.addWidget(self.combo_estado_egreso)
        self.panel_egreso.setLayout(diseno_panel_egreso)

        # Conectar radios al panel
        self.radio_egreso.toggled.connect(
            lambda checked: self.panel_egreso.setVisible(checked)
        )
        self.radio_sin_cierre.toggled.connect(
            lambda checked: self.panel_egreso.setVisible(False) if checked else None
        )

        boton_aplicar_egreso = QPushButton("Aplicar cierre y regenerar nota")
        boton_aplicar_egreso.setFont(QFont("Arial", 10))
        boton_aplicar_egreso.setStyleSheet("""
            QPushButton {
                background-color: #8e44ad; color: white;
                border-radius: 5px; padding: 6px;
            }
            QPushButton:hover { background-color: #9b59b6; }
        """)
        boton_aplicar_egreso.clicked.connect(self._aplicar_egreso)

        diseno_egreso.addWidget(lbl_cierre)
        diseno_egreso.addLayout(diseno_radios_cierre)
        diseno_egreso.addWidget(self.panel_egreso)
        diseno_egreso.addWidget(boton_aplicar_egreso)
        self.grupo_egreso.setLayout(diseno_egreso)

        # --- Área de texto de la nota ---
        grupo_nota = QGroupBox("Texto de la nota clínica")
        grupo_nota.setFont(QFont("Arial", 10, QFont.Bold))
        diseno_nota = QVBoxLayout()

        self.area_nota = _AreaNotaProtegida()
        self.area_nota.setFont(QFont("Courier New", 10))
        self.area_nota.setReadOnly(True)
        self.area_nota.setMinimumHeight(250)
        self.area_nota.setContextMenuPolicy(Qt.NoContextMenu)
        self.area_nota.setStyleSheet("""
            QTextEdit {
                background-color: #fdfefe;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                padding: 8px;
                selection-background-color: transparent;
                color: #2c3e50;
            }
        """)

        diseno_nota.addWidget(self.area_nota)
        grupo_nota.setLayout(diseno_nota)

        # --- Botones de acción ---
        diseno_botones_accion = QHBoxLayout()

        boton_copiar = QPushButton("📋 Copiar al portapapeles")
        boton_copiar.setFont(QFont("Arial", 10, QFont.Bold))
        boton_copiar.setMinimumHeight(40)
        boton_copiar.setStyleSheet("""
            QPushButton {
                background-color: #2980b9; color: white;
                border-radius: 5px; padding: 6px 14px;
            }
            QPushButton:hover { background-color: #3498db; }
        """)
        boton_copiar.clicked.connect(self._copiar_portapapeles)

        boton_exportar = QPushButton("💾 Exportar como .txt")
        boton_exportar.setFont(QFont("Arial", 10, QFont.Bold))
        boton_exportar.setMinimumHeight(40)
        boton_exportar.setStyleSheet("""
            QPushButton {
                background-color: #16a085; color: white;
                border-radius: 5px; padding: 6px 14px;
            }
            QPushButton:hover { background-color: #1abc9c; }
        """)
        boton_exportar.clicked.connect(self._exportar_txt)

        diseno_botones_accion.addWidget(boton_copiar)
        diseno_botones_accion.addWidget(boton_exportar)

        # --- Botones de navegación ---
        diseno_nav = QHBoxLayout()

        boton_atras = QPushButton("← Volver a procedimientos")
        boton_atras.setFont(QFont("Arial", 10))
        boton_atras.setMinimumHeight(38)
        boton_atras.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6; color: white;
                border-radius: 5px; padding: 6px 14px;
            }
            QPushButton:hover { background-color: #7f8c8d; }
        """)
        boton_atras.clicked.connect(self._al_ir_atras)

        boton_nueva_nota = QPushButton("✚ Nueva nota")
        boton_nueva_nota.setFont(QFont("Arial", 10, QFont.Bold))
        boton_nueva_nota.setMinimumHeight(38)
        boton_nueva_nota.setStyleSheet("""
            QPushButton {
                background-color: #e67e22; color: white;
                border-radius: 5px; padding: 6px 14px;
            }
            QPushButton:hover { background-color: #f39c12; }
        """)
        boton_nueva_nota.clicked.connect(self._nueva_nota)

        diseno_nav.addWidget(boton_atras)
        diseno_nav.addStretch()
        diseno_nav.addWidget(boton_nueva_nota)

        # Ensamblar
        diseno_principal.addWidget(etiqueta_titulo)
        diseno_principal.addWidget(separador)
        diseno_principal.addWidget(self.grupo_egreso)
        diseno_principal.addWidget(grupo_nota)
        diseno_principal.addLayout(diseno_botones_accion)
        diseno_principal.addLayout(diseno_nav)

        self.setLayout(diseno_principal)

    def cargar_nota(self):
        """Genera y muestra el texto de la nota clínica en el área de texto."""
        controlador = self.controlador_app.controlador_nota
        texto = controlador.generar_texto_nota()
        self.area_nota.setPlainText(texto)

    def _aplicar_egreso(self):
        """Aplica el cierre (egreso u observación) y regenera la nota."""
        controlador = self.controlador_app.controlador_nota

        if self.radio_egreso.isChecked():
            boton_modo = self.grupo_modo_salida.checkedButton()
            modo_salida = boton_modo.property("valor_real") if boton_modo else ""
            controlador.establecer_datos_egreso(
                medico_ordena=True,
                recomendaciones=self.check_recomendaciones.isChecked(),
                signos_alarma=self.check_signos_alarma.isChecked(),
                modo_salida=modo_salida,
                estado_egreso=self.combo_estado_egreso.currentText(),
            )
            controlador.nota_actual.queda_en_observacion = False

        elif self.radio_observacion.isChecked():
            # Limpiar datos de egreso, activar observación
            controlador.establecer_datos_egreso(
                medico_ordena=False,
                recomendaciones=False,
                signos_alarma=False,
                modo_salida="",
                estado_egreso="",
            )
            controlador.nota_actual.queda_en_observacion = True

        else:
            # Sin definir: limpiar ambos
            controlador.establecer_datos_egreso(
                medico_ordena=False,
                recomendaciones=False,
                signos_alarma=False,
                modo_salida="",
                estado_egreso="",
            )
            controlador.nota_actual.queda_en_observacion = False

        texto = controlador.generar_texto_nota()
        self.area_nota.setPlainText(texto)

    def _copiar_portapapeles(self):
        """Copia el texto al portapapeles y registra la estadística de uso."""
        texto = self.area_nota.toPlainText()
        if not texto.strip():
            QMessageBox.warning(self, "Sin contenido", "No hay texto para copiar.")
            return
        QApplication.clipboard().setText(texto)

        # Registrar estadística solo en este momento
        controlador = self.controlador_app.controlador_nota
        if controlador.nota_actual:
            self.controlador_app.servicio_estadisticas.registrar_nota(
                tipo_nota=controlador.nota_actual.tipo,
                tipos_procedimiento=controlador.nota_actual.obtener_tipos_procedimiento(),
            )

        QMessageBox.information(
            self, "Copiado",
            "La nota ha sido copiada al portapapeles.\n"
            "Puede pegarla directamente en el sistema de la IPS."
        )

    def _exportar_txt(self):
        """Exporta la nota a un archivo .txt en la ubicación elegida por el usuario."""
        texto = self.area_nota.toPlainText()
        if not texto.strip():
            QMessageBox.warning(self, "Sin contenido", "No hay texto para exportar.")
            return

        ruta, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar nota clínica",
            "",
            "Archivos de texto (*.txt)"
        )

        if ruta:
            controlador = self.controlador_app.controlador_nota
            controlador.nota_actual.texto_final = texto
            # Exportar sin registrar estadística (el conteo se hace al copiar)
            ruta_final = self.controlador_app.controlador_nota.exportador.exportar(
                texto_nota=texto,
                tipo_nota=controlador.nota_actual.tipo,
                ruta_personalizada=ruta,
            )
            QMessageBox.information(
                self, "Exportado correctamente",
                f"Nota guardada en:\n{ruta_final}"
            )

    def _nueva_nota(self):
        """Reinicia la aplicación y limpia todos los campos para una nueva nota."""
        respuesta = QMessageBox.question(
            self, "Nueva nota",
            "¿Desea iniciar una nueva nota? Se perderán los datos actuales.",
            QMessageBox.Yes | QMessageBox.No
        )
        if respuesta == QMessageBox.Yes:
            self.controlador_app.reiniciar()
            ventana = self.controlador_app.ventana_principal
            if ventana:
                # Limpiar campos de todas las vistas (incluye rev, entrega, recibo)
                ventana.limpiar_todas_las_vistas()
                self.area_nota.clear()
                self.radio_sin_cierre.setChecked(True)
                self.panel_egreso.setVisible(False)
                self.check_recomendaciones.setChecked(False)
                self.check_signos_alarma.setChecked(False)
                self.combo_estado_egreso.setCurrentIndex(0)
                for btn in self.grupo_modo_salida.buttons():
                    btn.setAutoExclusive(False)
                    btn.setChecked(False)
                    btn.setAutoExclusive(True)
                ventana.navegar_a_selector()

    def _al_ir_atras(self):
        """Navega de regreso a la vista de procedimientos."""
        if self.controlador_app.ventana_principal:
            self.controlador_app.ventana_principal.navegar_a_procedimientos()

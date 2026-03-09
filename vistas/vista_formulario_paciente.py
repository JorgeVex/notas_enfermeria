"""
Módulo: vista_formulario_paciente.py
Descripción: Vista donde el personal ingresa los datos básicos del paciente:
             sexo, edad, modo de ingreso, motivo de consulta y signos vitales.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QRadioButton, QComboBox, QTextEdit, QPushButton,
    QGroupBox, QButtonGroup, QGridLayout, QFrame, QMessageBox,
    QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from modelos.paciente import Paciente


class VistaFormularioPaciente(QWidget):
    """
    Formulario de datos básicos del paciente.
    Usa radio buttons para sexo y modo de ingreso,
    y campos de texto para edad, motivo y signos vitales.
    """

    def __init__(self, controlador_app):
        super().__init__()
        self.controlador_app = controlador_app
        self._construir_interfaz()

    def _construir_interfaz(self):
        """Construye todos los componentes visuales de la vista."""
        # Layout raíz con scroll
        layout_raiz = QVBoxLayout()
        layout_raiz.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        contenedor = QWidget()
        diseno_principal = QVBoxLayout()
        diseno_principal.setSpacing(15)
        diseno_principal.setContentsMargins(30, 30, 30, 30)

        # Título
        etiqueta_titulo = QLabel("Datos del Paciente")
        etiqueta_titulo.setFont(QFont("Arial", 16, QFont.Bold))
        etiqueta_titulo.setStyleSheet("color: #2c3e50;")

        separador = QFrame()
        separador.setFrameShape(QFrame.HLine)
        separador.setStyleSheet("color: #bdc3c7;")

        # --- Grupo datos demográficos ---
        grupo_demograficos = QGroupBox("Datos demográficos")
        grupo_demograficos.setFont(QFont("Arial", 10, QFont.Bold))
        diseno_demograficos = QGridLayout()

        # Sexo - Radio buttons
        etiqueta_sexo = QLabel("Sexo del paciente:")
        etiqueta_sexo.setFont(QFont("Arial", 10))
        self.radio_masculino = QRadioButton("Masculino")
        self.radio_masculino.setFont(QFont("Arial", 10))
        self.radio_femenino = QRadioButton("Femenino")
        self.radio_femenino.setFont(QFont("Arial", 10))
        self.grupo_sexo = QButtonGroup()
        self.grupo_sexo.addButton(self.radio_masculino)
        self.grupo_sexo.addButton(self.radio_femenino)

        diseno_sexo = QHBoxLayout()
        diseno_sexo.addWidget(self.radio_masculino)
        diseno_sexo.addWidget(self.radio_femenino)
        diseno_sexo.addStretch()

        # Edad
        etiqueta_edad = QLabel("Edad (años):")
        etiqueta_edad.setFont(QFont("Arial", 10))
        self.campo_edad = QLineEdit()
        self.campo_edad.setPlaceholderText("Ej: 35")
        self.campo_edad.setFont(QFont("Arial", 10))
        self.campo_edad.setMaximumWidth(120)
        self.campo_edad.textChanged.connect(self._actualizar_condicion_etaria)

        self.etiqueta_condicion = QLabel("")
        self.etiqueta_condicion.setFont(QFont("Arial", 9))
        self.etiqueta_condicion.setStyleSheet("color: #27ae60; font-style: italic;")

        diseno_demograficos.addWidget(etiqueta_sexo, 0, 0)
        diseno_demograficos.addLayout(diseno_sexo, 0, 1)
        diseno_demograficos.addWidget(etiqueta_edad, 1, 0)

        diseno_edad = QHBoxLayout()
        diseno_edad.addWidget(self.campo_edad)
        diseno_edad.addWidget(self.etiqueta_condicion)
        diseno_edad.addStretch()
        diseno_demograficos.addLayout(diseno_edad, 1, 1)

        grupo_demograficos.setLayout(diseno_demograficos)

        # --- Grupo modo de ingreso ---
        self.grupo_ingreso_box = QGroupBox("Modo de ingreso")
        self.grupo_ingreso_box.setFont(QFont("Arial", 10, QFont.Bold))
        diseno_ingreso = QHBoxLayout()

        self.grupo_modo_ingreso = QButtonGroup()
        for modo in Paciente.MODOS_INGRESO:
            radio = QRadioButton(modo.replace("EN ", "").capitalize())
            radio.setFont(QFont("Arial", 10))
            radio.setProperty("valor_real", modo)
            self.grupo_modo_ingreso.addButton(radio)
            diseno_ingreso.addWidget(radio)
        diseno_ingreso.addStretch()

        self.grupo_ingreso_box.setLayout(diseno_ingreso)

        # --- Acompañante (visible solo si es menor de edad) ---
        self.grupo_acompanante = QGroupBox("Acompañante (menor de edad)")
        self.grupo_acompanante.setFont(QFont("Arial", 10, QFont.Bold))
        self.grupo_acompanante.setVisible(False)
        diseno_acompanante = QHBoxLayout()

        self.grupo_tipo_acompanante = QButtonGroup()
        for opcion in ["Padre", "Madre", "Acompañante"]:
            radio_ac = QRadioButton(opcion)
            radio_ac.setFont(QFont("Arial", 10))
            self.grupo_tipo_acompanante.addButton(radio_ac)
            diseno_acompanante.addWidget(radio_ac)
        diseno_acompanante.addStretch()
        self.grupo_acompanante.setLayout(diseno_acompanante)

        self.campo_edad.textChanged.connect(self._mostrar_ocultar_acompanante)
        self.campo_edad.textChanged.connect(self._mostrar_ocultar_gestante)
        self.radio_femenino.toggled.connect(self._mostrar_ocultar_gestante)
        self.radio_masculino.toggled.connect(self._mostrar_ocultar_gestante)

        # --- Gestante (solo mujeres >= 13 años) ---
        self.grupo_gestante = QGroupBox("Estado de embarazo")
        self.grupo_gestante.setFont(QFont("Arial", 10, QFont.Bold))
        self.grupo_gestante.setVisible(False)
        diseno_gestante = QHBoxLayout()
        diseno_gestante.setSpacing(12)

        self.grupo_es_gestante = QButtonGroup()
        self.radio_no_gestante = QRadioButton("No gestante")
        self.radio_no_gestante.setFont(QFont("Arial", 10))
        self.radio_no_gestante.setChecked(True)
        self.radio_si_gestante = QRadioButton("Gestante")
        self.radio_si_gestante.setFont(QFont("Arial", 10))
        self.grupo_es_gestante.addButton(self.radio_no_gestante)
        self.grupo_es_gestante.addButton(self.radio_si_gestante)

        lbl_semanas = QLabel("Semanas de gestación:")
        lbl_semanas.setFont(QFont("Arial", 10))
        lbl_semanas.setVisible(False)
        self._lbl_semanas_gestante = lbl_semanas

        self.campo_semanas_gestante = QLineEdit()
        self.campo_semanas_gestante.setFont(QFont("Arial", 10))
        self.campo_semanas_gestante.setPlaceholderText("Ej: 38 (obligatorio)")
        self.campo_semanas_gestante.setMaximumWidth(150)
        self.campo_semanas_gestante.setVisible(False)
        self.campo_semanas_gestante.setStyleSheet(
            "border: 1px solid #e74c3c;"  # borde rojo para indicar obligatorio
        )

        def _al_cambiar_semanas(texto):
            # Verde cuando tiene valor, rojo cuando vacío
            if texto.strip():
                self.campo_semanas_gestante.setStyleSheet(
                    "border: 1px solid #27ae60;"
                )
            else:
                self.campo_semanas_gestante.setStyleSheet(
                    "border: 1px solid #e74c3c;"
                )
        self.campo_semanas_gestante.textChanged.connect(_al_cambiar_semanas)

        def _mostrar_semanas(checked):
            self.campo_semanas_gestante.setVisible(checked)
            self._lbl_semanas_gestante.setVisible(checked)
            if not checked:
                self.campo_semanas_gestante.clear()

        self.radio_si_gestante.toggled.connect(_mostrar_semanas)

        diseno_gestante.addWidget(self.radio_no_gestante)
        diseno_gestante.addWidget(self.radio_si_gestante)
        diseno_gestante.addWidget(self._lbl_semanas_gestante)
        diseno_gestante.addWidget(self.campo_semanas_gestante)
        diseno_gestante.addStretch()
        self.grupo_gestante.setLayout(diseno_gestante)

        # --- Grupo motivo de consulta ---
        grupo_motivo = QGroupBox("Motivo de consulta")
        grupo_motivo.setFont(QFont("Arial", 10, QFont.Bold))
        diseno_motivo = QVBoxLayout()

        etiqueta_motivo = QLabel("Escriba lo que refiere el paciente:")
        etiqueta_motivo.setFont(QFont("Arial", 10))
        self.campo_motivo = QTextEdit()
        self.campo_motivo.setFont(QFont("Arial", 10))
        self.campo_motivo.setMaximumHeight(80)
        self.campo_motivo.setPlaceholderText(
            'Ej: "Tengo mucho dolor de cabeza, náuseas y vómitos"'
        )

        diseno_motivo.addWidget(etiqueta_motivo)
        diseno_motivo.addWidget(self.campo_motivo)
        grupo_motivo.setLayout(diseno_motivo)

        # --- Grupo signos vitales ---
        self.grupo_signos_box = QGroupBox("Signos vitales")
        self.grupo_signos_box.setFont(QFont("Arial", 10, QFont.Bold))
        diseno_signos_outer = QVBoxLayout()
        diseno_signos_outer.setSpacing(6)

        # Radio para revaloración (oculto por defecto, visible al activar_modo_revaloracion)
        self._row_radio_signos = QWidget()
        row_rs = QHBoxLayout(); row_rs.setContentsMargins(0, 0, 0, 0)
        lbl_rs = QLabel("¿Agregar nuevos signos vitales?")
        lbl_rs.setFont(QFont("Arial", 9)); lbl_rs.setStyleSheet("color:#7f8c8d; font-style:italic;")
        self._radio_signos_no = QRadioButton("No"); self._radio_signos_no.setFont(QFont("Arial", 9))
        self._radio_signos_si = QRadioButton("Sí"); self._radio_signos_si.setFont(QFont("Arial", 9))
        self._radio_signos_no.setChecked(True)
        self._grupo_radio_signos = QButtonGroup()
        self._grupo_radio_signos.addButton(self._radio_signos_no)
        self._grupo_radio_signos.addButton(self._radio_signos_si)
        row_rs.addWidget(lbl_rs); row_rs.addWidget(self._radio_signos_no)
        row_rs.addWidget(self._radio_signos_si); row_rs.addStretch()
        self._row_radio_signos.setLayout(row_rs)
        self._row_radio_signos.setVisible(False)  # solo visible en revaloración

        # Panel de campos de signos (deshabilitado cuando se oculta el radio)
        self._panel_campos_signos = QWidget()
        diseno_signos = QGridLayout(); diseno_signos.setSpacing(10)
        campos_signos = [
            ("Tensión arterial (mmHg):", "campo_ta", "Ej: 120/80"),
            ("Frecuencia cardíaca (lpm):", "campo_fc", "Ej: 72"),
            ("Frecuencia respiratoria (rpm):", "campo_fr", "Ej: 18"),
            ("Temperatura (°C):", "campo_temp", "Ej: 36.5"),
            ("Saturación O₂ (%):", "campo_spo2", "Ej: 98"),
            ("Talla (cm):", "campo_talla", "Ej: 170"),
            ("Peso (kg):", "campo_peso", "Ej: 65"),
        ]
        for fila, (etiqueta, nombre_campo, placeholder) in enumerate(campos_signos):
            lbl = QLabel(etiqueta); lbl.setFont(QFont("Arial", 9))
            campo = QLineEdit(); campo.setFont(QFont("Arial", 9))
            campo.setPlaceholderText(placeholder); campo.setMaximumWidth(150)
            setattr(self, nombre_campo, campo)
            diseno_signos.addWidget(lbl, fila // 2, (fila % 2) * 2)
            diseno_signos.addWidget(campo, fila // 2, (fila % 2) * 2 + 1)
        self._panel_campos_signos.setLayout(diseno_signos)

        # Conectar radio para habilitar/deshabilitar campos
        def _toggle_campos_signos(checked):
            self._panel_campos_signos.setEnabled(checked)
            self._panel_campos_signos.setStyleSheet(
                "" if checked else "background:#f0f0f0; border-radius:4px;"
            )
        self._radio_signos_si.toggled.connect(_toggle_campos_signos)

        diseno_signos_outer.addWidget(self._row_radio_signos)
        diseno_signos_outer.addWidget(self._panel_campos_signos)
        self.grupo_signos_box.setLayout(diseno_signos_outer)

        # --- Médico de turno ---
        grupo_medico = QGroupBox("Médico de turno")
        grupo_medico.setFont(QFont("Arial", 10, QFont.Bold))
        diseno_medico = QHBoxLayout()

        etiqueta_medico = QLabel("Nombre del médico:")
        etiqueta_medico.setFont(QFont("Arial", 10))
        self.campo_medico = QLineEdit()
        self.campo_medico.setFont(QFont("Arial", 10))
        self.campo_medico.setPlaceholderText("Ej: Juan Pérez")

        diseno_medico.addWidget(etiqueta_medico)
        diseno_medico.addWidget(self.campo_medico)
        grupo_medico.setLayout(diseno_medico)

        # --- Botones de navegación ---
        diseno_botones = QHBoxLayout()
        self.boton_atras = QPushButton("← Atrás")
        self.boton_atras.setFont(QFont("Arial", 10))
        self.boton_atras.setMinimumHeight(40)
        self.boton_atras.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border-radius: 5px;
                padding: 6px 16px;
            }
            QPushButton:hover { background-color: #7f8c8d; }
        """)
        self.boton_atras.clicked.connect(self._al_ir_atras)

        self.boton_continuar = QPushButton("Continuar →")
        self.boton_continuar.setFont(QFont("Arial", 10, QFont.Bold))
        self.boton_continuar.setMinimumHeight(40)
        self.boton_continuar.setStyleSheet("""
            QPushButton {
                background-color: #2980b9;
                color: white;
                border-radius: 5px;
                padding: 6px 16px;
            }
            QPushButton:hover { background-color: #3498db; }
        """)
        self.boton_continuar.clicked.connect(self._al_continuar)

        diseno_botones.addWidget(self.boton_atras)
        diseno_botones.addStretch()
        diseno_botones.addWidget(self.boton_continuar)

        # Ensamblar diseño principal
        diseno_principal.addWidget(etiqueta_titulo)
        diseno_principal.addWidget(separador)
        diseno_principal.addWidget(grupo_demograficos)
        diseno_principal.addWidget(self.grupo_ingreso_box)
        diseno_principal.addWidget(self.grupo_acompanante)
        diseno_principal.addWidget(self.grupo_gestante)
        diseno_principal.addWidget(grupo_motivo)
        diseno_principal.addWidget(self.grupo_signos_box)
        diseno_principal.addWidget(grupo_medico)
        diseno_principal.addStretch()
        diseno_principal.addLayout(diseno_botones)

        contenedor.setLayout(diseno_principal)
        scroll.setWidget(contenedor)
        layout_raiz.addWidget(scroll)
        self.setLayout(layout_raiz)

    def _actualizar_condicion_etaria(self, texto):
        """Muestra automáticamente la condición etaria según la edad."""
        try:
            edad = int(texto.strip())
            if edad < 18:
                self.etiqueta_condicion.setText("← Menor de edad")
                self.etiqueta_condicion.setStyleSheet(
                    "color: #e67e22; font-style: italic;"
                )
            else:
                self.etiqueta_condicion.setText("← Mayor de edad")
                self.etiqueta_condicion.setStyleSheet(
                    "color: #27ae60; font-style: italic;"
                )
        except ValueError:
            self.etiqueta_condicion.setText("")

    def _mostrar_ocultar_acompanante(self, texto):
        """Muestra u oculta el grupo de acompañante según la edad."""
        try:
            edad = int(texto.strip())
            self.grupo_acompanante.setVisible(edad < 18)
        except ValueError:
            self.grupo_acompanante.setVisible(False)

    def activar_modo_revaloracion(self):
        """
        Llamar cuando el tipo de nota es REVALORACIÓN.
        - Deshabilita modo de ingreso (en gris)
        - Muestra radio de signos vitales y deshabilita campos por defecto
        - El título del grupo de signos cambia a indicar que son opcionales
        """
        # Modo de ingreso: deshabilitar completamente (en gris)
        self.grupo_ingreso_box.setEnabled(False)
        self.grupo_ingreso_box.setStyleSheet(
            "QGroupBox { background: #ecf0f1; color: #95a5a6; }"
            "QGroupBox::title { color: #95a5a6; }"
            "QRadioButton { color: #95a5a6; }"
        )
        self.grupo_ingreso_box.setTitle("Modo de ingreso (no aplica en revaloración)")

        # Signos vitales: mostrar radio, deshabilitar campos
        self._row_radio_signos.setVisible(True)
        self._radio_signos_no.setChecked(True)
        self._panel_campos_signos.setEnabled(False)
        self._panel_campos_signos.setStyleSheet("background:#f0f0f0; border-radius:4px;")
        self.grupo_signos_box.setTitle("Signos vitales (deshabilitados — activar si se toman nuevos)")

    def desactivar_modo_revaloracion(self):
        """
        Llamar cuando el tipo de nota NO es revaloración.
        Restaura modo de ingreso y signos vitales a su estado normal.
        """
        self.grupo_ingreso_box.setEnabled(True)
        self.grupo_ingreso_box.setStyleSheet("")
        self.grupo_ingreso_box.setTitle("Modo de ingreso")

        self._row_radio_signos.setVisible(False)
        self._panel_campos_signos.setEnabled(True)
        self._panel_campos_signos.setStyleSheet("")
        self.grupo_signos_box.setTitle("Signos vitales")

    def _mostrar_ocultar_gestante(self, *args):
        """Muestra el campo gestante solo si es mujer >= 13 años."""
        try:
            edad = int(self.campo_edad.text().strip())
            es_femenino = self.radio_femenino.isChecked()
            mostrar = es_femenino and edad >= 13
            self.grupo_gestante.setVisible(mostrar)
            if not mostrar:
                self.radio_no_gestante.setChecked(True)
                self.campo_semanas_gestante.clear()
                self.campo_semanas_gestante.setVisible(False)
        except ValueError:
            self.grupo_gestante.setVisible(False)

    def _obtener_sexo_seleccionado(self) -> str:
        """Retorna el sexo seleccionado como constante del modelo."""
        if self.radio_masculino.isChecked():
            return Paciente.SEXO_MASCULINO
        elif self.radio_femenino.isChecked():
            return Paciente.SEXO_FEMENINO
        return ""

    def _obtener_modo_ingreso(self) -> str:
        """Retorna el modo de ingreso seleccionado."""
        boton = self.grupo_modo_ingreso.checkedButton()
        if boton:
            return boton.property("valor_real")
        return ""

    def _obtener_acompanante(self) -> str:
        """Retorna el tipo de acompañante si aplica."""
        boton = self.grupo_tipo_acompanante.checkedButton()
        if boton:
            return boton.text()
        return ""

    def _al_continuar(self):
        """Valida campos y avanza a la vista de procedimientos."""
        sexo = self._obtener_sexo_seleccionado()
        edad_texto = self.campo_edad.text().strip()
        modo_ingreso = self._obtener_modo_ingreso()
        medico = self.campo_medico.text().strip()

        errores = []
        if not sexo:
            errores.append("Seleccione el sexo del paciente.")
        if not edad_texto or not edad_texto.isdigit():
            errores.append("Ingrese una edad válida.")
        if not modo_ingreso:
            errores.append("Seleccione el modo de ingreso.")

        # Validar semanas de gestación si es gestante
        es_gestante_marcada = (
            self.radio_si_gestante.isChecked()
            and self.grupo_gestante.isVisible()
        )
        if es_gestante_marcada and not self.campo_semanas_gestante.text().strip():
            errores.append("Ingrese las semanas de gestación (obligatorio para paciente gestante).")

        if errores:
            QMessageBox.warning(self, "Campos requeridos", "\n".join(errores))
            return

        controlador = self.controlador_app.controlador_nota
        es_gestante = (
            self.radio_si_gestante.isChecked()
            and self.grupo_gestante.isVisible()
        )
        semanas_gestante = (
            self.campo_semanas_gestante.text().strip()
            if es_gestante else ""
        )
        controlador.establecer_datos_paciente(
            sexo=sexo,
            edad=int(edad_texto),
            modo_ingreso=modo_ingreso,
            motivo_consulta=self.campo_motivo.toPlainText().strip(),
            acompanante=self._obtener_acompanante(),
        )
        # Gestante
        controlador.nota_actual.paciente.es_gestante = es_gestante
        controlador.nota_actual.paciente.semanas_gestacion = semanas_gestante
        # Solo registrar signos si están habilitados
        # (en revaloración: solo si el radio "Sí" está marcado)
        signos_habilitados = (
            not self._row_radio_signos.isVisible()  # modo normal: siempre
            or self._radio_signos_si.isChecked()    # revaloración: solo si eligió Sí
        )
        if signos_habilitados:
            controlador.establecer_signos_vitales(
                ta=self.campo_ta.text().strip(),
                fc=self.campo_fc.text().strip(),
                fr=self.campo_fr.text().strip(),
                temp=self.campo_temp.text().strip(),
                spo2=self.campo_spo2.text().strip(),
                talla=self.campo_talla.text().strip(),
                peso=self.campo_peso.text().strip(),
            )
        # Informar a la nota si se agregaron signos en revaloración
        if self._row_radio_signos.isVisible():
            controlador.nota_actual.revaloracion_agregar_signos = self._radio_signos_si.isChecked()
        if medico:
            controlador.establecer_medico(medico)

        if self.controlador_app.ventana_principal:
            self.controlador_app.ventana_principal.navegar_a_procedimientos()

    def _al_ir_atras(self):
        """Navega de regreso al selector de nota."""
        if self.controlador_app.ventana_principal:
            self.controlador_app.ventana_principal.navegar_a_selector()

    def _limpiar_campos(self):
        """Limpia todos los campos del formulario para una nueva nota."""
        # Sexo
        for btn in self.grupo_sexo.buttons():
            btn.setAutoExclusive(False)
            btn.setChecked(False)
            btn.setAutoExclusive(True)
        # Edad
        self.campo_edad.clear()
        self.etiqueta_condicion.setText("")
        # Modo ingreso
        for btn in self.grupo_modo_ingreso.buttons():
            btn.setAutoExclusive(False)
            btn.setChecked(False)
            btn.setAutoExclusive(True)
        # Acompañante
        for btn in self.grupo_tipo_acompanante.buttons():
            btn.setAutoExclusive(False)
            btn.setChecked(False)
            btn.setAutoExclusive(True)
        self.grupo_acompanante.setVisible(False)
        # Motivo consulta
        self.campo_motivo.clear()
        # Signos vitales
        self.campo_ta.clear()
        self.campo_fc.clear()
        self.campo_fr.clear()
        self.campo_temp.clear()
        self.campo_spo2.clear()
        self.campo_talla.clear()
        self.campo_peso.clear()
        # Restaurar modo normal (desactivar cualquier estado de revaloración)
        self.desactivar_modo_revaloracion()
        # Gestante
        self.grupo_gestante.setVisible(False)
        self.radio_no_gestante.setChecked(True)
        self.campo_semanas_gestante.clear()
        self.campo_semanas_gestante.setVisible(False)
        self._lbl_semanas_gestante.setVisible(False)
        # Médico
        self.campo_medico.clear()

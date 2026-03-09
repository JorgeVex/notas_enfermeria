"""
Módulo: vista_turno.py
Descripción: Vistas para nota de entrega de turno y nota de recibo de turno.
             Comparten la misma lógica de malestar y auxiliares.
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QRadioButton, QComboBox, QPushButton, QGroupBox,
    QButtonGroup, QScrollArea, QFrame, QCheckBox, QGridLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

MEDICAMENTOS_TURNO = [
    "ACETAMINOFÉN", "IBUPROFENO", "DICLOFENACO", "TRAMADOL",
    "METOCLOPRAMIDA", "ONDANSETRÓN", "OMEPRAZOL", "SALBUTAMOL",
    "MORFINA", "DIPIRONA", "BUSCAPINA", "DEXAMETASONA",
    "HIDROCORTISONA", "RANITIDINA", "FUROSEMIDA",
]
PRESENTACIONES_TURNO = ["AMPOLLA", "TABLETA", "CÁPSULA", "JARABE", "FRASCO"]
VIAS_TURNO = ["INTRAVENOSA", "INTRAMUSCULAR", "ORAL", "SUBLINGUAL", "INHALATORIA"]

LABS_TURNO = [
    "CUADRO HEMÁTICO (CH)", "PARCIAL DE ORINA (PO)", "GLUCOMETRÍA",
    "CREATININA", "BILIRRUBINA TOTAL", "PCR", "GASES ARTERIALES",
    "AST / ALT", "SODIO / POTASIO",
]

OPCIONES_ORDEN_MEDICO = [
    ("MEDICAMENTO", "Aplicar medicamento"),
    ("EKG", "Tomar electrocardiograma"),
    ("LABORATORIO", "Tomar laboratorios"),
    ("PROCEDIMIENTO", "Otro procedimiento"),
]


class _VistaTurnoBase(QWidget):
    """Base común para entrega y recibo de turno."""

    TITULO = ""
    VERBO_ACCION = ""      # "ENTREGO" o "RECIBO"
    CAMPO_ENTREGA = ""     # nombre del campo en nota para auxiliar que entrega
    CAMPO_RECIBE = ""      # nombre del campo en nota para auxiliar que recibe

    def __init__(self, controlador_app):
        super().__init__()
        self.controlador_app = controlador_app
        self._construir_interfaz()

    def _construir_interfaz(self):
        layout_raiz = QVBoxLayout()
        layout_raiz.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        contenedor = QWidget()
        lay = QVBoxLayout()
        lay.setSpacing(12)
        lay.setContentsMargins(25, 20, 25, 20)

        titulo = QLabel(self.TITULO)
        titulo.setFont(QFont("Arial", 15, QFont.Bold))
        titulo.setStyleSheet("color: #2c3e50;")
        sep = QFrame(); sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("color: #bdc3c7;")

        lay.addWidget(titulo)
        lay.addWidget(sep)
        lay.addWidget(self._grupo_malestar())
        lay.addWidget(self._grupo_auxiliares())
        lay.addStretch()
        lay.addLayout(self._botones())

        contenedor.setLayout(lay)
        scroll.setWidget(contenedor)
        layout_raiz.addWidget(scroll)
        self.setLayout(layout_raiz)

    def _grupo_malestar(self):
        g = QGroupBox("Estado del paciente durante el turno")
        g.setFont(QFont("Arial", 10, QFont.Bold))
        d = QVBoxLayout(); d.setSpacing(8)

        # Radio malestar
        lbl_m = QLabel("¿El paciente refiere malestar?")
        lbl_m.setFont(QFont("Arial", 10))
        self.grupo_malestar_radio = QButtonGroup()
        self.radio_malestar_no = QRadioButton("No")
        self.radio_malestar_no.setFont(QFont("Arial", 10))
        self.radio_malestar_no.setChecked(True)
        self.radio_malestar_si = QRadioButton("Sí")
        self.radio_malestar_si.setFont(QFont("Arial", 10))
        self.radio_malestar_si.setStyleSheet("color: #e67e22;")
        self.grupo_malestar_radio.addButton(self.radio_malestar_no)
        self.grupo_malestar_radio.addButton(self.radio_malestar_si)
        row_m = QHBoxLayout()
        row_m.addWidget(lbl_m)
        row_m.addWidget(self.radio_malestar_no)
        row_m.addWidget(self.radio_malestar_si)
        row_m.addStretch()

        # Panel de malestar: ¿qué ordenó el médico?
        self.panel_malestar = QWidget(); self.panel_malestar.setVisible(False)
        dm = QVBoxLayout(); dm.setContentsMargins(10, 4, 0, 0); dm.setSpacing(8)

        # Selector de tipo de orden médica
        lbl_tipo_orden = QLabel("¿Qué ordena el médico?")
        lbl_tipo_orden.setFont(QFont("Arial", 10, QFont.Bold))
        row_tipo = QHBoxLayout()
        self.grupo_tipo_orden = QButtonGroup()
        self.radios_tipo_orden = {}
        for valor, texto in OPCIONES_ORDEN_MEDICO:
            rb = QRadioButton(texto); rb.setFont(QFont("Arial", 9))
            rb.setProperty("valor", valor)
            self.grupo_tipo_orden.addButton(rb)
            self.radios_tipo_orden[valor] = rb
            row_tipo.addWidget(rb)
        self.radios_tipo_orden["MEDICAMENTO"].setChecked(True)
        row_tipo.addStretch()

        # Panel medicamento
        self.panel_orden_medicamento = QWidget()
        pm = QHBoxLayout(); pm.setContentsMargins(0, 0, 0, 0); pm.setSpacing(6)
        self.combo_med_malestar = QComboBox()
        self.combo_med_malestar.setEditable(True)
        self.combo_med_malestar.addItems(MEDICAMENTOS_TURNO)
        self.combo_med_malestar.setFont(QFont("Arial", 9))
        self.combo_med_malestar.setMinimumWidth(175)
        self.campo_cant_malestar = QLineEdit()
        self.campo_cant_malestar.setPlaceholderText("Cant.")
        self.campo_cant_malestar.setMaximumWidth(50)
        self.campo_cant_malestar.setFont(QFont("Arial", 9))
        self.combo_pres_malestar = QComboBox()
        self.combo_pres_malestar.addItems(PRESENTACIONES_TURNO)
        self.combo_pres_malestar.setFont(QFont("Arial", 9))
        self.combo_via_malestar = QComboBox()
        self.combo_via_malestar.addItems(VIAS_TURNO)
        self.combo_via_malestar.setFont(QFont("Arial", 9))
        pm.addWidget(self.combo_med_malestar); pm.addWidget(self.campo_cant_malestar)
        pm.addWidget(self.combo_pres_malestar)
        pm.addWidget(QLabel("vía")); pm.addWidget(self.combo_via_malestar)
        pm.addStretch()
        self.panel_orden_medicamento.setLayout(pm)

        # Panel EKG (sin campos extra, es solo texto fijo)
        self.panel_orden_ekg = QWidget()
        pe = QHBoxLayout(); pe.setContentsMargins(0, 0, 0, 0)
        lbl_ekg = QLabel("Se tomará electrocardiograma al paciente.")
        lbl_ekg.setFont(QFont("Arial", 9)); lbl_ekg.setStyleSheet("color:#2980b9;")
        pe.addWidget(lbl_ekg); pe.addStretch()
        self.panel_orden_ekg.setLayout(pe)
        self.panel_orden_ekg.setVisible(False)

        # Panel laboratorios
        self.panel_orden_labs = QWidget()
        pl = QVBoxLayout(); pl.setContentsMargins(0, 0, 0, 0); pl.setSpacing(3)
        lbl_labs_t = QLabel("Laboratorios a tomar:"); lbl_labs_t.setFont(QFont("Arial", 9))
        self.checks_labs_turno = {}
        grid_lt = QGridLayout(); grid_lt.setSpacing(2)
        for i, lab in enumerate(LABS_TURNO):
            cb = QCheckBox(lab); cb.setFont(QFont("Arial", 9))
            self.checks_labs_turno[lab] = cb
            grid_lt.addWidget(cb, i // 3, i % 3)
        pl.addWidget(lbl_labs_t); pl.addLayout(grid_lt)
        self.panel_orden_labs.setLayout(pl)
        self.panel_orden_labs.setVisible(False)

        # Panel procedimiento libre
        self.panel_orden_procedimiento = QWidget()
        pp = QHBoxLayout(); pp.setContentsMargins(0, 0, 0, 0)
        lbl_pr = QLabel("Procedimiento:"); lbl_pr.setFont(QFont("Arial", 9))
        self.campo_procedimiento_turno = QLineEdit()
        self.campo_procedimiento_turno.setFont(QFont("Arial", 9))
        self.campo_procedimiento_turno.setPlaceholderText("Ej: Curación de herida, inmovilización...")
        pp.addWidget(lbl_pr); pp.addWidget(self.campo_procedimiento_turno); pp.addStretch()
        self.panel_orden_procedimiento.setLayout(pp)
        self.panel_orden_procedimiento.setVisible(False)

        # Conectar radios de tipo de orden
        def _al_cambiar_tipo_orden():
            rb = self.grupo_tipo_orden.checkedButton()
            val = rb.property("valor") if rb else "MEDICAMENTO"
            self.panel_orden_medicamento.setVisible(val == "MEDICAMENTO")
            self.panel_orden_ekg.setVisible(val == "EKG")
            self.panel_orden_labs.setVisible(val == "LABORATORIO")
            self.panel_orden_procedimiento.setVisible(val == "PROCEDIMIENTO")
        for rb in self.grupo_tipo_orden.buttons():
            rb.toggled.connect(lambda _: _al_cambiar_tipo_orden())

        self.radio_malestar_si.toggled.connect(
            lambda checked: self.panel_malestar.setVisible(checked)
        )

        dm.addWidget(lbl_tipo_orden)
        dm.addLayout(row_tipo)
        dm.addWidget(self.panel_orden_medicamento)
        dm.addWidget(self.panel_orden_ekg)
        dm.addWidget(self.panel_orden_labs)
        dm.addWidget(self.panel_orden_procedimiento)
        self.panel_malestar.setLayout(dm)

        d.addLayout(row_m)
        d.addWidget(self.panel_malestar)
        g.setLayout(d); return g

    def _grupo_auxiliares(self):
        g = QGroupBox("Auxiliares de enfermería")
        g.setFont(QFont("Arial", 10, QFont.Bold))
        d = QVBoxLayout(); d.setSpacing(8)

        # Auxiliar que entrega
        row_e = QHBoxLayout()
        lbl_e = QLabel("Auxiliar que ENTREGA el turno:")
        lbl_e.setFont(QFont("Arial", 10))
        self.campo_auxiliar_entrega = QLineEdit()
        self.campo_auxiliar_entrega.setFont(QFont("Arial", 10))
        self.campo_auxiliar_entrega.setPlaceholderText("Nombre completo")
        self.campo_auxiliar_entrega.setMinimumWidth(250)
        row_e.addWidget(lbl_e)
        row_e.addWidget(self.campo_auxiliar_entrega)
        row_e.addStretch()

        # Auxiliar que recibe
        row_r = QHBoxLayout()
        lbl_r = QLabel("Auxiliar que RECIBE el turno:")
        lbl_r.setFont(QFont("Arial", 10))
        self.campo_auxiliar_recibe = QLineEdit()
        self.campo_auxiliar_recibe.setFont(QFont("Arial", 10))
        self.campo_auxiliar_recibe.setPlaceholderText("Nombre completo")
        self.campo_auxiliar_recibe.setMinimumWidth(250)
        row_r.addWidget(lbl_r)
        row_r.addWidget(self.campo_auxiliar_recibe)
        row_r.addStretch()

        d.addLayout(row_e)
        d.addLayout(row_r)
        g.setLayout(d); return g

    def _botones(self):
        row = QHBoxLayout()
        boton_atras = QPushButton("← Volver")
        boton_atras.setFont(QFont("Arial", 10))
        boton_atras.setMinimumHeight(36)
        boton_atras.setStyleSheet("""
            QPushButton { background:#95a5a6; color:white; border-radius:5px; padding:6px 14px; }
            QPushButton:hover { background:#7f8c8d; }
        """)
        boton_atras.clicked.connect(self._al_ir_atras)

        boton_generar = QPushButton("Generar nota →")
        boton_generar.setFont(QFont("Arial", 10, QFont.Bold))
        boton_generar.setMinimumHeight(36)
        boton_generar.setStyleSheet("""
            QPushButton { background:#27ae60; color:white; border-radius:5px; padding:6px 14px; }
            QPushButton:hover { background:#2ecc71; }
        """)
        boton_generar.clicked.connect(self._al_generar)

        row.addWidget(boton_atras); row.addStretch(); row.addWidget(boton_generar)
        return row

    def _al_ir_atras(self):
        if self.controlador_app.ventana_principal:
            self.controlador_app.ventana_principal.navegar_a_paciente()

    def _al_generar(self):
        nota = self.controlador_app.controlador_nota.nota_actual
        if not nota:
            return
        self._guardar_en_nota(nota)
        if self.controlador_app.ventana_principal:
            self.controlador_app.ventana_principal.navegar_a_resumen()

    def _guardar_en_nota(self, nota):
        """Implementar en cada subclase."""
        raise NotImplementedError

    def limpiar_campos(self):
        self.radio_malestar_no.setChecked(True)
        self.panel_malestar.setVisible(False)
        self.radios_tipo_orden["MEDICAMENTO"].setChecked(True)
        self.combo_med_malestar.setCurrentIndex(0)
        self.campo_cant_malestar.clear()
        self.combo_pres_malestar.setCurrentIndex(0)
        self.combo_via_malestar.setCurrentIndex(0)
        for cb in self.checks_labs_turno.values():
            cb.setChecked(False)
        self.campo_procedimiento_turno.clear()
        self.campo_auxiliar_entrega.clear()
        self.campo_auxiliar_recibe.clear()


class VistaEntregaTurno(_VistaTurnoBase):
    """Vista específica para nota de entrega de turno."""

    TITULO = "Entrega de Turno"

    def _guardar_en_nota(self, nota):
        nota.entrega_refiere_malestar = self.radio_malestar_si.isChecked()
        if nota.entrega_refiere_malestar:
            rb = self.grupo_tipo_orden.checkedButton()
            nota.entrega_tipo_orden = rb.property("valor") if rb else "MEDICAMENTO"
            nota.entrega_medicamento_malestar = self.combo_med_malestar.currentText().strip()
            nota.entrega_cantidad_malestar = self.campo_cant_malestar.text().strip()
            nota.entrega_presentacion_malestar = self.combo_pres_malestar.currentText()
            nota.entrega_via_malestar = self.combo_via_malestar.currentText()
            nota.entrega_labs_malestar = [
                lab for lab, cb in self.checks_labs_turno.items() if cb.isChecked()
            ]
            nota.entrega_procedimiento_malestar = self.campo_procedimiento_turno.text().strip()
        nota.entrega_auxiliar_entrega = self.campo_auxiliar_entrega.text().strip()
        nota.entrega_auxiliar_recibe = self.campo_auxiliar_recibe.text().strip()


class VistaReciboTurno(_VistaTurnoBase):
    """Vista específica para nota de recibo de turno."""

    TITULO = "Recibo de Turno"

    def _guardar_en_nota(self, nota):
        nota.recibo_refiere_malestar = self.radio_malestar_si.isChecked()
        if nota.recibo_refiere_malestar:
            rb = self.grupo_tipo_orden.checkedButton()
            nota.recibo_tipo_orden = rb.property("valor") if rb else "MEDICAMENTO"
            nota.recibo_medicamento_malestar = self.combo_med_malestar.currentText().strip()
            nota.recibo_cantidad_malestar = self.campo_cant_malestar.text().strip()
            nota.recibo_presentacion_malestar = self.combo_pres_malestar.currentText()
            nota.recibo_via_malestar = self.combo_via_malestar.currentText()
            nota.recibo_labs_malestar = [
                lab for lab, cb in self.checks_labs_turno.items() if cb.isChecked()
            ]
            nota.recibo_procedimiento_malestar = self.campo_procedimiento_turno.text().strip()
        nota.recibo_auxiliar_entrega = self.campo_auxiliar_entrega.text().strip()
        nota.recibo_auxiliar_recibe = self.campo_auxiliar_recibe.text().strip()

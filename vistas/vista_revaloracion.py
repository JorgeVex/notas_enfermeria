"""
Módulo: vista_revaloracion.py
Descripción: Vista específica para la nota de revaloración.
             Permite agregar signos vitales opcionales, complicaciones,
             carro rojo, plan médico, labs revisados y tipo de cierre.
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit,
    QRadioButton, QComboBox, QTextEdit, QPushButton, QGroupBox,
    QButtonGroup, QCheckBox, QScrollArea, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from modelos.procedimiento import Procedimiento
from modelos.medicamento import Medicamento


# Medicamentos comunes en revaloración
MEDICAMENTOS_COMUNES = [
    "ACETAMINOFÉN", "IBUPROFENO", "DICLOFENACO", "TRAMADOL", "MORFINA",
    "METOCLOPRAMIDA", "ONDANSETRÓN", "RANITIDINA", "OMEPRAZOL",
    "METOPROLOL", "ENALAPRIL", "FUROSEMIDA", "HIDRALAZINA",
    "DEXAMETASONA", "HIDROCORTISONA", "METILPREDNISOLONA",
    "AMOXICILINA", "CLINDAMICINA", "CIPROFLOXACINO",
    "SALBUTAMOL", "AMINOFILINA", "ADRENALINA (CARRO ROJO)",
    "ATROPINA (CARRO ROJO)", "LIDOCAÍNA (CARRO ROJO)",
    "AMIODARONA (CARRO ROJO)", "DOPAMINA (CARRO ROJO)",
]

PRESENTACIONES = ["AMPOLLA", "TABLETA", "CÁPSULA", "JARABE", "FRASCO"]
VIAS = ["INTRAVENOSA", "INTRAMUSCULAR", "ORAL", "SUBLINGUAL", "INHALATORIA"]

MANIOBRAS_CARRO = [
    "RCP BÁSICA", "DESFIBRILACIÓN", "INTUBACIÓN OROTRAQUEAL",
    "CARDIOVERSIÓN", "MASAJE CARDÍACO EXTERNO", "VENTILACIÓN CON BOLSA MÁSCARA",
    "ACCESO VENOSO CENTRAL",
]

LABS_DISPONIBLES = [
    "CUADRO HEMÁTICO (CH)", "PARCIAL DE ORINA (PO)", "COPROLÓGICO",
    "BILIRRUBINA TOTAL", "BILIRRUBINA DIRECTA", "GLUCOMETRÍA",
    "CREATININA", "PCR", "VSG", "AMILASA", "LIPASA",
    "AST / ALT", "ALBUMINA", "SODIO / POTASIO", "GASES ARTERIALES",
]

CIERRES = [
    ("OBSERVACION", "Sigue en observación"),
    ("HABITACION", "Pasa a habitación"),
    ("EGRESO", "Se va de egreso"),
    ("HOSPITALIZACION", "Se hospitaliza"),
    ("REMISION", "Se remite"),
]


class FilaMedicamentoRev(QWidget):
    """Fila para ingresar un medicamento en la revaloración."""

    def __init__(self, parent=None):
        super().__init__(parent)
        lay = QHBoxLayout()
        lay.setContentsMargins(0, 2, 0, 2)
        lay.setSpacing(6)

        self.combo_nombre = QComboBox()
        self.combo_nombre.setEditable(True)
        self.combo_nombre.addItems(MEDICAMENTOS_COMUNES)
        self.combo_nombre.setFont(QFont("Arial", 9))
        self.combo_nombre.setMinimumWidth(200)

        self.campo_cantidad = QLineEdit()
        self.campo_cantidad.setPlaceholderText("Cant.")
        self.campo_cantidad.setMaximumWidth(55)
        self.campo_cantidad.setFont(QFont("Arial", 9))

        self.combo_presentacion = QComboBox()
        self.combo_presentacion.addItems(PRESENTACIONES)
        self.combo_presentacion.setFont(QFont("Arial", 9))

        self.combo_via = QComboBox()
        self.combo_via.addItems(VIAS)
        self.combo_via.setFont(QFont("Arial", 9))

        self.boton_quitar = QPushButton("✕")
        self.boton_quitar.setMaximumWidth(28)
        self.boton_quitar.setFont(QFont("Arial", 9))
        self.boton_quitar.setStyleSheet("color: #e74c3c; border: none;")

        lay.addWidget(self.combo_nombre)
        lay.addWidget(self.campo_cantidad)
        lay.addWidget(self.combo_presentacion)
        lay.addWidget(QLabel("vía"))
        lay.addWidget(self.combo_via)
        lay.addWidget(self.boton_quitar)
        self.setLayout(lay)

    def obtener_medicamento(self):
        nombre = self.combo_nombre.currentText().strip()
        cantidad = self.campo_cantidad.text().strip()
        if not nombre or not cantidad:
            return None
        med = Medicamento()
        med.nombre = nombre
        med.cantidad = cantidad
        med.presentacion = self.combo_presentacion.currentText()
        med.via_administracion = self.combo_via.currentText()
        return med


class VistaRevaloracion(QWidget):
    """
    Vista para construir la nota de revaloración con:
    - Signos vitales opcionales (radio Sí/No)
    - Complicaciones + carro rojo
    - Plan médico del médico
    - Medicamentos administrados
    - Labs revisados y su resultado
    - Cierre (observación, habitación, egreso, hospitalización, remisión)
    """

    def __init__(self, controlador_app):
        super().__init__()
        self.controlador_app = controlador_app
        self.filas_medicamentos = []
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

        titulo = QLabel("Revaloración del Paciente")
        titulo.setFont(QFont("Arial", 15, QFont.Bold))
        titulo.setStyleSheet("color: #2c3e50;")
        sep = QFrame(); sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("color: #bdc3c7;")

        lay.addWidget(titulo)
        lay.addWidget(sep)
        lay.addWidget(self._grupo_signos())
        lay.addWidget(self._grupo_complicacion())
        lay.addWidget(self._grupo_medicamentos())
        lay.addWidget(self._grupo_labs())
        lay.addWidget(self._grupo_cierre())
        lay.addStretch()
        lay.addLayout(self._botones())

        contenedor.setLayout(lay)
        scroll.setWidget(contenedor)
        layout_raiz.addWidget(scroll)
        self.setLayout(layout_raiz)

    # ── Grupos ────────────────────────────────────────────────────────────────

    def _grupo_signos(self):
        g = QGroupBox("Signos vitales")
        g.setFont(QFont("Arial", 10, QFont.Bold))
        d = QVBoxLayout(); d.setSpacing(6)

        aviso = QLabel("Los signos vitales están deshabilitados por defecto para la revaloración.")
        aviso.setFont(QFont("Arial", 9))
        aviso.setStyleSheet("color: #7f8c8d; font-style: italic;")

        radio_row = QHBoxLayout()
        lbl = QLabel("¿Agregar nuevos signos vitales?")
        lbl.setFont(QFont("Arial", 10))
        self.radio_signos_no = QRadioButton("No")
        self.radio_signos_no.setFont(QFont("Arial", 10))
        self.radio_signos_no.setChecked(True)
        self.radio_signos_si = QRadioButton("Sí")
        self.radio_signos_si.setFont(QFont("Arial", 10))
        self.grupo_signos_radio = QButtonGroup()
        self.grupo_signos_radio.addButton(self.radio_signos_no)
        self.grupo_signos_radio.addButton(self.radio_signos_si)
        radio_row.addWidget(lbl)
        radio_row.addWidget(self.radio_signos_no)
        radio_row.addWidget(self.radio_signos_si)
        radio_row.addStretch()

        # Panel de signos (deshabilitado por defecto)
        self.panel_signos = QWidget()
        self.panel_signos.setEnabled(False)
        self.panel_signos.setStyleSheet("background: #f0f0f0; border-radius: 4px;")
        gs = QGridLayout(); gs.setSpacing(6)
        campos = [
            ("TA (mmHg):", "rev_campo_ta", "120/80"),
            ("FC (lpm):", "rev_campo_fc", "72"),
            ("FR (rpm):", "rev_campo_fr", "18"),
            ("Temp (°C):", "rev_campo_temp", "36.5"),
            ("SpO₂ (%):", "rev_campo_spo2", "98"),
        ]
        for i, (lbl_txt, attr, ph) in enumerate(campos):
            lbl2 = QLabel(lbl_txt); lbl2.setFont(QFont("Arial", 9))
            campo = QLineEdit(); campo.setPlaceholderText(ph)
            campo.setFont(QFont("Arial", 9)); campo.setMaximumWidth(120)
            setattr(self, attr, campo)
            gs.addWidget(lbl2, i // 2, (i % 2) * 2)
            gs.addWidget(campo, i // 2, (i % 2) * 2 + 1)
        self.panel_signos.setLayout(gs)

        def _toggle_signos(checked):
            self.panel_signos.setEnabled(checked)
            self.panel_signos.setStyleSheet(
                "background: white;" if checked else "background: #f0f0f0; border-radius: 4px;"
            )
        self.radio_signos_si.toggled.connect(_toggle_signos)

        d.addWidget(aviso)
        d.addLayout(radio_row)
        d.addWidget(self.panel_signos)
        g.setLayout(d); return g

    def _grupo_complicacion(self):
        g = QGroupBox("Complicaciones (opcional)")
        g.setFont(QFont("Arial", 10, QFont.Bold))
        d = QVBoxLayout(); d.setSpacing(6)

        self.check_complicacion = QCheckBox("Paciente presentó complicación durante la revaloración")
        self.check_complicacion.setFont(QFont("Arial", 10))
        self.check_complicacion.setStyleSheet("color: #c0392b;")

        self.panel_complicacion = QWidget()
        self.panel_complicacion.setVisible(False)
        dc = QVBoxLayout(); dc.setContentsMargins(10, 4, 0, 0); dc.setSpacing(6)

        lbl_desc = QLabel("Descripción de la complicación:")
        lbl_desc.setFont(QFont("Arial", 9))
        self.campo_desc_complicacion = QTextEdit()
        self.campo_desc_complicacion.setFont(QFont("Arial", 9))
        self.campo_desc_complicacion.setMaximumHeight(55)
        self.campo_desc_complicacion.setPlaceholderText("Ej: Paro cardiorrespiratorio, desaturación severa...")

        self.check_carro_rojo = QCheckBox("Se activó equipo de resucitación / carro rojo")
        self.check_carro_rojo.setFont(QFont("Arial", 9, QFont.Bold))
        self.check_carro_rojo.setStyleSheet("color: #c0392b;")

        self.panel_carro = QWidget()
        self.panel_carro.setVisible(False)
        dparro = QVBoxLayout(); dparro.setContentsMargins(10, 2, 0, 0); dparro.setSpacing(4)

        lbl_man = QLabel("Maniobras realizadas:")
        lbl_man.setFont(QFont("Arial", 9))
        self.checks_maniobras = {}
        grid_man = QGridLayout(); grid_man.setSpacing(3)
        for i, m in enumerate(MANIOBRAS_CARRO):
            cb = QCheckBox(m); cb.setFont(QFont("Arial", 9))
            self.checks_maniobras[m] = cb
            grid_man.addWidget(cb, i // 2, i % 2)

        lbl_med_carro = QLabel("Medicamentos del carro rojo usados:")
        lbl_med_carro.setFont(QFont("Arial", 9))
        self.campo_med_carro = QTextEdit()
        self.campo_med_carro.setFont(QFont("Arial", 9))
        self.campo_med_carro.setMaximumHeight(45)
        self.campo_med_carro.setPlaceholderText("Ej: ADRENALINA 1 AMPOLLA IV, ATROPINA 1 AMPOLLA IV...")

        dparro.addWidget(lbl_man)
        dparro.addLayout(grid_man)
        dparro.addWidget(lbl_med_carro)
        dparro.addWidget(self.campo_med_carro)
        self.panel_carro.setLayout(dparro)

        self.check_carro_rojo.stateChanged.connect(
            lambda s: self.panel_carro.setVisible(s == Qt.Checked)
        )

        dc.addWidget(lbl_desc)
        dc.addWidget(self.campo_desc_complicacion)
        dc.addWidget(self.check_carro_rojo)
        dc.addWidget(self.panel_carro)
        self.panel_complicacion.setLayout(dc)

        self.check_complicacion.stateChanged.connect(
            lambda s: self.panel_complicacion.setVisible(s == Qt.Checked)
        )

        d.addWidget(self.check_complicacion)
        d.addWidget(self.panel_complicacion)
        g.setLayout(d); return g

    def _grupo_medicamentos(self):
        g = QGroupBox("Plan del médico — Medicamentos a administrar")
        g.setFont(QFont("Arial", 10, QFont.Bold))
        self._lay_medicamentos = QVBoxLayout(); self._lay_medicamentos.setSpacing(4)

        # Selector de plan principal
        lbl_plan = QLabel("El médico ordena:")
        lbl_plan.setFont(QFont("Arial", 10))
        self.grupo_plan = QButtonGroup()
        planes = [
            ("MEDICAMENTO", "Nuevo medicamento"),
            ("EGRESO", "Egreso"),
            ("HOSPITALIZACION", "Hospitalización"),
            ("REMISION", "Remisión"),
        ]
        row_plan = QHBoxLayout()
        row_plan.addWidget(lbl_plan)
        self.radios_plan = {}
        for valor, texto in planes:
            rb = QRadioButton(texto)
            rb.setFont(QFont("Arial", 10))
            rb.setProperty("valor", valor)
            self.grupo_plan.addButton(rb)
            self.radios_plan[valor] = rb
            row_plan.addWidget(rb)
        self.radios_plan["MEDICAMENTO"].setChecked(True)
        row_plan.addStretch()

        # Destino para hospitalización/remisión
        self.panel_destino = QWidget(); self.panel_destino.setVisible(False)
        dd = QHBoxLayout(); dd.setContentsMargins(0, 0, 0, 0)
        lbl_dest = QLabel("Destino:"); lbl_dest.setFont(QFont("Arial", 9))
        self.campo_destino = QLineEdit()
        self.campo_destino.setFont(QFont("Arial", 9))
        self.campo_destino.setPlaceholderText("Ej: UCI, Clínica Central, Piso 3...")
        self.campo_destino.setMaximumWidth(250)
        dd.addWidget(lbl_dest); dd.addWidget(self.campo_destino); dd.addStretch()
        self.panel_destino.setLayout(dd)

        for rb in self.grupo_plan.buttons():
            rb.toggled.connect(self._al_cambiar_plan)

        # Lista de filas de medicamentos
        self.contenedor_meds = QWidget()
        self._lay_meds_inner = QVBoxLayout()
        self._lay_meds_inner.setContentsMargins(0, 0, 0, 0)
        self._lay_meds_inner.setSpacing(3)
        self.contenedor_meds.setLayout(self._lay_meds_inner)

        boton_agregar = QPushButton("+ Agregar medicamento")
        boton_agregar.setFont(QFont("Arial", 9))
        boton_agregar.setStyleSheet("""
            QPushButton { background:#2980b9; color:white; border-radius:4px; padding:4px 10px; }
            QPushButton:hover { background:#3498db; }
        """)
        boton_agregar.clicked.connect(self._agregar_fila_medicamento)
        self._agregar_fila_medicamento()  # Una fila inicial

        self._lay_medicamentos.addLayout(row_plan)
        self._lay_medicamentos.addWidget(self.panel_destino)
        self._lay_medicamentos.addWidget(self.contenedor_meds)
        self._lay_medicamentos.addWidget(boton_agregar)
        g.setLayout(self._lay_medicamentos)
        return g

    def _grupo_labs(self):
        g = QGroupBox("Resultados de laboratorio (opcional)")
        g.setFont(QFont("Arial", 10, QFont.Bold))
        d = QVBoxLayout(); d.setSpacing(5)

        self.check_labs_revisados = QCheckBox("Se recibieron y revisaron resultados de laboratorio")
        self.check_labs_revisados.setFont(QFont("Arial", 10))

        self.panel_labs = QWidget(); self.panel_labs.setVisible(False)
        dl = QVBoxLayout(); dl.setContentsMargins(10, 4, 0, 0); dl.setSpacing(4)

        lbl_labs = QLabel("Laboratorios revisados:"); lbl_labs.setFont(QFont("Arial", 9))
        self.checks_labs = {}
        grid_labs = QGridLayout(); grid_labs.setSpacing(3)
        for i, lab in enumerate(LABS_DISPONIBLES):
            cb = QCheckBox(lab); cb.setFont(QFont("Arial", 9))
            self.checks_labs[lab] = cb
            grid_labs.addWidget(cb, i // 2, i % 2)

        dl.addWidget(lbl_labs)
        dl.addLayout(grid_labs)
        self.panel_labs.setLayout(dl)

        self.check_labs_revisados.stateChanged.connect(
            lambda s: self.panel_labs.setVisible(s == Qt.Checked)
        )
        d.addWidget(self.check_labs_revisados)
        d.addWidget(self.panel_labs)
        g.setLayout(d); return g

    def _grupo_cierre(self):
        g = QGroupBox("Cierre de la revaloración")
        g.setFont(QFont("Arial", 10, QFont.Bold))
        d = QVBoxLayout(); d.setSpacing(6)

        lbl = QLabel("¿Cómo queda el paciente?"); lbl.setFont(QFont("Arial", 10))
        self.grupo_cierre = QButtonGroup()
        row = QHBoxLayout(); row.addWidget(lbl)
        self.radios_cierre = {}
        for valor, texto in CIERRES:
            rb = QRadioButton(texto); rb.setFont(QFont("Arial", 10))
            rb.setProperty("valor", valor)
            self.grupo_cierre.addButton(rb)
            self.radios_cierre[valor] = rb
            row.addWidget(rb)
        self.radios_cierre["OBSERVACION"].setChecked(True)
        row.addStretch()

        # Destino habitación
        self.panel_cierre_destino = QWidget(); self.panel_cierre_destino.setVisible(False)
        dcd = QHBoxLayout(); dcd.setContentsMargins(0, 0, 0, 0)
        lbl_cd = QLabel("Detalle:"); lbl_cd.setFont(QFont("Arial", 9))
        self.campo_cierre_destino = QLineEdit()
        self.campo_cierre_destino.setFont(QFont("Arial", 9))
        self.campo_cierre_destino.setPlaceholderText("Ej: Piso 3, Habitación 301...")
        self.campo_cierre_destino.setMaximumWidth(250)
        dcd.addWidget(lbl_cd); dcd.addWidget(self.campo_cierre_destino); dcd.addStretch()
        self.panel_cierre_destino.setLayout(dcd)

        for rb in self.grupo_cierre.buttons():
            rb.toggled.connect(self._al_cambiar_cierre)

        d.addLayout(row)
        d.addWidget(self.panel_cierre_destino)
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

    # ── Slots ────────────────────────────────────────────────────────────────

    def _al_cambiar_plan(self):
        rb = self.grupo_plan.checkedButton()
        if rb:
            val = rb.property("valor")
            mostrar_destino = val in ("HOSPITALIZACION", "REMISION")
            self.panel_destino.setVisible(mostrar_destino)
            self.contenedor_meds.setVisible(val == "MEDICAMENTO")

    def _al_cambiar_cierre(self):
        rb = self.grupo_cierre.checkedButton()
        if rb:
            val = rb.property("valor")
            self.panel_cierre_destino.setVisible(val in ("HABITACION", "HOSPITALIZACION", "REMISION"))

    def _agregar_fila_medicamento(self):
        fila = FilaMedicamentoRev(self)
        fila.boton_quitar.clicked.connect(lambda: self._quitar_fila(fila))
        self.filas_medicamentos.append(fila)
        self._lay_meds_inner.addWidget(fila)

    def _quitar_fila(self, fila):
        if fila in self.filas_medicamentos:
            self.filas_medicamentos.remove(fila)
            self._lay_meds_inner.removeWidget(fila)
            fila.deleteLater()

    def _al_ir_atras(self):
        if self.controlador_app.ventana_principal:
            self.controlador_app.ventana_principal.navegar_a_paciente()

    def _al_generar(self):
        nota = self.controlador_app.controlador_nota.nota_actual
        if not nota:
            return

        # Signos vitales
        nota.revaloracion_agregar_signos = self.radio_signos_si.isChecked()
        if nota.revaloracion_agregar_signos:
            self.controlador_app.controlador_nota.establecer_signos_vitales(
                ta=self.rev_campo_ta.text().strip(),
                fc=self.rev_campo_fc.text().strip(),
                fr=self.rev_campo_fr.text().strip(),
                temp=self.rev_campo_temp.text().strip(),
                spo2=self.rev_campo_spo2.text().strip(),
            )

        # Complicación
        nota.revaloracion_complicacion = self.check_complicacion.isChecked()
        if nota.revaloracion_complicacion:
            nota.revaloracion_desc_complicacion = self.campo_desc_complicacion.toPlainText().strip()
            nota.revaloracion_carro_rojo = self.check_carro_rojo.isChecked()
            if nota.revaloracion_carro_rojo:
                nota.revaloracion_maniobras_carro = [
                    m for m, cb in self.checks_maniobras.items() if cb.isChecked()
                ]
                raw = self.campo_med_carro.toPlainText().strip()
                nota.revaloracion_medicamentos_carro = (
                    [l.strip() for l in raw.split(",") if l.strip()] if raw else []
                )

        # Plan médico
        rb_plan = self.grupo_plan.checkedButton()
        nota.revaloracion_plan = rb_plan.property("valor") if rb_plan else "MEDICAMENTO"
        destino = self.campo_destino.text().strip()
        if nota.revaloracion_plan == "HOSPITALIZACION":
            nota.revaloracion_destino_hospitalizacion = destino
        elif nota.revaloracion_plan == "REMISION":
            nota.revaloracion_destino_remision = destino

        # Medicamentos
        nota.procedimientos = []
        meds = [f.obtener_medicamento() for f in self.filas_medicamentos]
        meds = [m for m in meds if m]
        if meds and nota.revaloracion_plan == "MEDICAMENTO":
            from modelos.procedimiento import Procedimiento
            proc = self.controlador_app.controlador_nota.agregar_procedimiento(
                Procedimiento.TIPO_INYECTOLOGIA, sitio_aplicacion=""
            )
            for med in meds:
                proc.medicamentos.append(med)
            # Construir plan automático
            self.controlador_app.controlador_nota.construir_plan_medico_automatico()

        # Labs
        nota.revaloracion_labs_revisados = self.check_labs_revisados.isChecked()
        if nota.revaloracion_labs_revisados:
            nota.revaloracion_labs_descritos = [
                lab for lab, cb in self.checks_labs.items() if cb.isChecked()
            ]

        # Cierre
        rb_cierre = self.grupo_cierre.checkedButton()
        nota.revaloracion_cierre = rb_cierre.property("valor") if rb_cierre else "OBSERVACION"
        nota.revaloracion_destino_hospitalizacion = self.campo_cierre_destino.text().strip() \
            if nota.revaloracion_cierre in ("HABITACION", "HOSPITALIZACION") else \
            nota.revaloracion_destino_hospitalizacion
        nota.revaloracion_destino_remision = self.campo_cierre_destino.text().strip() \
            if nota.revaloracion_cierre == "REMISION" else nota.revaloracion_destino_remision

        if self.controlador_app.ventana_principal:
            self.controlador_app.ventana_principal.navegar_a_resumen()

    def limpiar_campos(self):
        self.radio_signos_no.setChecked(True)
        for attr in ("rev_campo_ta", "rev_campo_fc", "rev_campo_fr", "rev_campo_temp", "rev_campo_spo2"):
            getattr(self, attr).clear()
        self.check_complicacion.setChecked(False)
        self.campo_desc_complicacion.clear()
        self.check_carro_rojo.setChecked(False)
        for cb in self.checks_maniobras.values():
            cb.setChecked(False)
        self.campo_med_carro.clear()
        self.radios_plan["MEDICAMENTO"].setChecked(True)
        self.campo_destino.clear()
        while self.filas_medicamentos:
            self._quitar_fila(self.filas_medicamentos[0])
        self._agregar_fila_medicamento()
        self.check_labs_revisados.setChecked(False)
        for cb in self.checks_labs.values():
            cb.setChecked(False)
        self.radios_cierre["OBSERVACION"].setChecked(True)
        self.campo_cierre_destino.clear()

"""
Módulo: vista_procedimientos.py
Descripción: Vista del plan médico. Incluye medicamentos, procedimientos
             clínicos y soporte para órdenes de consulta externa.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QCheckBox, QComboBox, QPushButton, QGroupBox,
    QScrollArea, QFrame, QMessageBox, QGridLayout,
    QRadioButton, QButtonGroup, QTextEdit, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from modelos.procedimiento import Procedimiento
from modelos.medicamento import Medicamento


ESTILO_BTN_VERDE = """
    QPushButton { background-color: #27ae60; color: white; border-radius: 5px; padding: 5px 10px; }
    QPushButton:hover { background-color: #2ecc71; }
"""
ESTILO_BTN_GRIS = """
    QPushButton { background-color: #95a5a6; color: white; border-radius: 5px; padding: 5px 14px; }
    QPushButton:hover { background-color: #7f8c8d; }
"""
ESTILO_BTN_VERDE_OSCURO = """
    QPushButton { background-color: #16a085; color: white; border-radius: 5px; padding: 5px 14px; }
    QPushButton:hover { background-color: #1abc9c; }
"""


class VistaProcedimientos(QWidget):
    """
    Vista del plan médico: medicamentos, procedimientos y consulta externa.
    """

    def __init__(self, controlador_app):
        super().__init__()
        self.controlador_app = controlador_app
        self.filas_medicamentos = []
        self._construir_interfaz()

    def _construir_interfaz(self):
        diseno_principal = QVBoxLayout()
        diseno_principal.setSpacing(8)
        diseno_principal.setContentsMargins(22, 18, 22, 18)

        lbl_titulo = QLabel("Plan Médico")
        lbl_titulo.setFont(QFont("Arial", 15, QFont.Bold))
        lbl_titulo.setStyleSheet("color: #2c3e50;")

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("color: #bdc3c7;")

        area_scroll = QScrollArea()
        area_scroll.setWidgetResizable(True)
        area_scroll.setFrameShape(QFrame.NoFrame)

        contenedor = QWidget()
        diseno_cont = QVBoxLayout()
        diseno_cont.setSpacing(8)

        # ── CONSULTA EXTERNA ──────────────────────────────────────────
        self.grupo_ce = QGroupBox("¿Viene por orden de consulta externa?")
        self.grupo_ce.setFont(QFont("Arial", 10, QFont.Bold))
        diseno_ce = QVBoxLayout()
        diseno_ce.setSpacing(4)

        diseno_check_ce = QHBoxLayout()
        self.check_consulta_externa = QCheckBox(
            "Sí, el paciente trae orden de consulta externa"
        )
        self.check_consulta_externa.setFont(QFont("Arial", 10))
        self.check_consulta_externa.stateChanged.connect(self._al_cambiar_ce)
        diseno_check_ce.addWidget(self.check_consulta_externa)
        diseno_check_ce.addStretch()

        self.panel_ce = QWidget()
        self.panel_ce.setVisible(False)
        diseno_panel_ce = QVBoxLayout()
        diseno_panel_ce.setContentsMargins(0, 4, 0, 0)
        diseno_panel_ce.setSpacing(4)
        lbl_ce = QLabel("Seleccione los procedimientos de la orden:")
        lbl_ce.setFont(QFont("Arial", 9))
        diseno_checks_ce = QHBoxLayout()
        self.checks_ce = {}
        for tipo in Procedimiento.TIPOS_CONSULTA_EXTERNA:
            cb = QCheckBox(tipo.capitalize())
            cb.setFont(QFont("Arial", 9))
            self.checks_ce[tipo] = cb
            diseno_checks_ce.addWidget(cb)
        diseno_checks_ce.addStretch()
        diseno_panel_ce.addWidget(lbl_ce)
        diseno_panel_ce.addLayout(diseno_checks_ce)
        self.panel_ce.setLayout(diseno_panel_ce)

        diseno_ce.addLayout(diseno_check_ce)
        diseno_ce.addWidget(self.panel_ce)
        self.grupo_ce.setLayout(diseno_ce)

        # ── MEDICAMENTOS ──────────────────────────────────────────────
        grupo_meds = QGroupBox("Medicamentos")
        grupo_meds.setFont(QFont("Arial", 10, QFont.Bold))
        diseno_meds = QVBoxLayout()
        diseno_meds.setSpacing(4)

        self.contenedor_filas_meds = QWidget()
        self.layout_filas_meds = QVBoxLayout()
        self.layout_filas_meds.setSpacing(3)
        self.layout_filas_meds.setContentsMargins(0, 0, 0, 0)
        self.contenedor_filas_meds.setLayout(self.layout_filas_meds)

        btn_agregar_med = QPushButton("+ Añadir medicamento")
        btn_agregar_med.setFont(QFont("Arial", 9))
        btn_agregar_med.setMaximumWidth(190)
        btn_agregar_med.setStyleSheet(ESTILO_BTN_VERDE)
        btn_agregar_med.clicked.connect(self._agregar_fila_medicamento)

        diseno_meds.addWidget(self.contenedor_filas_meds)
        diseno_meds.addWidget(btn_agregar_med)
        grupo_meds.setLayout(diseno_meds)

        # ── PROCEDIMIENTOS ────────────────────────────────────────────
        grupo_proc = QGroupBox("Procedimientos")
        grupo_proc.setFont(QFont("Arial", 10, QFont.Bold))
        diseno_proc = QVBoxLayout()
        diseno_proc.setSpacing(6)

        # Checkboxes en dos filas para no saturar
        fila1 = QHBoxLayout()
        fila2 = QHBoxLayout()
        self.checkboxes_procedimiento = {}
        tipos = Procedimiento.TIPOS_DISPONIBLES
        mitad = (len(tipos) + 1) // 2
        for i, tipo in enumerate(tipos):
            cb = QCheckBox(tipo.capitalize())
            cb.setFont(QFont("Arial", 9))
            cb.setProperty("tipo", tipo)
            cb.stateChanged.connect(self._al_cambiar_procedimiento)
            self.checkboxes_procedimiento[tipo] = cb
            (fila1 if i < mitad else fila2).addWidget(cb)
        fila1.addStretch()
        fila2.addStretch()

        self.contenedor_paneles = QWidget()
        self.contenedor_paneles.setVisible(False)
        self.diseno_paneles = QVBoxLayout()
        self.diseno_paneles.setContentsMargins(0, 4, 0, 0)
        self.diseno_paneles.setSpacing(6)
        self.contenedor_paneles.setLayout(self.diseno_paneles)

        # Crear todos los paneles
        self.paneles_procedimiento = {
            Procedimiento.TIPO_CANALIZACION:       self._panel_canalizacion(),
            Procedimiento.TIPO_CURACION:           self._panel_curacion(),
            Procedimiento.TIPO_SUTURA:             self._panel_sutura(),
            Procedimiento.TIPO_INYECTOLOGIA:       self._panel_inyectologia(),
            Procedimiento.TIPO_INMOVILIZACION:     self._panel_inmovilizacion(),
            Procedimiento.TIPO_ELECTROCARDIOGRAMA: self._panel_ecg(),
            Procedimiento.TIPO_LAVADO_OCULAR:      self._panel_lavado_ocular(),
            Procedimiento.TIPO_MONITORIA_FETAL:    self._panel_monitoria_fetal(),
            Procedimiento.TIPO_LABORATORIOS:       self._panel_laboratorios(),
        }

        diseno_proc.addLayout(fila1)
        diseno_proc.addLayout(fila2)
        diseno_proc.addWidget(self.contenedor_paneles)
        grupo_proc.setLayout(diseno_proc)

        diseno_cont.addWidget(self.grupo_ce)
        diseno_cont.addWidget(grupo_meds)
        diseno_cont.addWidget(grupo_proc)
        diseno_cont.addStretch()

        contenedor.setLayout(diseno_cont)
        area_scroll.setWidget(contenedor)

        # ── NAVEGACIÓN ────────────────────────────────────────────────
        diseno_nav = QHBoxLayout()
        btn_atras = QPushButton("← Atrás")
        btn_atras.setFont(QFont("Arial", 10))
        btn_atras.setMinimumHeight(36)
        btn_atras.setStyleSheet(ESTILO_BTN_GRIS)
        btn_atras.clicked.connect(self._al_ir_atras)

        btn_generar = QPushButton("Generar Nota ✓")
        btn_generar.setFont(QFont("Arial", 10, QFont.Bold))
        btn_generar.setMinimumHeight(36)
        btn_generar.setStyleSheet(ESTILO_BTN_VERDE_OSCURO)
        btn_generar.clicked.connect(self._al_generar_nota)

        diseno_nav.addWidget(btn_atras)
        diseno_nav.addStretch()
        diseno_nav.addWidget(btn_generar)

        diseno_principal.addWidget(lbl_titulo)
        diseno_principal.addWidget(sep)
        diseno_principal.addWidget(area_scroll)
        diseno_principal.addLayout(diseno_nav)
        self.setLayout(diseno_principal)

    # ── PANELES DE PROCEDIMIENTO ──────────────────────────────────────

    def _panel_canalizacion(self):
        p = QGroupBox("Config: Canalización")
        p.setFont(QFont("Arial", 9, QFont.Bold))
        d = QGridLayout(); d.setSpacing(5)

        # ── Catéter 1 ──────────────────────────────────────
        lbl_c1 = QLabel("Catéter 1:")
        lbl_c1.setFont(QFont("Arial", 9, QFont.Bold))
        lbl_c1.setStyleSheet("color:#2980b9;")

        self.combo_cateter = QComboBox(); self.combo_cateter.setFont(QFont("Arial", 9))
        self.combo_cateter.addItems(Procedimiento.TIPOS_CATETER)

        self.combo_vena_acceso = QComboBox(); self.combo_vena_acceso.setFont(QFont("Arial", 9))
        self.combo_vena_acceso.addItems(Procedimiento.VENAS_ACCESO)

        self.check_tapon = QCheckBox("Con tapón"); self.check_tapon.setFont(QFont("Arial", 9))

        self.combo_solucion = QComboBox(); self.combo_solucion.setFont(QFont("Arial", 9))
        self.combo_solucion.addItem("-- Sin solución --")
        self.combo_solucion.addItems(Procedimiento.SOLUCIONES)

        # ── Segundo catéter ─────────────────────────────────
        self.check_segundo_cateter = QCheckBox("Agregar segundo catéter (desangrado / doble acceso)")
        self.check_segundo_cateter.setFont(QFont("Arial", 9, QFont.Bold))
        self.check_segundo_cateter.setStyleSheet("color:#c0392b;")
        self.check_segundo_cateter.stateChanged.connect(self._al_cambiar_segundo_cateter)

        self.panel_segundo_cateter = QWidget()
        self.panel_segundo_cateter.setVisible(False)
        d2 = QGridLayout(); d2.setSpacing(4); d2.setContentsMargins(12, 0, 0, 0)

        lbl_c2 = QLabel("Catéter 2:")
        lbl_c2.setFont(QFont("Arial", 9, QFont.Bold))
        lbl_c2.setStyleSheet("color:#c0392b;")

        self.combo_cateter_2 = QComboBox(); self.combo_cateter_2.setFont(QFont("Arial", 9))
        self.combo_cateter_2.addItems(Procedimiento.TIPOS_CATETER)

        self.combo_vena_acceso_2 = QComboBox(); self.combo_vena_acceso_2.setFont(QFont("Arial", 9))
        self.combo_vena_acceso_2.addItems(Procedimiento.VENAS_ACCESO)

        self.check_tapon_2 = QCheckBox("Con tapón"); self.check_tapon_2.setFont(QFont("Arial", 9))

        self.combo_solucion_2 = QComboBox(); self.combo_solucion_2.setFont(QFont("Arial", 9))
        self.combo_solucion_2.addItem("-- Sin solución --")
        self.combo_solucion_2.addItems(Procedimiento.SOLUCIONES)

        d2.addWidget(lbl_c2, 0, 0)
        d2.addWidget(self.combo_cateter_2, 0, 1)
        d2.addWidget(QLabel("Vena:"), 1, 0); d2.addWidget(self.combo_vena_acceso_2, 1, 1)
        d2.addWidget(self.check_tapon_2, 2, 0, 1, 2)
        d2.addWidget(QLabel("Solución:"), 3, 0); d2.addWidget(self.combo_solucion_2, 3, 1)
        self.panel_segundo_cateter.setLayout(d2)

        # Ensamblar
        fila = 0
        d.addWidget(lbl_c1, fila, 0, 1, 2); fila += 1
        d.addWidget(QLabel("Catéter:"), fila, 0); d.addWidget(self.combo_cateter, fila, 1); fila += 1
        d.addWidget(QLabel("Vena:"), fila, 0); d.addWidget(self.combo_vena_acceso, fila, 1); fila += 1
        d.addWidget(self.check_tapon, fila, 0, 1, 2); fila += 1
        d.addWidget(QLabel("Solución:"), fila, 0); d.addWidget(self.combo_solucion, fila, 1); fila += 1
        d.addWidget(self.check_segundo_cateter, fila, 0, 1, 2); fila += 1
        d.addWidget(self.panel_segundo_cateter, fila, 0, 1, 2)
        p.setLayout(d); return p

    def _al_cambiar_segundo_cateter(self, estado):
        """Muestra u oculta el panel del segundo catéter."""
        from PyQt5.QtCore import Qt
        self.panel_segundo_cateter.setVisible(estado == Qt.Checked)

    def _panel_curacion(self):
        p = QGroupBox("Config: Curación")
        p.setFont(QFont("Arial", 9, QFont.Bold))
        d = QGridLayout(); d.setSpacing(5)
        self.combo_herida = QComboBox(); self.combo_herida.setFont(QFont("Arial", 9))
        self.combo_herida.addItems(Procedimiento.TIPOS_HERIDA)
        self.checks_materiales = {}
        dm = QHBoxLayout()
        for mat in Procedimiento.MATERIALES_CURACION:
            cb = QCheckBox(mat); cb.setFont(QFont("Arial", 9))
            self.checks_materiales[mat] = cb; dm.addWidget(cb)
        dm.addStretch()
        self.campo_desc_curacion = QTextEdit()
        self.campo_desc_curacion.setFont(QFont("Arial", 9))
        self.campo_desc_curacion.setMaximumHeight(50)
        self.campo_desc_curacion.setPlaceholderText("Descripción adicional (opcional)...")
        d.addWidget(QLabel("Tipo herida:"), 0, 0); d.addWidget(self.combo_herida, 0, 1)
        d.addWidget(QLabel("Materiales:"), 1, 0); d.addLayout(dm, 1, 1)
        d.addWidget(QLabel("Descripción:"), 2, 0); d.addWidget(self.campo_desc_curacion, 2, 1)
        p.setLayout(d); return p

    def _panel_sutura(self):
        p = QGroupBox("Config: Sutura")
        p.setFont(QFont("Arial", 9, QFont.Bold))
        d = QGridLayout(); d.setSpacing(5)
        self.combo_anestesia = QComboBox(); self.combo_anestesia.setFont(QFont("Arial", 9))
        self.combo_anestesia.addItems(Procedimiento.TIPOS_ANESTESIA)
        self.campo_puntos = QLineEdit(); self.campo_puntos.setFont(QFont("Arial", 9))
        self.campo_puntos.setPlaceholderText("Ej: 5"); self.campo_puntos.setMaximumWidth(80)
        self.combo_tipo_sutura = QComboBox(); self.combo_tipo_sutura.setFont(QFont("Arial", 9))
        self.combo_tipo_sutura.addItems(Procedimiento.TIPOS_SUTURA)
        self.check_sangrado = QCheckBox("Control de sangrado realizado")
        self.check_sangrado.setFont(QFont("Arial", 9))
        self.campo_desc_sutura = QTextEdit()
        self.campo_desc_sutura.setFont(QFont("Arial", 9))
        self.campo_desc_sutura.setMaximumHeight(50)
        self.campo_desc_sutura.setPlaceholderText("Descripción adicional (opcional)...")
        d.addWidget(QLabel("Anestesia:"), 0, 0); d.addWidget(self.combo_anestesia, 0, 1)
        d.addWidget(QLabel("N° puntos:"), 1, 0); d.addWidget(self.campo_puntos, 1, 1)
        d.addWidget(QLabel("Tipo sutura:"), 2, 0); d.addWidget(self.combo_tipo_sutura, 2, 1)
        d.addWidget(self.check_sangrado, 3, 0, 1, 2)
        d.addWidget(QLabel("Descripción:"), 4, 0); d.addWidget(self.campo_desc_sutura, 4, 1)
        p.setLayout(d); return p

    def _panel_inyectologia(self):
        p = QGroupBox("Config: Inyectología")
        p.setFont(QFont("Arial", 9, QFont.Bold))
        d = QHBoxLayout(); d.setSpacing(8)
        self.combo_sitio = QComboBox(); self.combo_sitio.setFont(QFont("Arial", 9))
        self.combo_sitio.addItems(Procedimiento.SITIOS_APLICACION)
        d.addWidget(QLabel("Sitio de aplicación:")); d.addWidget(self.combo_sitio)
        d.addStretch(); p.setLayout(d); return p

    def _panel_inmovilizacion(self):
        p = QGroupBox("Config: Inmovilización")
        p.setFont(QFont("Arial", 9, QFont.Bold))
        d = QGridLayout(); d.setSpacing(5)

        self.combo_zona_inmovilizacion = QComboBox()
        self.combo_zona_inmovilizacion.setFont(QFont("Arial", 9))
        self.combo_zona_inmovilizacion.addItems(Procedimiento.ZONAS_INMOVILIZACION)

        self.combo_tipo_inmovilizacion = QComboBox()
        self.combo_tipo_inmovilizacion.setFont(QFont("Arial", 9))
        self.combo_tipo_inmovilizacion.addItems(Procedimiento.TIPOS_INMOVILIZACION)

        self.combo_medida_venda = QComboBox()
        self.combo_medida_venda.setFont(QFont("Arial", 9))
        self.combo_medida_venda.addItems(Procedimiento.MEDIDAS_VENDA)

        self.campo_desc_inmovilizacion = QTextEdit()
        self.campo_desc_inmovilizacion.setFont(QFont("Arial", 9))
        self.campo_desc_inmovilizacion.setMaximumHeight(45)
        self.campo_desc_inmovilizacion.setPlaceholderText("Observaciones adicionales (opcional)...")

        d.addWidget(QLabel("Zona:"), 0, 0); d.addWidget(self.combo_zona_inmovilizacion, 0, 1)
        d.addWidget(QLabel("Tipo:"), 1, 0); d.addWidget(self.combo_tipo_inmovilizacion, 1, 1)
        d.addWidget(QLabel("Medida:"), 2, 0); d.addWidget(self.combo_medida_venda, 2, 1)
        d.addWidget(QLabel("Obs:"), 3, 0); d.addWidget(self.campo_desc_inmovilizacion, 3, 1)
        p.setLayout(d); return p

    def _panel_ecg(self):
        p = QGroupBox("Config: Electrocardiograma")
        p.setFont(QFont("Arial", 9, QFont.Bold))
        d = QVBoxLayout(); d.setSpacing(5)

        lbl_info = QLabel("Se indicará al paciente retirar todos los elementos metálicos.")
        lbl_info.setFont(QFont("Arial", 9)); lbl_info.setStyleSheet("color:#7f8c8d;font-style:italic;")

        lbl_prot = QLabel("¿Tiene cirugías o prótesis con material metálico?")
        lbl_prot.setFont(QFont("Arial", 9, QFont.Bold))

        self.grupo_protesis_ecg = QButtonGroup()
        self.radio_sin_protesis = QRadioButton("No"); self.radio_sin_protesis.setFont(QFont("Arial", 9))
        self.radio_sin_protesis.setChecked(True)
        self.radio_con_protesis = QRadioButton("Sí"); self.radio_con_protesis.setFont(QFont("Arial", 9))
        self.grupo_protesis_ecg.addButton(self.radio_sin_protesis)
        self.grupo_protesis_ecg.addButton(self.radio_con_protesis)
        dr = QHBoxLayout()
        dr.addWidget(self.radio_sin_protesis); dr.addWidget(self.radio_con_protesis); dr.addStretch()

        self.campo_tipo_protesis = QLineEdit()
        self.campo_tipo_protesis.setFont(QFont("Arial", 9))
        self.campo_tipo_protesis.setPlaceholderText("Especifique tipo de prótesis o cirugía...")
        self.campo_tipo_protesis.setVisible(False)
        self.radio_con_protesis.toggled.connect(lambda checked: self.campo_tipo_protesis.setVisible(checked))

        # Plan médico (solo para consulta externa)
        self.lbl_plan_ecg = QLabel("Plan médico según resultado:")
        self.lbl_plan_ecg.setFont(QFont("Arial", 9, QFont.Bold))
        self.lbl_plan_ecg.setVisible(False)
        self.grupo_plan_ecg = QButtonGroup()
        self.radio_ecg_egreso = QRadioButton("Egreso"); self.radio_ecg_egreso.setFont(QFont("Arial", 9))
        self.radio_ecg_egreso.setChecked(True)
        self.radio_ecg_urgencias = QRadioButton("Ingreso a urgencias"); self.radio_ecg_urgencias.setFont(QFont("Arial", 9))
        self.grupo_plan_ecg.addButton(self.radio_ecg_egreso)
        self.grupo_plan_ecg.addButton(self.radio_ecg_urgencias)
        self.widget_plan_ecg = QWidget(); self.widget_plan_ecg.setVisible(False)
        dp = QHBoxLayout(); dp.setContentsMargins(0,0,0,0)
        dp.addWidget(self.radio_ecg_egreso); dp.addWidget(self.radio_ecg_urgencias); dp.addStretch()
        self.widget_plan_ecg.setLayout(dp)

        d.addWidget(lbl_info); d.addWidget(lbl_prot); d.addLayout(dr)
        d.addWidget(self.campo_tipo_protesis)
        d.addWidget(self.lbl_plan_ecg); d.addWidget(self.widget_plan_ecg)
        p.setLayout(d); return p

    def _panel_lavado_ocular(self):
        p = QGroupBox("Config: Lavado Ocular")
        p.setFont(QFont("Arial", 9, QFont.Bold))
        d = QGridLayout(); d.setSpacing(5)

        self.combo_ojo_afectado = QComboBox(); self.combo_ojo_afectado.setFont(QFont("Arial", 9))
        self.combo_ojo_afectado.addItems(["OJO DERECHO", "OJO IZQUIERDO", "AMBOS OJOS"])

        self.campo_motivo_lavado = QLineEdit(); self.campo_motivo_lavado.setFont(QFont("Arial", 9))
        self.campo_motivo_lavado.setPlaceholderText("Ej: presencia de cuerpo extraño, irritante químico...")

        d.addWidget(QLabel("Ojo afectado:"), 0, 0); d.addWidget(self.combo_ojo_afectado, 0, 1)
        d.addWidget(QLabel("Motivo:"), 1, 0); d.addWidget(self.campo_motivo_lavado, 1, 1)
        p.setLayout(d); return p

    def _panel_monitoria_fetal(self):
        p = QGroupBox("Config: Monitoría Fetal")
        p.setFont(QFont("Arial", 9, QFont.Bold))
        d = QGridLayout(); d.setSpacing(5)

        self.campo_semanas_gestacion = QLineEdit(); self.campo_semanas_gestacion.setFont(QFont("Arial", 9))
        self.campo_semanas_gestacion.setPlaceholderText("Ej: 36"); self.campo_semanas_gestacion.setMaximumWidth(80)

        self.grupo_resultado_monitoria = QButtonGroup()
        self.radio_reactiva = QRadioButton("Reactiva"); self.radio_reactiva.setFont(QFont("Arial", 9))
        self.radio_reactiva.setChecked(True)
        self.radio_no_reactiva = QRadioButton("No reactiva"); self.radio_no_reactiva.setFont(QFont("Arial", 9))
        self.grupo_resultado_monitoria.addButton(self.radio_reactiva)
        self.grupo_resultado_monitoria.addButton(self.radio_no_reactiva)
        dr = QHBoxLayout()
        dr.addWidget(self.radio_reactiva); dr.addWidget(self.radio_no_reactiva); dr.addStretch()

        lbl_plan = QLabel("Plan médico según resultado:")
        lbl_plan.setFont(QFont("Arial", 9, QFont.Bold))
        self.grupo_plan_monitoria = QButtonGroup()
        self.radio_mon_egreso = QRadioButton("Egreso"); self.radio_mon_egreso.setFont(QFont("Arial", 9))
        self.radio_mon_egreso.setChecked(True)
        self.radio_mon_urgencias = QRadioButton("Ingreso a urgencias"); self.radio_mon_urgencias.setFont(QFont("Arial", 9))
        self.grupo_plan_monitoria.addButton(self.radio_mon_egreso)
        self.grupo_plan_monitoria.addButton(self.radio_mon_urgencias)
        dp = QHBoxLayout()
        dp.addWidget(self.radio_mon_egreso); dp.addWidget(self.radio_mon_urgencias); dp.addStretch()

        d.addWidget(QLabel("Semanas gestación:"), 0, 0); d.addWidget(self.campo_semanas_gestacion, 0, 1)
        d.addWidget(QLabel("Resultado:"), 1, 0)
        w_res = QWidget(); w_res.setLayout(dr); d.addWidget(w_res, 1, 1)
        d.addWidget(lbl_plan, 2, 0, 1, 2)
        w_plan = QWidget(); w_plan.setLayout(dp); d.addWidget(w_plan, 3, 0, 1, 2)
        p.setLayout(d); return p

    def _panel_laboratorios(self):
        p = QGroupBox("Config: Laboratorios")
        p.setFont(QFont("Arial", 9, QFont.Bold))
        d = QVBoxLayout(); d.setSpacing(4)

        lbl = QLabel("Seleccione los exámenes solicitados:")
        lbl.setFont(QFont("Arial", 9))

        self.checks_laboratorios = {}
        fila1 = QHBoxLayout(); fila2 = QHBoxLayout()
        labs = Procedimiento.LABORATORIOS_DISPONIBLES
        mitad = (len(labs) + 1) // 2
        for i, lab in enumerate(labs):
            cb = QCheckBox(lab); cb.setFont(QFont("Arial", 9))
            self.checks_laboratorios[lab] = cb
            (fila1 if i < mitad else fila2).addWidget(cb)
        fila1.addStretch(); fila2.addStretch()

        self.campo_resultados_lab = QTextEdit()
        self.campo_resultados_lab.setFont(QFont("Arial", 9))
        self.campo_resultados_lab.setMaximumHeight(50)
        self.campo_resultados_lab.setPlaceholderText("Observaciones de resultados (opcional)...")

        d.addWidget(lbl)
        d.addLayout(fila1); d.addLayout(fila2)
        d.addWidget(self.campo_resultados_lab)
        p.setLayout(d); return p

    # ── LÓGICA DE INTERACCIÓN ─────────────────────────────────────────

    def _al_cambiar_ce(self, estado):
        """Muestra u oculta el panel de consulta externa."""
        self.panel_ce.setVisible(estado == Qt.Checked)
        # Si tiene CE con ECG o monitoría, mostrar el plan médico en sus paneles
        self._actualizar_visibilidad_plan_medico()

    def _actualizar_visibilidad_plan_medico(self):
        """Muestra el selector de plan médico solo si el proc es de consulta externa."""
        es_ce = self.check_consulta_externa.isChecked()
        ecg_en_ce = es_ce and self.checks_ce.get(Procedimiento.TIPO_ELECTROCARDIOGRAMA, QCheckBox()).isChecked()
        self.lbl_plan_ecg.setVisible(ecg_en_ce)
        self.widget_plan_ecg.setVisible(ecg_en_ce)

    def _al_cambiar_procedimiento(self):
        """Actualiza los paneles según los procedimientos seleccionados."""
        while self.diseno_paneles.count():
            item = self.diseno_paneles.takeAt(0)
            if item.widget():
                item.widget().setParent(None)

        tipos_sel = [
            tipo for tipo, cb in self.checkboxes_procedimiento.items()
            if cb.isChecked()
        ]

        if tipos_sel:
            self.contenedor_paneles.setVisible(True)
            for tipo in tipos_sel:
                panel = self.paneles_procedimiento.get(tipo)
                if panel:
                    self.diseno_paneles.addWidget(panel)
                    panel.setVisible(True)
        else:
            self.contenedor_paneles.setVisible(False)

    def _agregar_fila_medicamento(self):
        fila = FilaMedicamento(self._eliminar_fila_medicamento)
        self.filas_medicamentos.append(fila)
        self.layout_filas_meds.addWidget(fila)

    def _eliminar_fila_medicamento(self, fila):
        if fila in self.filas_medicamentos:
            self.filas_medicamentos.remove(fila)
            fila.setParent(None); fila.deleteLater()

    def limpiar_campos(self):
        """Limpia todos los campos para una nueva nota."""
        for fila in list(self.filas_medicamentos):
            fila.setParent(None); fila.deleteLater()
        self.filas_medicamentos.clear()

        self.check_consulta_externa.setChecked(False)
        for cb in self.checks_ce.values():
            cb.setChecked(False)

        for cb in self.checkboxes_procedimiento.values():
            cb.setChecked(False)

        # Canalización
        self.combo_cateter.setCurrentIndex(0)
        self.combo_vena_acceso.setCurrentIndex(0)
        self.check_tapon.setChecked(False)
        self.combo_solucion.setCurrentIndex(0)
        self.check_segundo_cateter.setChecked(False)
        self.panel_segundo_cateter.setVisible(False)
        self.combo_cateter_2.setCurrentIndex(0)
        self.combo_vena_acceso_2.setCurrentIndex(0)
        self.check_tapon_2.setChecked(False)
        self.combo_solucion_2.setCurrentIndex(0)
        # Curación
        self.combo_herida.setCurrentIndex(0)
        for cb in self.checks_materiales.values(): cb.setChecked(False)
        self.campo_desc_curacion.clear()
        # Sutura
        self.combo_anestesia.setCurrentIndex(0)
        self.campo_puntos.clear()
        self.combo_tipo_sutura.setCurrentIndex(0)
        self.check_sangrado.setChecked(False)
        self.campo_desc_sutura.clear()
        # Inyectología
        self.combo_sitio.setCurrentIndex(0)
        # Inmovilización
        self.combo_zona_inmovilizacion.setCurrentIndex(0)
        self.combo_tipo_inmovilizacion.setCurrentIndex(0)
        self.combo_medida_venda.setCurrentIndex(0)
        self.campo_desc_inmovilizacion.clear()
        # ECG
        self.radio_sin_protesis.setChecked(True)
        self.campo_tipo_protesis.clear(); self.campo_tipo_protesis.setVisible(False)
        self.radio_ecg_egreso.setChecked(True)
        # Lavado ocular
        self.combo_ojo_afectado.setCurrentIndex(0)
        self.campo_motivo_lavado.clear()
        # Monitoría fetal
        self.campo_semanas_gestacion.clear()
        self.radio_reactiva.setChecked(True)
        self.radio_mon_egreso.setChecked(True)
        # Laboratorios
        for cb in self.checks_laboratorios.values(): cb.setChecked(False)
        self.campo_resultados_lab.clear()

    def _recopilar_procedimientos(self):
        ctrl = self.controlador_app.controlador_nota
        procedimientos = []
        es_ce = self.check_consulta_externa.isChecked()

        for tipo, cb in self.checkboxes_procedimiento.items():
            if not cb.isChecked():
                continue
            kwargs = {"es_consulta_externa": False}

            if tipo == Procedimiento.TIPO_CANALIZACION:
                sol = self.combo_solucion.currentText()
                sol2 = self.combo_solucion_2.currentText()
                kwargs.update({
                    "tipo_cateter": self.combo_cateter.currentText(),
                    "vena_acceso": self.combo_vena_acceso.currentText(),
                    "con_tapon": self.check_tapon.isChecked(),
                    "solucion": "" if "Sin solución" in sol else sol,
                    "segundo_cateter": self.check_segundo_cateter.isChecked(),
                    "tipo_cateter_2": self.combo_cateter_2.currentText(),
                    "vena_acceso_2": self.combo_vena_acceso_2.currentText(),
                    "con_tapon_2": self.check_tapon_2.isChecked(),
                    "solucion_2": "" if "Sin solución" in sol2 else sol2,

                })
            elif tipo == Procedimiento.TIPO_CURACION:
                mats = [m for m, c in self.checks_materiales.items() if c.isChecked()]
                kwargs.update({
                    "tipo_herida": self.combo_herida.currentText(),
                    "materiales": mats,
                    "descripcion": self.campo_desc_curacion.toPlainText().strip(),
                })
            elif tipo == Procedimiento.TIPO_SUTURA:
                kwargs.update({
                    "tipo_anestesia": self.combo_anestesia.currentText(),
                    "numero_puntos": int(self.campo_puntos.text() or 0),
                    "tipo_sutura": self.combo_tipo_sutura.currentText(),
                    "control_sangrado": self.check_sangrado.isChecked(),
                    "descripcion": self.campo_desc_sutura.toPlainText().strip(),
                })
            elif tipo == Procedimiento.TIPO_INYECTOLOGIA:
                kwargs.update({"sitio_aplicacion": self.combo_sitio.currentText()})
            elif tipo == Procedimiento.TIPO_INMOVILIZACION:
                kwargs.update({
                    "zona_inmovilizacion": self.combo_zona_inmovilizacion.currentText(),
                    "tipo_inmovilizacion": self.combo_tipo_inmovilizacion.currentText(),
                    "medida_venda": self.combo_medida_venda.currentText(),
                    "descripcion": self.campo_desc_inmovilizacion.toPlainText().strip(),
                })
            elif tipo == Procedimiento.TIPO_ELECTROCARDIOGRAMA:
                plan = "EGRESO" if self.radio_ecg_egreso.isChecked() else "INGRESO A URGENCIAS"
                kwargs.update({
                    "ecg_tiene_protesis": self.radio_con_protesis.isChecked(),
                    "ecg_tipo_protesis": self.campo_tipo_protesis.text().strip(),
                    "es_consulta_externa": es_ce and self.checks_ce.get(tipo, QCheckBox()).isChecked(),
                    "plan_medico": plan if (es_ce and self.checks_ce.get(tipo, QCheckBox()).isChecked()) else "",
                })
            elif tipo == Procedimiento.TIPO_LAVADO_OCULAR:
                kwargs.update({
                    "ojo_afectado": self.combo_ojo_afectado.currentText(),
                    "motivo": self.campo_motivo_lavado.text().strip(),
                    "es_consulta_externa": es_ce and self.checks_ce.get(tipo, QCheckBox()).isChecked(),
                })
            elif tipo == Procedimiento.TIPO_MONITORIA_FETAL:
                res = "REACTIVA" if self.radio_reactiva.isChecked() else "NO REACTIVA"
                plan = "EGRESO" if self.radio_mon_egreso.isChecked() else "INGRESO A URGENCIAS"
                kwargs.update({
                    "semanas_gestacion": self.campo_semanas_gestacion.text().strip(),
                    "resultado": res,
                    "plan_medico": plan,
                    "es_consulta_externa": es_ce and self.checks_ce.get(tipo, QCheckBox()).isChecked(),
                })
            elif tipo == Procedimiento.TIPO_LABORATORIOS:
                labs = [lab for lab, cb in self.checks_laboratorios.items() if cb.isChecked()]
                kwargs.update({
                    "labs_solicitados": labs,
                    "resultados": self.campo_resultados_lab.toPlainText().strip(),
                })

            proc = ctrl.agregar_procedimiento(tipo, **kwargs)
            procedimientos.append(proc)

        return procedimientos

    def sincronizar_semanas_gestante(self):
        """
        Pre-llena el campo de semanas en el panel de monitoría fetal
        con las semanas que ya ingresó la enfermera en el formulario del paciente.
        Llamar al entrar a esta vista si la paciente es gestante.
        """
        try:
            nota = self.controlador_app.controlador_nota.nota_actual
            if nota and nota.paciente:
                semanas = getattr(nota.paciente, "semanas_gestacion", "")
                if semanas and hasattr(self, "campo_semanas_monitoria"):
                    self.campo_semanas_monitoria.setText(semanas)
        except Exception:
            pass

    def _al_generar_nota(self):
        self.controlador_app.controlador_nota.nota_actual.procedimientos = []
        self.controlador_app.controlador_nota.nota_actual.ordenes_plan_medico = []
        es_ce = self.check_consulta_externa.isChecked()

        # Registrar procedimientos de CE en la nota
        if es_ce:
            nombres_ce = [
                tipo for tipo, cb in self.checks_ce.items() if cb.isChecked()
            ]
            self.controlador_app.controlador_nota.establecer_consulta_externa(
                es_ce, nombres_ce
            )
        else:
            self.controlador_app.controlador_nota.establecer_consulta_externa(False, [])

        procedimientos = self._recopilar_procedimientos()

        # Medicamentos del plan general
        meds_validos = []
        for fila in self.filas_medicamentos:
            med = fila.obtener_medicamento()
            if med and med.esta_completo():
                meds_validos.append(med)

        if meds_validos:
            destino = procedimientos[0] if procedimientos else \
                self.controlador_app.controlador_nota.agregar_procedimiento(
                    Procedimiento.TIPO_INYECTOLOGIA, sitio_aplicacion=""
                )
            for med in meds_validos:
                destino.agregar_medicamento(med)

        # Construir automáticamente el plan médico desde los procedimientos
        self.controlador_app.controlador_nota.construir_plan_medico_automatico()

        if self.controlador_app.ventana_principal:
            self.controlador_app.ventana_principal.navegar_a_resumen()

    def _al_ir_atras(self):
        if self.controlador_app.ventana_principal:
            self.controlador_app.ventana_principal.navegar_a_formulario_paciente()


class FilaMedicamento(QFrame):
    def __init__(self, callback_eliminar):
        super().__init__()
        self.callback_eliminar = callback_eliminar
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet("background-color: #f8f9fa; border-radius: 4px; padding: 2px;")
        self._construir()

    def _construir(self):
        d = QHBoxLayout(); d.setContentsMargins(6, 3, 6, 3); d.setSpacing(5)
        self.campo_nombre = QLineEdit()
        self.campo_nombre.setPlaceholderText("Nombre del medicamento")
        self.campo_nombre.setFont(QFont("Arial", 9))
        self.combo_presentacion = QComboBox()
        self.combo_presentacion.setFont(QFont("Arial", 9))
        self.combo_presentacion.addItems(Medicamento.PRESENTACIONES)
        self.combo_presentacion.setMaximumWidth(110)
        self.campo_cantidad = QLineEdit()
        self.campo_cantidad.setPlaceholderText("Cant.")
        self.campo_cantidad.setMaximumWidth(55)
        self.campo_cantidad.setFont(QFont("Arial", 9))
        self.combo_via = QComboBox()
        self.combo_via.setFont(QFont("Arial", 9))
        self.combo_via.addItems(Medicamento.VIAS_ADMINISTRACION)
        self.combo_via.setMaximumWidth(130)
        btn_del = QPushButton("✕")
        btn_del.setFont(QFont("Arial", 9, QFont.Bold))
        btn_del.setMaximumWidth(26); btn_del.setMaximumHeight(24)
        btn_del.setStyleSheet("""
            QPushButton { background-color:#e74c3c; color:white; border-radius:4px; padding:2px; }
            QPushButton:hover { background-color:#c0392b; }
        """)
        btn_del.clicked.connect(lambda: self.callback_eliminar(self))
        d.addWidget(self.campo_nombre); d.addWidget(self.combo_presentacion)
        d.addWidget(QLabel("Cant:")); d.addWidget(self.campo_cantidad)
        d.addWidget(QLabel("Vía:")); d.addWidget(self.combo_via)
        d.addWidget(btn_del); self.setLayout(d)

    def obtener_medicamento(self):
        med = Medicamento()
        med.nombre = self.campo_nombre.text().strip()
        med.presentacion = self.combo_presentacion.currentText()
        med.cantidad = self.campo_cantidad.text().strip()
        med.via_administracion = self.combo_via.currentText()
        return med

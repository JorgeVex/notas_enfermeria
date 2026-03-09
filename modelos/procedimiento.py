"""
Módulo: procedimiento.py
Descripción: Modelo que representa un procedimiento clínico realizado
             al paciente durante su atención en urgencias.
"""

from modelos.medicamento import Medicamento


class Procedimiento:
    """
    Clase que encapsula los datos de un procedimiento médico.
    Cada tipo de procedimiento activa campos y bloques específicos.
    """

    # Tipos de procedimiento disponibles
    TIPO_INYECTOLOGIA       = "INYECTOLOGÍA"
    TIPO_CANALIZACION       = "CANALIZACIÓN"
    TIPO_CURACION           = "CURACIÓN"
    TIPO_SUTURA             = "SUTURA"
    TIPO_INMOVILIZACION     = "INMOVILIZACIÓN"
    TIPO_ELECTROCARDIOGRAMA = "ELECTROCARDIOGRAMA"
    TIPO_LAVADO_OCULAR      = "LAVADO OCULAR"
    TIPO_MONITORIA_FETAL    = "MONITORÍA FETAL"
    TIPO_LABORATORIOS       = "LABORATORIOS"

    # Procedimientos que pueden provenir de orden de consulta externa
    TIPOS_CONSULTA_EXTERNA = [
        TIPO_ELECTROCARDIOGRAMA,
        TIPO_MONITORIA_FETAL,
        TIPO_LAVADO_OCULAR,
        TIPO_CURACION,
    ]

    TIPOS_DISPONIBLES = [
        TIPO_INYECTOLOGIA,
        TIPO_CANALIZACION,
        TIPO_CURACION,
        TIPO_SUTURA,
        TIPO_INMOVILIZACION,
        TIPO_ELECTROCARDIOGRAMA,
        TIPO_LAVADO_OCULAR,
        TIPO_MONITORIA_FETAL,
        TIPO_LABORATORIOS,
    ]

    # Tipos de catéter para canalización
    TIPOS_CATETER = [
        "CATÉTER N°14", "CATÉTER N°16", "CATÉTER N°18",
        "CATÉTER N°20", "CATÉTER N°22", "CATÉTER N°24",
    ]

    # Venas de acceso venoso periférico (ordenadas de más a menos frecuente en urgencias)
    VENAS_ACCESO = [
        # ── Las más usadas en urgencias ─────────────────────
        "VENA ANTECUBITAL DERECHA",       # 1ª elección habitual
        "VENA ANTECUBITAL IZQUIERDA",
        "VENA CEFÁLICA DERECHA",          # Fácil acceso, calibre bueno
        "VENA CEFÁLICA IZQUIERDA",
        "VENA BASÍLICA DERECHA",          # Alternativa frecuente
        "VENA BASÍLICA IZQUIERDA",
        # ── Antebrazo / muñeca ──────────────────────────────
        "VENA RADIAL DERECHA",
        "VENA RADIAL IZQUIERDA",
        "VENA CUBITAL DERECHA",
        "VENA CUBITAL IZQUIERDA",
        # ── Mano ────────────────────────────────────────────
        "VENA METACARPIANA DERECHA",
        "VENA METACARPIANA IZQUIERDA",
        "VENA DORSAL DE MANO DERECHA",
        "VENA DORSAL DE MANO IZQUIERDA",
        # ── Miembro inferior ────────────────────────────────
        "VENA SAFENA MAYOR DERECHA",
        "VENA SAFENA MAYOR IZQUIERDA",
        "VENA DORSAL DE PIE DERECHO",
        "VENA DORSAL DE PIE IZQUIERDO",
        # ── Acceso de emergencia / central ──────────────────
        "VENA YUGULAR EXTERNA DERECHA",
        "VENA YUGULAR EXTERNA IZQUIERDA",
        "VENA FEMORAL DERECHA",
        "VENA FEMORAL IZQUIERDA",
        "VENA SUBCLAVIA DERECHA",
        "VENA SUBCLAVIA IZQUIERDA",
    ]

    # Soluciones para canalización
    SOLUCIONES = [
        "SOLUCIÓN SALINA NORMAL 0.9%",
        "LACTATO DE RINGER",
        "DEXTROSA AL 5%",
        "HARTMANN",
    ]

    # Sitios de aplicación para inyectología
    SITIOS_APLICACION = ["GLÚTEO", "DELTOIDES", "MUSLO"]

    # Tipos de herida para curación
    TIPOS_HERIDA = [
        "SUPERFICIAL", "PROFUNDA", "CONTAMINADA",
        "INFECTADA", "ABRASIÓN", "LACERACIÓN",
    ]

    # Materiales de curación
    MATERIALES_CURACION = [
        "GASA", "SSN 0.9%", "AGUA ESTÉRIL",
        "JABÓN QUIRÚRGICO", "POVIDONA YODADA", "APÓSITO",
    ]

    # Tipos de sutura
    TIPOS_SUTURA = ["SIMPLE", "CONTINUA", "COLCHONERO"]

    # Zona de inmovilización y tipo de venda
    ZONAS_INMOVILIZACION = [
        "TOBILLO DERECHO",
        "TOBILLO IZQUIERDO",
        "MUÑECA DERECHA",
        "MUÑECA IZQUIERDA",
        "RODILLA DERECHA",
        "RODILLA IZQUIERDA",
        "CODO DERECHO",
        "CODO IZQUIERDO",
        "COLUMNA CERVICAL",
        "COLUMNA LUMBAR",
        "HOMBRO DERECHO",
        "HOMBRO IZQUIERDO",
        "MANO DERECHA",
        "MANO IZQUIERDA",
        "PIE DERECHO",
        "PIE IZQUIERDO",
    ]

    TIPOS_INMOVILIZACION = [
        "VENDA ELÁSTICA",
        "VENDA DE YESO",
        "VENDA DE ALGODÓN",
        "FÉRULA",
        "CABESTRILLO",
        "COLLAR CERVICAL",
    ]

    MEDIDAS_VENDA = [
        "5x5",
        "8x8",
        "10x10",
        "12x12",
        "15x15",
    ]

    # Tipos de anestesia
    TIPOS_ANESTESIA = ["ANESTESIA LOCAL", "ANESTESIA TÓPICA"]

    # Laboratorios disponibles
    LABORATORIOS_DISPONIBLES = [
        "CUADRO HEMÁTICO (CH)",
        "PARCIAL DE ORINA (PO)",
        "COPROLÓGICO",
        "BILIRRUBINA TOTAL",
        "BILIRRUBINA DIRECTA",
        "GLUCOMETRÍA",
        "CREATININA",
    ]

    def __init__(self, tipo: str):
        self.tipo: str = tipo
        self.medicamentos: list = []
        self.paciente_tolera: bool = True
        self.descripcion: str = ""

        # Canalización — soporte para 1 o 2 catéteres
        self.tipo_cateter: str = ""
        self.vena_acceso: str = ""
        self.con_tapon: bool = False
        self.solucion: str = ""
        # Segundo catéter (desangrados / doble acceso)
        self.segundo_cateter: bool = False
        self.tipo_cateter_2: str = ""
        self.vena_acceso_2: str = ""
        self.solucion_2: str = ""
        self.con_tapon_2: bool = False
        # Observación post-canalización
        self.queda_en_observacion: bool = False

        # Curación
        self.materiales_curacion: list = []
        self.tipo_herida: str = ""

        # Sutura
        self.tipo_anestesia: str = ""
        self.numero_puntos: int = 0
        self.tipo_sutura: str = ""
        self.control_sangrado: bool = False

        # Inyectología
        self.sitio_aplicacion: str = ""

        # Inmovilización estructurada
        self.zona_inmovilizacion: str = ""
        self.tipo_inmovilizacion: str = ""
        self.medida_venda: str = ""

        # Electrocardiograma
        self.ecg_tiene_protesis_metalica: bool = False
        self.ecg_tipo_protesis: str = ""

        # Lavado ocular
        self.lavado_ojo_afectado: str = ""        # OJO DERECHO / OJO IZQUIERDO / AMBOS
        self.lavado_motivo: str = ""

        # Monitoría fetal
        self.monitoria_semanas_gestacion: str = ""
        self.monitoria_resultado: str = ""        # REACTIVA / NO REACTIVA
        self.monitoria_plan_medico: str = ""      # EGRESO / INGRESO A URGENCIAS

        # Laboratorios
        self.laboratorios_solicitados: list = []  # lista de nombres de labs
        self.laboratorios_resultados: str = ""    # observaciones de resultados

        # Consulta externa
        self.es_consulta_externa: bool = False

    def agregar_medicamento(self, medicamento: Medicamento):
        """Agrega un medicamento al procedimiento."""
        self.medicamentos.append(medicamento)

    def tiene_medicamentos(self) -> bool:
        """Verifica si el procedimiento tiene medicamentos registrados."""
        return len(self.medicamentos) > 0

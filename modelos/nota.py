"""
Módulo: nota.py
Descripción: Modelo central que representa una nota clínica completa.
             Agrupa al paciente, procedimientos y metadatos de la nota.
"""

from datetime import datetime
from modelos.paciente import Paciente
from modelos.procedimiento import Procedimiento


class NotaClinica:
    """
    Clase central del sistema. Representa la nota clínica completa
    con todos sus componentes: paciente, procedimientos y datos de egreso.
    """

    # Tipos de nota disponibles
    TIPO_INGRESO = "NOTA DE INGRESO"
    TIPO_REVALORACION = "NOTA DE REVALORACIÓN"
    TIPO_ENTREGA_TURNO = "NOTA DE ENTREGA DE TURNO"
    TIPO_RECIBO_TURNO = "NOTA DE RECIBO DE TURNO"
    TIPO_RECOGIDA_AMBULANCIA = "NOTA DE RECOGIDA EN AMBULANCIA"
    TIPO_TRASLADO_AMBULANCIA = "NOTA DE TRASLADO EN AMBULANCIA HACIA OTRA INSTITUCIÓN"
    TIPO_HOSPITALIZACION = "NOTA DE INGRESO A HOSPITALIZACIÓN"
    TIPO_EGRESO = "NOTA DE EGRESO"

    TIPOS_DISPONIBLES = [
        TIPO_INGRESO,
        TIPO_REVALORACION,
        TIPO_ENTREGA_TURNO,
        TIPO_RECIBO_TURNO,
        TIPO_RECOGIDA_AMBULANCIA,
        TIPO_TRASLADO_AMBULANCIA,
        TIPO_HOSPITALIZACION,
        TIPO_EGRESO,
    ]

    # Modos de salida al egreso
    SALIDA_CAMINANDO = "CAMINANDO POR SUS PROPIOS MEDIOS"
    SALIDA_SILLA_RUEDAS = "EN SILLA DE RUEDAS"
    SALIDA_AMBULANCIA = "EN AMBULANCIA"

    MODOS_SALIDA = [SALIDA_CAMINANDO, SALIDA_SILLA_RUEDAS, SALIDA_AMBULANCIA]

    # Destinos de traslado
    DESTINOS_TRASLADO = [
        "OBSERVACIÓN",
        "HOSPITALIZACIÓN",
        "OTRA IPS",
        "UCI",
        "QUIRÓFANO",
    ]

    # Tipos de ambulancia
    AMBULANCIA_BASICA = "BÁSICA"
    AMBULANCIA_MEDICALIZADA = "MEDICALIZADA"

    TIPOS_AMBULANCIA = [AMBULANCIA_BASICA, AMBULANCIA_MEDICALIZADA]

    def __init__(self):
        self.tipo: str = ""
        self.fecha_hora_inicio: datetime = datetime.now()
        self.fecha_hora_egreso: datetime = None
        self.paciente: Paciente = Paciente()
        self.medico_turno: str = ""
        self.procedimientos: list = []
        self.texto_final: str = ""

        # Datos de egreso
        self.medico_ordena_egreso: bool = False
        self.entrega_recomendaciones: bool = False
        self.explica_signos_alarma: bool = False
        self.modo_salida: str = ""
        self.estado_egreso: str = ""
        self.observaciones_egreso: str = ""

        # Datos de traslado
        self.destino_traslado: str = ""
        self.tipo_ambulancia: str = ""
        self.paciente_estable_traslado: bool = False
        self.acompanado_personal_salud: bool = False
        self.observaciones_traslado: str = ""

        # Datos de observación
        self.paciente_consciente: bool = True
        self.paciente_orientado: bool = True
        self.monitoreo_continuo: bool = False
        self.sintomas_observacion: str = ""

        # Cierre de nota: observación o egreso
        self.queda_en_observacion: bool = False

        # Plan médico ordenado por el médico
        self.ordenes_plan_medico: list = []  # lista de strings de órdenes

        # Consulta externa
        self.es_consulta_externa: bool = False
        self.procedimientos_consulta_externa: list = []

        # Revaloración
        self.revaloracion_agregar_signos: bool = False     # radio: agregar nuevos signos?
        self.revaloracion_plan: str = ""                   # MEDICAMENTO|EGRESO|HOSPITALIZACION|REMISION
        self.revaloracion_destino_hospitalizacion: str = ""
        self.revaloracion_destino_remision: str = ""
        self.revaloracion_labs_revisados: bool = False     # médico revisó labs
        self.revaloracion_labs_descritos: list = []        # qué labs revisó
        self.revaloracion_cierre: str = ""                 # EGRESO|HOSPITALIZACION|REMISION|OBSERVACION|HABITACION
        self.revaloracion_complicacion: bool = False       # hubo complicación
        self.revaloracion_desc_complicacion: str = ""
        self.revaloracion_carro_rojo: bool = False
        self.revaloracion_maniobras_carro: list = []       # lo usado del carro rojo
        self.revaloracion_medicamentos_carro: list = []    # medicamentos del carro rojo

        # Entrega de turno
        self.entrega_auxiliar_entrega: str = ""
        self.entrega_auxiliar_recibe: str = ""
        self.entrega_refiere_malestar: bool = False
        self.entrega_tipo_orden: str = "MEDICAMENTO"   # MEDICAMENTO|EKG|LABORATORIO|PROCEDIMIENTO
        self.entrega_medicamento_malestar: str = ""
        self.entrega_presentacion_malestar: str = ""
        self.entrega_cantidad_malestar: str = ""
        self.entrega_via_malestar: str = ""
        self.entrega_labs_malestar: list = []
        self.entrega_procedimiento_malestar: str = ""

        # Recibo de turno
        self.recibo_auxiliar_entrega: str = ""
        self.recibo_auxiliar_recibe: str = ""
        self.recibo_refiere_malestar: bool = False
        self.recibo_tipo_orden: str = "MEDICAMENTO"
        self.recibo_medicamento_malestar: str = ""
        self.recibo_presentacion_malestar: str = ""
        self.recibo_cantidad_malestar: str = ""
        self.recibo_via_malestar: str = ""
        self.recibo_labs_malestar: list = []
        self.recibo_procedimiento_malestar: str = ""

        # Flags especiales
        self.notificar_medico: bool = False
        self.es_soat: bool = False
        self.tipo_accidente_soat: str = ""

    def agregar_procedimiento(self, procedimiento: Procedimiento):
        """Agrega un procedimiento a la nota clínica."""
        self.procedimientos.append(procedimiento)

    def registrar_hora_egreso(self):
        """Registra la hora de egreso del paciente."""
        self.fecha_hora_egreso = datetime.now()

    def tiene_procedimientos(self) -> bool:
        """Verifica si la nota tiene procedimientos registrados."""
        return len(self.procedimientos) > 0

    def obtener_tipos_procedimiento(self) -> list:
        """Retorna la lista de tipos de procedimiento registrados."""
        return [proc.tipo for proc in self.procedimientos]

    # Tipos de nota disponibles para consulta externa
    TIPO_CONSULTA_EXTERNA = "NOTA DE CONSULTA EXTERNA"

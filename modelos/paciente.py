"""
Módulo: paciente.py
Descripción: Modelo que representa los datos básicos del paciente
             necesarios para construir la nota clínica.
"""


class Paciente:
    """
    Clase que encapsula los datos demográficos y clínicos del paciente.
    No almacena información de forma persistente.
    """

    # Constantes de sexo
    SEXO_MASCULINO = "MASCULINO"
    SEXO_FEMENINO = "FEMENINO"

    # Constantes de modo de ingreso
    INGRESO_CAMINANDO = "CAMINANDO POR SUS PROPIOS MEDIOS"
    INGRESO_SILLA_RUEDAS = "EN SILLA DE RUEDAS"
    INGRESO_CAMILLA = "EN CAMILLA"
    INGRESO_AMBULANCIA = "EN AMBULANCIA"

    MODOS_INGRESO = [
        INGRESO_CAMINANDO,
        INGRESO_SILLA_RUEDAS,
        INGRESO_CAMILLA,
        INGRESO_AMBULANCIA,
    ]

    # Constantes de estado general
    ESTADO_ESTABLE = "ESTABLE"
    ESTADO_REGULAR = "REGULAR"
    ESTADO_CRITICO = "CRÍTICO"

    ESTADOS_GENERALES = [ESTADO_ESTABLE, ESTADO_REGULAR, ESTADO_CRITICO]

    def __init__(self):
        self.sexo: str = ""
        self.edad: int = 0
        self.condicion_etaria: str = ""
        self.modo_ingreso: str = ""
        self.motivo_consulta: str = ""
        self.estado_general: str = ""
        self.acompanante: str = ""
        self.es_gestante: bool = False      # Solo aplica si sexo=FEMENINO y edad >= 13
        self.semanas_gestacion: str = ""    # Opcional, para el bloque de ingreso

        # Signos vitales
        self.tension_arterial: str = ""
        self.frecuencia_cardiaca: str = ""
        self.frecuencia_respiratoria: str = ""
        self.temperatura: str = ""
        self.saturacion_oxigeno: str = ""
        self.talla: str = ""
        self.peso: str = ""

    def establecer_edad(self, edad: int):
        """Establece la edad y determina automáticamente la condición etaria."""
        self.edad = edad
        self.condicion_etaria = "MENOR DE EDAD" if edad < 18 else "MAYOR DE EDAD"

    def tiene_signos_vitales(self) -> bool:
        """Verifica si se registró al menos un signo vital."""
        return any([
            self.tension_arterial,
            self.frecuencia_cardiaca,
            self.frecuencia_respiratoria,
            self.temperatura,
            self.saturacion_oxigeno,
        ])

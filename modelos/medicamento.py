"""
Módulo: medicamento.py
Descripción: Modelo que representa un medicamento administrado al paciente
             durante un procedimiento clínico.
"""


class Medicamento:
    """
    Clase que encapsula los datos de un medicamento administrado.
    Genera su propio bloque de texto clínico al ser solicitado.
    """

    # Vías de administración
    VIA_INTRAVENOSA = "INTRAVENOSA"
    VIA_INTRAMUSCULAR = "INTRAMUSCULAR"
    VIA_SUBCUTANEA = "SUBCUTÁNEA"
    VIA_ORAL = "ORAL"
    EN_LOS_LIQUIDOS = "EN LOS LÍQUIDOS"

    VIAS_ADMINISTRACION = [
        VIA_INTRAVENOSA,
        VIA_INTRAMUSCULAR,
        VIA_SUBCUTANEA,
        VIA_ORAL,
        EN_LOS_LIQUIDOS,
    ]

    # Presentaciones disponibles
    PRESENTACIONES = [
        "AMPOLLA",
        "FRASCO",
        "TABLETA",
        "CÁPSULA",
        "SOLUCIÓN",
        "SUSPENSIÓN",
        "SUPOSITORIO",
        "PARCHE",
    ]

    def __init__(self):
        self.nombre: str = ""
        self.presentacion: str = ""
        self.cantidad: str = ""
        self.via_administracion: str = ""
        self.hora_administracion: str = ""
        self.paciente_tolera: bool = True
        self.observaciones: str = ""

    def generar_texto(self) -> str:
        """Genera el fragmento de texto clínico para este medicamento."""
        texto = (
            f"SE ADMINISTRA {self.cantidad} {self.presentacion} "
            f"DE {self.nombre.upper()} POR VÍA {self.via_administracion}."
        )
        if not self.paciente_tolera:
            texto += " PACIENTE REFIERE NO TOLERAR EL PROCEDIMIENTO."
        if self.observaciones:
            texto += f" {self.observaciones.upper()}."
        return texto

    def esta_completo(self) -> bool:
        """Verifica que el medicamento tenga los campos mínimos requeridos."""
        return all([
            self.nombre,
            self.presentacion,
            self.cantidad,
            self.via_administracion,
        ])

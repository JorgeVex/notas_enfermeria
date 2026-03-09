"""
Módulo: estadisticas.py
Descripción: Modelo que representa un registro de estadística de uso.
             No almacena datos clínicos del paciente.
"""

from datetime import datetime


class RegistroEstadistico:
    """
    Clase que representa un registro estadístico de una nota generada.
    Solo almacena metadatos de uso, nunca datos clínicos del paciente.
    """

    def __init__(self, tipo_nota: str, tipos_procedimiento: list):
        self.fecha: str = datetime.now().strftime("%Y-%m-%d")
        self.hora: str = datetime.now().strftime("%H:%M:%S")
        self.tipo_nota: str = tipo_nota
        self.tipos_procedimiento: list = tipos_procedimiento

    def a_diccionario(self) -> dict:
        """Convierte el registro a diccionario para serialización JSON."""
        return {
            "fecha": self.fecha,
            "hora": self.hora,
            "tipo_nota": self.tipo_nota,
            "tipos_procedimiento": self.tipos_procedimiento,
        }

    @classmethod
    def desde_diccionario(cls, datos: dict) -> "RegistroEstadistico":
        """Crea un registro desde un diccionario deserializado."""
        registro = cls(
            tipo_nota=datos.get("tipo_nota", ""),
            tipos_procedimiento=datos.get("tipos_procedimiento", []),
        )
        registro.fecha = datos.get("fecha", "")
        registro.hora = datos.get("hora", "")
        return registro

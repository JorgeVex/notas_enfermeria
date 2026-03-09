"""
Módulo: utilidades_fecha.py
Descripción: Funciones utilitarias para manejo de fechas y horas
             utilizadas en la generación de notas clínicas.
"""

from datetime import datetime


def obtener_fecha_hora_actual() -> str:
    """Retorna la fecha y hora actual en formato clínico legible."""
    ahora = datetime.now()
    return ahora.strftime("%d/%m/%Y %H:%M")


def obtener_fecha_actual() -> str:
    """Retorna la fecha actual en formato dd/mm/yyyy."""
    return datetime.now().strftime("%d/%m/%Y")


def obtener_hora_actual() -> str:
    """Retorna la hora actual en formato HH:MM."""
    return datetime.now().strftime("%H:%M")


def formatear_fecha_hora(fecha_hora: datetime) -> str:
    """Formatea un objeto datetime al formato clínico estándar."""
    return fecha_hora.strftime("%d/%m/%Y %H:%M")


def formatear_hora(fecha_hora: datetime) -> str:
    """Extrae y formatea solo la hora de un objeto datetime."""
    return fecha_hora.strftime("%H:%M")


def obtener_fecha_para_archivo() -> str:
    """Retorna la fecha actual formateada para uso en nombres de archivo."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

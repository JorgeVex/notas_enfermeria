"""
Módulo: servicio_estadisticas.py
Descripción: Servicio que gestiona el registro y consulta de estadísticas
             de uso del sistema. No almacena datos clínicos del paciente.
"""

import json
import os
from collections import Counter
from modelos.estadisticas import RegistroEstadistico


class ServicioEstadisticas:
    """
    Servicio que registra y consulta el uso del sistema de notas clínicas.
    Persiste los datos en un archivo JSON sin información del paciente.
    """

    RUTA_ARCHIVO = os.path.join("datos", "estadisticas_uso.json")

    def __init__(self):
        self._asegurar_archivo()

    def _asegurar_archivo(self):
        """Crea el archivo de estadísticas si no existe."""
        carpeta = os.path.dirname(self.RUTA_ARCHIVO)
        if carpeta and not os.path.exists(carpeta):
            os.makedirs(carpeta)
        if not os.path.exists(self.RUTA_ARCHIVO):
            self._guardar_registros([])

    def registrar_nota(self, tipo_nota: str, tipos_procedimiento: list):
        """
        Registra una nueva nota generada en el historial de estadísticas.

        Parámetros:
            tipo_nota: Tipo de nota clínica generada.
            tipos_procedimiento: Lista de tipos de procedimientos realizados.
        """
        registro = RegistroEstadistico(tipo_nota, tipos_procedimiento)
        registros = self._cargar_registros()
        registros.append(registro.a_diccionario())
        self._guardar_registros(registros)

    def obtener_total_notas(self) -> int:
        """Retorna el total de notas generadas históricamente."""
        return len(self._cargar_registros())

    def obtener_notas_por_dia(self, fecha: str) -> int:
        """
        Retorna el número de notas generadas en una fecha específica.

        Parámetros:
            fecha: Fecha en formato YYYY-MM-DD.
        """
        registros = self._cargar_registros()
        return sum(1 for r in registros if r.get("fecha") == fecha)

    def obtener_notas_por_mes(self, anio: int, mes: int) -> int:
        """
        Retorna el número de notas generadas en un mes y año específicos.

        Parámetros:
            anio: Año en formato entero (ej: 2025).
            mes: Mes en formato entero (1-12).
        """
        prefijo = f"{anio}-{mes:02d}"
        registros = self._cargar_registros()
        return sum(1 for r in registros if r.get("fecha", "").startswith(prefijo))

    def obtener_tipos_nota_frecuentes(self, top: int = 5) -> list:
        """
        Retorna los tipos de nota más frecuentes.

        Parámetros:
            top: Número de tipos a retornar.

        Retorna:
            Lista de tuplas (tipo_nota, cantidad).
        """
        registros = self._cargar_registros()
        tipos = [r.get("tipo_nota", "") for r in registros]
        return Counter(tipos).most_common(top)

    def obtener_procedimientos_frecuentes(self, top: int = 5) -> list:
        """
        Retorna los procedimientos más frecuentes.

        Parámetros:
            top: Número de procedimientos a retornar.

        Retorna:
            Lista de tuplas (tipo_procedimiento, cantidad).
        """
        registros = self._cargar_registros()
        procedimientos = []
        for r in registros:
            procedimientos.extend(r.get("tipos_procedimiento", []))
        return Counter(procedimientos).most_common(top)

    def obtener_resumen(self) -> dict:
        """
        Retorna un resumen general de las estadísticas de uso.
        """
        from datetime import datetime
        ahora = datetime.now()
        return {
            "total_notas": self.obtener_total_notas(),
            "notas_hoy": self.obtener_notas_por_dia(
                ahora.strftime("%Y-%m-%d")
            ),
            "notas_este_mes": self.obtener_notas_por_mes(
                ahora.year, ahora.month
            ),
            "tipos_frecuentes": self.obtener_tipos_nota_frecuentes(),
            "procedimientos_frecuentes": self.obtener_procedimientos_frecuentes(),
        }

    def _cargar_registros(self) -> list:
        """Carga los registros desde el archivo JSON."""
        try:
            with open(self.RUTA_ARCHIVO, "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _guardar_registros(self, registros: list):
        """Guarda los registros en el archivo JSON."""
        with open(self.RUTA_ARCHIVO, "w", encoding="utf-8") as archivo:
            json.dump(registros, archivo, ensure_ascii=False, indent=2)

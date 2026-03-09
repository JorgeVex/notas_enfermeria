"""
Módulo: exportador_archivo.py
Descripción: Servicio encargado de exportar la nota clínica generada
             a un archivo de texto (.txt) listo para copiar al sistema de la IPS.
"""

import os
from utilidades.utilidades_fecha import obtener_fecha_para_archivo


class ExportadorArchivo:
    """
    Servicio que gestiona la exportación de notas clínicas a archivos .txt.
    """

    CARPETA_EXPORTACION = "notas_generadas"

    def __init__(self):
        self._asegurar_carpeta_exportacion()

    def _asegurar_carpeta_exportacion(self):
        """Crea la carpeta de exportación si no existe."""
        if not os.path.exists(self.CARPETA_EXPORTACION):
            os.makedirs(self.CARPETA_EXPORTACION)

    def exportar(self, texto_nota: str, tipo_nota: str,
                  ruta_personalizada: str = None) -> str:
        """
        Exporta el texto de la nota a un archivo .txt.

        Parámetros:
            texto_nota: Texto completo de la nota generada.
            tipo_nota: Tipo de nota para nombrar el archivo.
            ruta_personalizada: Si se proporciona, guarda en esa ruta.

        Retorna:
            Ruta absoluta del archivo generado.
        """
        if ruta_personalizada:
            ruta_archivo = ruta_personalizada
        else:
            nombre_archivo = self._generar_nombre_archivo(tipo_nota)
            ruta_archivo = os.path.join(self.CARPETA_EXPORTACION, nombre_archivo)

        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            archivo.write(texto_nota)

        return os.path.abspath(ruta_archivo)

    def _generar_nombre_archivo(self, tipo_nota: str) -> str:
        """Genera un nombre de archivo único basado en el tipo de nota y la fecha."""
        tipo_limpio = tipo_nota.replace(" ", "_").replace("/", "-")
        marca_tiempo = obtener_fecha_para_archivo()
        return f"{tipo_limpio}_{marca_tiempo}.txt"

    def leer_archivo(self, ruta: str) -> str:
        """Lee el contenido de un archivo .txt exportado."""
        if not os.path.exists(ruta):
            raise FileNotFoundError(f"No se encontró el archivo: {ruta}")
        with open(ruta, "r", encoding="utf-8") as archivo:
            return archivo.read()

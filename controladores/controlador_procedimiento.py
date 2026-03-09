"""
Módulo: controlador_procedimiento.py
Descripción: Controlador que gestiona la lógica de selección y
             configuración de procedimientos clínicos en la interfaz.
"""

from modelos.procedimiento import Procedimiento
from modelos.medicamento import Medicamento


class ControladorProcedimiento:
    """
    Controlador auxiliar para la gestión de procedimientos.
    Determina qué campos activar en la interfaz según el procedimiento seleccionado.
    """

    @staticmethod
    def obtener_campos_requeridos(tipo: str) -> dict:
        """
        Retorna los campos requeridos para un tipo de procedimiento.

        Parámetros:
            tipo: Tipo de procedimiento.

        Retorna:
            Diccionario con los campos y si son requeridos.
        """
        campos = {
            Procedimiento.TIPO_CANALIZACION: {
                "tipo_cateter": True,
                "con_tapon": False,
                "solucion": False,
                "medicamentos": False,
            },
            Procedimiento.TIPO_INYECTOLOGIA: {
                "sitio_aplicacion": True,
                "medicamentos": True,
            },
            Procedimiento.TIPO_CURACION: {
                "tipo_herida": True,
                "materiales_curacion": False,
                "descripcion": False,
            },
            Procedimiento.TIPO_SUTURA: {
                "tipo_anestesia": True,
                "numero_puntos": True,
                "tipo_sutura": True,
                "control_sangrado": False,
                "descripcion": False,
            },
            Procedimiento.TIPO_INMOVILIZACION: {
                "descripcion": True,
            },
        }
        return campos.get(tipo, {})

    @staticmethod
    def requiere_traslado_sala(tipo: str) -> bool:
        """
        Indica si el procedimiento requiere traslado a una sala específica.
        Importante para auditorías SOAT.
        """
        return tipo in [Procedimiento.TIPO_CURACION, Procedimiento.TIPO_SUTURA]

    @staticmethod
    def crear_medicamento_vacio() -> Medicamento:
        """Crea una instancia de medicamento vacía lista para ser completada."""
        return Medicamento()

    @staticmethod
    def validar_procedimiento(procedimiento: Procedimiento) -> list:
        """
        Valida los datos de un procedimiento.

        Retorna:
            Lista de mensajes de error (vacía si todo es válido).
        """
        errores = []
        tipo = procedimiento.tipo

        if tipo == Procedimiento.TIPO_CANALIZACION:
            if not procedimiento.tipo_cateter:
                errores.append("Debe seleccionar el tipo de catéter.")

        elif tipo == Procedimiento.TIPO_INYECTOLOGIA:
            if not procedimiento.sitio_aplicacion:
                errores.append("Debe seleccionar el sitio de aplicación.")
            if not procedimiento.tiene_medicamentos():
                errores.append("Debe agregar al menos un medicamento para inyectología.")

        elif tipo == Procedimiento.TIPO_CURACION:
            if not procedimiento.tipo_herida:
                errores.append("Debe seleccionar el tipo de herida.")

        elif tipo == Procedimiento.TIPO_SUTURA:
            if not procedimiento.tipo_anestesia:
                errores.append("Debe seleccionar el tipo de anestesia.")
            if procedimiento.numero_puntos <= 0:
                errores.append("Debe ingresar el número de puntos.")
            if not procedimiento.tipo_sutura:
                errores.append("Debe seleccionar el tipo de sutura.")

        return errores

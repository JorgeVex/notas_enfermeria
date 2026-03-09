"""
Módulo: controlador_app.py
Descripción: Controlador principal de la aplicación. Coordina la
             navegación entre vistas y el ciclo de vida de la app.
"""

from controladores.controlador_nota import ControladorNota
from servicios.servicio_estadisticas import ServicioEstadisticas


class ControladorApp:
    """
    Controlador raíz de la aplicación.
    Gestiona el estado global y la navegación entre pantallas.
    """

    def __init__(self):
        self.controlador_nota = ControladorNota()
        self.servicio_estadisticas = ServicioEstadisticas()
        self.ventana_principal = None

    def establecer_ventana_principal(self, ventana):
        """Registra la referencia a la ventana principal de la app."""
        self.ventana_principal = ventana

    def obtener_resumen_estadisticas(self) -> dict:
        """Retorna el resumen de estadísticas de uso del sistema."""
        return self.servicio_estadisticas.obtener_resumen()

    def iniciar_nota(self, tipo_nota: str):
        """Inicia una nueva nota y navega a la vista de datos del paciente."""
        self.controlador_nota.iniciar_nueva_nota(tipo_nota)
        if self.ventana_principal:
            self.ventana_principal.navegar_a_formulario_paciente()

    def finalizar_y_exportar(self, ruta: str = None) -> str:
        """
        Genera el texto de la nota, la exporta y registra estadísticas.

        Retorna:
            Ruta del archivo generado.
        """
        self.controlador_nota.generar_texto_nota()
        return self.controlador_nota.exportar_nota(ruta_personalizada=ruta)

    def reiniciar(self):
        """Reinicia el controlador para iniciar una nueva nota desde cero."""
        self.controlador_nota = ControladorNota()

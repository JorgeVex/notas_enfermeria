"""
Módulo: main.py
Descripción: Punto de entrada principal de la aplicación.
             Inicializa el controlador de la app, la ventana principal
             y ejecuta el loop de eventos de PyQt5.
"""

import sys
import os

# Asegurar que el directorio raíz del proyecto esté en el path de Python
directorio_raiz = os.path.dirname(os.path.abspath(__file__))
if directorio_raiz not in sys.path:
    sys.path.insert(0, directorio_raiz)

# Cambiar el directorio de trabajo al raíz del proyecto
# para que las rutas relativas (como datos/estadisticas_uso.json) funcionen
os.chdir(directorio_raiz)

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from controladores.controlador_app import ControladorApp
from vistas.ventana_principal import VentanaPrincipal


def iniciar_aplicacion():
    """Función principal que inicializa y lanza la aplicación."""
    app = QApplication(sys.argv)
    app.setApplicationName("Sistema de Notas de Enfermería")
    app.setOrganizationName("IPS Urgencias")

    # Fuente global de la aplicación
    fuente_global = QFont("Arial", 10)
    app.setFont(fuente_global)

    # Inicializar controlador principal
    controlador = ControladorApp()

    # Crear y mostrar ventana principal
    ventana = VentanaPrincipal(controlador)
    ventana.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    iniciar_aplicacion()

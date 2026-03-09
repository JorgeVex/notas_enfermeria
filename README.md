# Sistema de Notas de Enfermería - Urgencias

Aplicación de escritorio desarrollada en Python con PyQt5 para la generación
estructurada de notas clínicas en servicios de urgencias de IPS.

## Requisitos

- Python 3.8 o superior
- PyQt5

## Instalación de dependencias

```bash
pip install PyQt5
pip install pyqt5-tools
```

## Ejecución

```bash
cd notas_enfermeria_app
python main.py
```

## Estructura del proyecto

```
notas_enfermeria_app/
│
├── main.py                          # Punto de entrada
│
├── controladores/
│   ├── controlador_app.py           # Coordinador general
│   ├── controlador_nota.py          # Lógica de la nota clínica
│   └── controlador_procedimiento.py # Lógica de procedimientos
│
├── modelos/
│   ├── paciente.py                  # Datos del paciente
│   ├── nota.py                      # Nota clínica completa
│   ├── procedimiento.py             # Procedimientos clínicos
│   ├── medicamento.py               # Medicamentos administrados
│   ├── bloque_clinico.py            # Bloques y motor de bloques
│   └── estadisticas.py              # Registro estadístico
│
├── vistas/
│   ├── ventana_principal.py         # Ventana y navegación
│   ├── vista_selector_nota.py       # Selección de tipo de nota
│   ├── vista_formulario_paciente.py # Datos del paciente
│   ├── vista_procedimientos.py      # Procedimientos y medicamentos
│   └── vista_resumen.py             # Nota generada y exportación
│
├── servicios/
│   ├── generador_nota.py            # Motor generador de texto
│   ├── exportador_archivo.py        # Exportación a .txt
│   └── servicio_estadisticas.py     # Gestión de estadísticas
│
├── utilidades/
│   ├── utilidades_fecha.py          # Manejo de fechas y horas
│   └── validadores.py               # Validación de campos
│
└── datos/
    └── estadisticas_uso.json        # Registro de uso (sin datos clínicos)
```

## Tipos de nota soportados

- Nota de ingreso
- Nota de revaloración
- Nota de entrega de turno
- Nota de recibo de turno
- Nota de recogida en ambulancia
- Nota de traslado en ambulancia hacia otra institución
- Nota de ingreso a hospitalización
- Nota de egreso

## Procedimientos soportados

- Inyectología
- Canalización
- Curación
- Sutura
- Inmovilización

## Flujo SOAT

El sistema soporta el flujo especial para pacientes accidentados
cubiertos por SOAT, documentando correctamente los traslados
secuenciales a sala de curación y sutura.

## Privacidad

La aplicación **no almacena datos clínicos del paciente**.
Solo registra estadísticas de uso (tipo de nota, fecha, hora y
tipo de procedimiento) para control interno de la institución.

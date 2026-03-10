# 🏥 Sistema de Notas de Enfermería — Urgencias

Aplicación de escritorio desarrollada en **Python + PyQt5** para la generación automática de notas clínicas estructuradas en servicios de urgencias de IPS colombianas.

> **Proyecto personal en desarrollo activo** — nació de observar en primera persona cómo los errores en las notas de enfermería generan inconsistencias en la facturación y pérdidas económicas para las instituciones. La idea es simple: que la auxiliar se enfoque en el paciente, no en redactar.

---

## ¿Qué hace?

En lugar de redactar cada nota desde cero, la auxiliar selecciona el tipo de nota, completa los campos clave y la app genera automáticamente el texto en mayúsculas con terminología clínica correcta, listo para copiar al sistema de la IPS.

**Sin errores ortográficos. Sin elementos sin justificar. En segundos.**

---

## Tipos de nota soportados

| Tipo | Descripción |
|------|-------------|
| 📋 Nota de ingreso | Ingreso inicial del paciente a urgencias |
| 🔄 Nota de revaloración | Seguimiento con nuevo plan médico |
| 🤝 Entrega de turno | Traspaso entre auxiliares con estado del paciente |
| 📥 Recibo de turno | Recepción formal del turno |
| 🚑 Recogida en ambulancia | Atención prehospitalaria |
| 🚐 Traslado en ambulancia | Remisión a otra institución |
| 🏨 Ingreso a hospitalización | Paso de urgencias a hospitalización |
| 🚪 Nota de egreso | Salida del paciente con indicaciones |

---

## Procedimientos soportados

- Inyectología
- Canalización (simple o doble vía, con 24 opciones de acceso venoso)
- Curación
- Sutura
- Inmovilización
- Electrocardiograma
- Lavado ocular
- Monitoría fetal
- Laboratorios

---

## 🔒 Privacidad

La aplicación **no almacena ningún dato clínico del paciente**.
Solo registra estadísticas de uso anónimas (tipo de nota, fecha, hora, procedimientos) para control interno.

---

## 🚀 Potencial de escalabilidad

Cada nota generada es un dato estructurado. A futuro, el sistema puede alimentar análisis estadísticos reales para las IPS:
- Procedimientos más frecuentes por turno
- Carga asistencial por franja horaria
- Patologías predominantes
- Indicadores para toma de decisiones clínicas y administrativas

---

## Instalación y ejecución

**Requisitos:** Python 3.8 o superior

```bash
# Instalar dependencias
pip install PyQt5

# Ejecutar
cd notas_enfermeria_app
python main.py
```

**¿Sin Python instalado?** El repositorio incluye `compilar_exe.bat` para generar un ejecutable `.exe` de Windows con un solo clic.

---

## Estructura del proyecto

```
notas_enfermeria_app/
├── main.py
├── controladores/
│   ├── controlador_app.py
│   ├── controlador_nota.py
│   └── controlador_procedimiento.py
├── modelos/
│   ├── paciente.py
│   ├── nota.py
│   ├── procedimiento.py
│   ├── medicamento.py
│   ├── bloque_clinico.py
│   └── estadisticas.py
├── vistas/
│   ├── ventana_principal.py
│   ├── vista_selector_nota.py
│   ├── vista_formulario_paciente.py
│   ├── vista_procedimientos.py
│   ├── vista_revaloracion.py
│   ├── vista_turno.py
│   └── vista_resumen.py
├── servicios/
│   ├── generador_nota.py
│   ├── exportador_archivo.py
│   └── servicio_estadisticas.py
├── utilidades/
│   ├── utilidades_fecha.py
│   └── validadores.py
└── datos/
    └── estadisticas_uso.json
```

---

## Stack tecnológico

- **Python 3.8+**
- **PyQt5** — interfaz gráfica de escritorio
- **PyInstaller** — generación de ejecutable Windows
- Desarrollado con asistencia de **Claude (Anthropic)** 🤖

---

*Proyecto personal en fase beta. Desarrollado por un técnico en Análisis y Desarrollo de Software, actualmente estudiante de Ingeniería en Ciencia de Datos, desde la experiencia directa en facturación de urgencias.*
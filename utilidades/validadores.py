"""
Módulo: validadores.py
Descripción: Funciones de validación de campos del formulario
             antes de generar la nota clínica.
"""


def validar_edad(valor: str) -> tuple:
    """
    Valida que la edad ingresada sea un número entero positivo.
    Retorna (es_valido: bool, mensaje: str)
    """
    if not valor.strip():
        return False, "La edad es obligatoria."
    try:
        edad = int(valor.strip())
        if edad <= 0 or edad > 130:
            return False, "La edad debe estar entre 1 y 130 años."
        return True, ""
    except ValueError:
        return False, "La edad debe ser un número entero."


def validar_campo_requerido(valor: str, nombre_campo: str) -> tuple:
    """
    Valida que un campo de texto requerido no esté vacío.
    Retorna (es_valido: bool, mensaje: str)
    """
    if not valor or not valor.strip():
        return False, f"El campo '{nombre_campo}' es obligatorio."
    return True, ""


def validar_numero_positivo(valor: str, nombre_campo: str) -> tuple:
    """
    Valida que un valor sea un número entero positivo mayor a cero.
    Retorna (es_valido: bool, mensaje: str)
    """
    if not valor.strip():
        return False, f"El campo '{nombre_campo}' es obligatorio."
    try:
        numero = int(valor.strip())
        if numero <= 0:
            return False, f"'{nombre_campo}' debe ser mayor a cero."
        return True, ""
    except ValueError:
        return False, f"'{nombre_campo}' debe ser un número entero."


def validar_seleccion(valor: str, nombre_campo: str) -> tuple:
    """
    Valida que se haya seleccionado una opción en un campo de selección.
    Retorna (es_valido: bool, mensaje: str)
    """
    if not valor or valor.strip() == "":
        return False, f"Debe seleccionar una opción para '{nombre_campo}'."
    return True, ""


def validar_nota_basica(tipo_nota: str, sexo: str,
                         edad: str, medico: str) -> list:
    """
    Valida los campos mínimos requeridos para generar cualquier nota.
    Retorna lista de mensajes de error (vacía si todo es válido).
    """
    errores = []

    valido, msg = validar_seleccion(tipo_nota, "Tipo de nota")
    if not valido:
        errores.append(msg)

    valido, msg = validar_seleccion(sexo, "Sexo del paciente")
    if not valido:
        errores.append(msg)

    valido, msg = validar_edad(edad)
    if not valido:
        errores.append(msg)

    valido, msg = validar_campo_requerido(medico, "Médico de turno")
    if not valido:
        errores.append(msg)

    return errores

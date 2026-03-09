"""
Módulo: bloque_clinico.py
Descripción: Clase BloqueClinico que representa fragmentos reutilizables
             de texto clínico, y MotorBloques que los genera y administra.
"""


class BloqueClinico:
    """
    Representa un fragmento reutilizable de texto clínico.
    Cada bloque encapsula una parte específica de la nota.
    """

    def __init__(self, identificador: str, texto: str):
        self.identificador: str = identificador
        self.texto: str = texto

    def __str__(self) -> str:
        return self.texto


class MotorBloques:
    """
    Repositorio central de bloques clínicos reutilizables.
    Genera cada bloque según los datos recibidos.
    Permite ensamblar notas de distintos tipos sin duplicar lógica.
    """

    @staticmethod
    def bloque_encabezado(fecha_hora: str) -> BloqueClinico:
        """Genera el bloque de encabezado con fecha y hora."""
        return BloqueClinico(
            "encabezado",
            f"FECHA Y HORA: {fecha_hora}"
        )

    @staticmethod
    def bloque_ingreso_paciente(sexo: str, condicion: str, edad: int,
                                 modo: str, acompanante: str = "",
                                 es_gestante: bool = False,
                                 semanas_gestacion: str = "") -> BloqueClinico:
        """Genera el bloque de ingreso del paciente."""
        texto = (
            f"INGRESA PACIENTE {sexo} {condicion} DE {edad} AÑOS DE EDAD "
            f"{modo}"
        )
        if acompanante:
            texto += f", ACOMPAÑADO(A) POR {acompanante.upper()}"
        texto += "."
        if es_gestante:
            if semanas_gestacion:
                texto += (
                    f" PACIENTE REFIERE ESTAR EN ESTADO DE EMBARAZO DE "
                    f"{semanas_gestacion} SEMANAS DE GESTACIÓN."
                )
            else:
                texto += " PACIENTE REFIERE ESTAR EN ESTADO DE EMBARAZO."
        return BloqueClinico("ingreso_paciente", texto)

    @staticmethod
    def bloque_motivo_consulta(motivo: str) -> BloqueClinico:
        """Genera el bloque del motivo de consulta referido por el paciente."""
        return BloqueClinico(
            "motivo_consulta",
            f'QUIEN REFIERE: "{motivo.upper()}".'
        )

    @staticmethod
    def bloque_signos_vitales(ta: str = "", fc: str = "", fr: str = "",
                               temp: str = "", spo2: str = "",
                               talla: str = "", peso: str = "") -> BloqueClinico:
        """Genera el bloque de signos vitales con los datos disponibles."""
        partes = ["SE REALIZA TOMA DE SIGNOS VITALES:"]
        if ta:    partes.append(f"TENSIÓN ARTERIAL: {ta} MMHG")
        if fc:    partes.append(f"FRECUENCIA CARDÍACA: {fc} LPM")
        if fr:    partes.append(f"FRECUENCIA RESPIRATORIA: {fr} RPM")
        if temp:  partes.append(f"TEMPERATURA: {temp} °C")
        if spo2:  partes.append(f"SATURACIÓN DE OXÍGENO: {spo2}%")
        if talla: partes.append(f"TALLA: {talla} CM")
        if peso:  partes.append(f"PESO: {peso} KG")
        return BloqueClinico("signos_vitales", " | ".join(partes) + ".")

    @staticmethod
    def bloque_valoracion_medica(nombre_medico: str,
                                  tiene_plan: bool = False) -> BloqueClinico:
        """
        Genera el bloque de valoración por el médico de turno.
        Si tiene_plan es True, omite el sufijo 'QUIEN ORDENA NUEVO PLAN'
        porque el plan aparece en bloque_plan_medico.
        """
        if tiene_plan:
            texto = (
                f"PACIENTE ES VALORADO POR MÉDICO DE TURNO DR(A). "
                f"{nombre_medico.upper()}."
            )
        else:
            texto = (
                f"PACIENTE ES VALORADO POR MÉDICO DE TURNO DR(A). "
                f"{nombre_medico.upper()}, QUIEN ORDENA NUEVO PLAN."
            )
        return BloqueClinico("valoracion_medica", texto)

    @staticmethod
    def bloque_ocho_correctos() -> BloqueClinico:
        """Genera el bloque de verificación de los 8 correctivos de medicamentos."""
        return BloqueClinico(
            "ocho_correctos",
            "SE CUMPLE CON ORDEN MÉDICA APLICANDO LOS 8 CORRECTIVOS "
            "DE ADMINISTRACIÓN DE MEDICAMENTOS."
        )

    @staticmethod
    def bloque_medicamento(cantidad: str, presentacion: str,
                            nombre: str, via: str) -> BloqueClinico:
        """Genera el bloque de administración de un medicamento."""
        return BloqueClinico(
            "medicamento",
            f"SE ADMINISTRA {cantidad} {presentacion} DE "
            f"{nombre.upper()} POR VÍA {via}."
        )

    @staticmethod
    def bloque_canalizacion(tipo_cateter: str, vena_acceso: str,
                             con_tapon: bool, solucion: str = "",
                             es_segunda_via: bool = False) -> BloqueClinico:
        """Genera el bloque de canalización para UN catéter.
        Llamar dos veces para doble acceso (es_segunda_via=True en la segunda).
        """
        vena = f" EN {vena_acceso.upper()}" if vena_acceso else ""
        if es_segunda_via:
            texto = f""
        else:
            texto = f""
        if con_tapon:
            texto += " CON TAPÓN"
        if solucion:
            texto += f", SE INICIA INFUSIÓN DE {solucion}"
        texto += ". PACIENTE TOLERA PROCEDIMIENTO."
        return BloqueClinico("canalizacion", texto)

    @staticmethod
    def bloque_observacion_cierre() -> BloqueClinico:
        """Bloque de cierre: paciente queda en observación esperando revaloración."""
        return BloqueClinico(
            "observacion_cierre",
            "PACIENTE QUEDA EN SALA DE OBSERVACIÓN A LA ESPERA "
            "DE REVALORACIÓN MÉDICA POR PARTE DEL MÉDICO DE TURNO."
        )

    @staticmethod
    def bloque_traslado_curacion() -> BloqueClinico:
        """Genera el bloque de traslado a sala de curación."""
        return BloqueClinico(
            "traslado_curacion",
            "SE TRASLADA PACIENTE A SALA DE CURACIÓN."
        )

    @staticmethod
    def bloque_curacion(tipo_herida: str, materiales: list,
                         descripcion: str = "") -> BloqueClinico:
        """Genera el bloque del procedimiento de curación."""
        materiales_str = ", ".join(materiales) if materiales else "MATERIAL ESTÉRIL"
        texto = (
            f"SE REALIZA PROCEDIMIENTO DE CURACIÓN DE HERIDA {tipo_herida.upper()} "
            f"UTILIZANDO {materiales_str}."
        )
        if descripcion:
            texto += f" {descripcion.upper()}."
        texto += " PACIENTE TOLERA PROCEDIMIENTO."
        return BloqueClinico("curacion", texto)

    @staticmethod
    def bloque_traslado_sutura() -> BloqueClinico:
        """Genera el bloque de traslado a sala de sutura."""
        return BloqueClinico(
            "traslado_sutura",
            "SE TRASLADA PACIENTE A SALA DE SUTURA."
        )

    @staticmethod
    def bloque_sutura(anestesia: str, num_puntos: int,
                       tipo_sutura: str, descripcion: str = "") -> BloqueClinico:
        """Genera el bloque del procedimiento de sutura."""
        texto = (
            f"SE APLICA {anestesia.upper()} Y SE REALIZA SUTURA "
            f"{tipo_sutura.upper()} CON {num_puntos} PUNTO(S)."
        )
        if descripcion:
            texto += f" {descripcion.upper()}."
        texto += " PACIENTE TOLERA PROCEDIMIENTO."
        return BloqueClinico("sutura", texto)

    @staticmethod
    def bloque_inyectologia(sitio: str) -> BloqueClinico:
        """Genera el bloque de inyectología."""
        return BloqueClinico(
            "inyectologia",
            f"SE REALIZA PROCEDIMIENTO DE INYECTOLOGÍA EN REGIÓN {sitio.upper()}. "
            f"PACIENTE TOLERA PROCEDIMIENTO."
        )

    @staticmethod
    def bloque_inmovilizacion(zona: str, tipo_inmovilizacion: str,
                               medida_venda: str, descripcion: str = "") -> BloqueClinico:
        """Genera el bloque del procedimiento de inmovilización con vendas."""
        texto = (
            f"SE TRASLADA PACIENTE A SALA DE PROCEDIMIENTOS. "
            f"SE REALIZA INMOVILIZACIÓN DE {zona.upper()} "
            f"UTILIZANDO {tipo_inmovilizacion.upper()} DE {medida_venda}"
        )
        if descripcion:
            texto += f". {descripcion.upper()}"
        texto += ". PACIENTE TOLERA PROCEDIMIENTO."
        return BloqueClinico("inmovilizacion", texto)

    @staticmethod
    def bloque_electrocardiograma(tiene_protesis: bool,
                                   tipo_protesis: str = "") -> BloqueClinico:
        """Genera el bloque del procedimiento de electrocardiograma."""
        partes = [
            "SE INDICA AL PACIENTE RETIRAR TODOS LOS ELEMENTOS METÁLICOS "
            "(CINTURÓN, CADENAS, ARETES, RELOJ, ENTRE OTROS) PARA LA REALIZACIÓN "
            "DEL ELECTROCARDIOGRAMA."
        ]
        if tiene_protesis:
            desc_protesis = tipo_protesis.upper() if tipo_protesis else "NO ESPECIFICADA"
            partes.append(
                f"PACIENTE REFIERE TENER CIRUGÍA O PRÓTESIS QUE INVOLUCRA MATERIAL "
                f"METÁLICO: {desc_protesis}. SE TOMA NOTA Y SE INFORMA AL MÉDICO DE TURNO."
            )
        else:
            partes.append(
                "PACIENTE REFIERE NO TENER CIRUGÍAS NI PRÓTESIS QUE INVOLUCREN "
                "MATERIAL METÁLICO."
            )
        partes.append(
            "SE CUMPLE CON LA TOMA DE ELECTROCARDIOGRAMA, EL CUAL ES ENTREGADO "
            "AL MÉDICO DE TURNO PARA SU RESPECTIVA LECTURA E INTERPRETACIÓN."
        )
        return BloqueClinico("electrocardiograma", " ".join(partes))

    @staticmethod
    def bloque_orden_egreso() -> BloqueClinico:
        """Genera el bloque de orden de egreso médico."""
        return BloqueClinico(
            "orden_egreso",
            "MÉDICO ORDENA EGRESO."
        )

    @staticmethod
    def bloque_indicaciones_egreso(recomendaciones: bool,
                                    signos_alarma: bool) -> BloqueClinico:
        """Genera el bloque de indicaciones al paciente al egreso."""
        partes = []
        if recomendaciones:
            partes.append("SE EXPLICA PROCEDIMIENTO REALIZADO AL PACIENTE "
                          "Y SE ENTREGAN RECOMENDACIONES")
        if signos_alarma:
            partes.append("SE INDICA REINGRESAR EN CASO DE PERSISTENCIA "
                          "O AGRAVAMIENTO DE SÍNTOMAS")
        texto = ". ".join(partes) + "." if partes else ""
        return BloqueClinico("indicaciones_egreso", texto)

    @staticmethod
    def bloque_egreso_paciente(hora_egreso: str, modo_salida: str,
                                estado: str = "ESTABLE") -> BloqueClinico:
        """Genera el bloque de egreso del paciente."""
        return BloqueClinico(
            "egreso_paciente",
            f"SIENDO LAS {hora_egreso} EGRESA PACIENTE "
            f"{modo_salida} CON SIGNOS VITALES {estado}."
        )

    @staticmethod
    def bloque_observacion(consciente: bool, orientado: bool,
                            monitoreo: bool, sintomas: str = "") -> BloqueClinico:
        """Genera el bloque de nota de observación."""
        partes = []
        if consciente:
            partes.append("PACIENTE CONSCIENTE")
        if orientado:
            partes.append("ORIENTADO EN TIEMPO, LUGAR Y ESPACIO")
        if monitoreo:
            partes.append("SE MANTIENE EN MONITOREO CONTINUO")
        if sintomas:
            partes.append(f"REFIERE {sintomas.upper()}")
        texto = ". ".join(partes) + "." if partes else ""
        return BloqueClinico("observacion", texto)

    @staticmethod
    def bloque_traslado(destino: str, tipo_ambulancia: str,
                         estable: bool, acompanado: bool,
                         observaciones: str = "") -> BloqueClinico:
        """Genera el bloque de traslado del paciente a otra institución."""
        texto = (
            f"SE REALIZA TRASLADO DE PACIENTE EN AMBULANCIA {tipo_ambulancia.upper()} "
            f"HACIA {destino.upper()}."
        )
        if estable:
            texto += " PACIENTE SE ENCUENTRA HEMODINÁMICAMENTE ESTABLE."
        if acompanado:
            texto += " ACOMPAÑADO POR PERSONAL DE SALUD."
        if observaciones:
            texto += f" {observaciones.upper()}."
        return BloqueClinico("traslado", texto)

    @staticmethod
    def bloque_soat(tipo_accidente: str) -> BloqueClinico:
        """Genera el bloque inicial para paciente accidentado cubierto por SOAT."""
        return BloqueClinico(
            "soat",
            f"PACIENTE INGRESA POR ACCIDENTE DE TIPO {tipo_accidente.upper()}, "
            f"CUBIERTO POR SOAT. SE REALIZA VALORACIÓN INICIAL."
        )

    @staticmethod
    def bloque_consulta_externa(procedimientos: list) -> BloqueClinico:
        """Genera el bloque de justificación de ingreso por orden de consulta externa."""
        if len(procedimientos) == 1:
            lista = procedimientos[0].upper()
        elif len(procedimientos) == 2:
            lista = f"{procedimientos[0].upper()} Y {procedimientos[1].upper()}"
        else:
            lista = ", ".join(p.upper() for p in procedimientos[:-1])
            lista += f" Y {procedimientos[-1].upper()}"
        return BloqueClinico(
            "consulta_externa",
            f"INGRESA PACIENTE CON ORDEN DE CONSULTA EXTERNA PARA REALIZAR "
            f"EL SIGUIENTE PROCEDIMIENTO: {lista}."
        )

    @staticmethod
    def bloque_lavado_ocular(ojo: str, motivo: str = "") -> BloqueClinico:
        """Genera el bloque del procedimiento de lavado ocular."""
        texto = (
            f"SE TRASLADA PACIENTE A SALA DE PROCEDIMIENTOS. SE REALIZA LAVADO "
            f"OCULAR EN {ojo.upper()} CON SOLUCIÓN SALINA NORMAL 0.9%"
        )
        if motivo:
            texto += f" POR {motivo.upper()}"
        texto += ". PACIENTE TOLERA PROCEDIMIENTO SIN COMPLICACIONES."
        return BloqueClinico("lavado_ocular", texto)

    @staticmethod
    def bloque_monitoria_fetal(semanas: str, resultado: str,
                                plan_medico: str) -> BloqueClinico:
        """Genera el bloque del procedimiento de monitoría fetal."""
        texto = (
            f"SE REALIZA MONITORÍA FETAL A PACIENTE DE {semanas} SEMANAS "
            f"DE GESTACIÓN. SE OBTIENE MONITORÍA {resultado.upper()}, "
            f"LA CUAL ES ENTREGADA AL MÉDICO DE TURNO PARA SU RESPECTIVA "
            f"LECTURA E INTERPRETACIÓN."
        )
        if plan_medico == "EGRESO":
            texto += (
                " MÉDICO REVISA RESULTADOS Y ORDENA EGRESO DE LA PACIENTE "
                "CON INDICACIONES Y SIGNOS DE ALARMA."
            )
        elif plan_medico == "INGRESO A URGENCIAS":
            texto += (
                " MÉDICO REVISA RESULTADOS Y DEBIDO A HALLAZGOS EN LA MONITORÍA "
                "ORDENA INGRESO A CONSULTA DE URGENCIAS PARA VALORACIÓN."
            )
        return BloqueClinico("monitoria_fetal", texto)

    @staticmethod
    def bloque_laboratorios(labs_solicitados: list,
                             resultados: str = "") -> BloqueClinico:
        """Genera el bloque de toma de muestras para laboratorios."""
        if len(labs_solicitados) == 1:
            lista = labs_solicitados[0].upper()
        elif len(labs_solicitados) == 2:
            lista = f"{labs_solicitados[0].upper()} Y {labs_solicitados[1].upper()}"
        else:
            lista = ", ".join(l.upper() for l in labs_solicitados[:-1])
            lista += f" Y {labs_solicitados[-1].upper()}"
        texto = (
            f"SE TOMAN MUESTRAS PARA LOS SIGUIENTES EXÁMENES DE LABORATORIO: "
            f"{lista}. LAS MUESTRAS SON DEBIDAMENTE ROTULADAS Y ENVIADAS AL "
            f"LABORATORIO PARA SU PROCESAMIENTO."
        )
        if resultados:
            texto += f" {resultados.upper()}."
        return BloqueClinico("laboratorios", texto)

    @staticmethod
    def bloque_ecg_consulta_externa(plan_medico: str) -> BloqueClinico:
        """Genera el bloque del plan médico según resultado del EKG en consulta externa."""
        if plan_medico == "EGRESO":
            texto = (
                "MÉDICO REVISA RESULTADOS DEL ELECTROCARDIOGRAMA Y ORDENA "
                "EGRESO DEL PACIENTE CON INDICACIONES Y SIGNOS DE ALARMA."
            )
        elif plan_medico == "INGRESO A URGENCIAS":
            texto = (
                "MÉDICO REVISA RESULTADOS DEL ELECTROCARDIOGRAMA Y DEBIDO A "
                "HALLAZGOS ENCONTRADOS ORDENA INGRESO A CONSULTA DE URGENCIAS "
                "PARA VALORACIÓN Y MANEJO."
            )
        else:
            texto = "MÉDICO REVISA Y EVALÚA RESULTADOS DEL ELECTROCARDIOGRAMA."
        return BloqueClinico("ecg_consulta_externa", texto)

    @staticmethod
    def bloque_plan_medico(ordenes: list) -> BloqueClinico:
        """
        Genera el bloque del plan ordenado por el médico.
        ordenes: lista de strings con cada orden en forma imperativa
        Ej: ['CANALIZAR CON CATÉTER N°20 CON TAPÓN',
             'APLICAR 1 AMPOLLA DE DICLOFENACO IV',
             'TOMAR ELECTROCARDIOGRAMA']
        """
        if not ordenes:
            return BloqueClinico("plan_medico", "")
        lineas = "\n".join(f"* {o.upper()}" for o in ordenes)
        return BloqueClinico(
            "plan_medico",
            f"MÉDICO ORDENA NUEVO PLAN:\n{lineas}"
        )

    @staticmethod
    def bloque_cumplimiento_enfermeria(acciones: list) -> BloqueClinico:
        """
        Genera el bloque de ejecución por parte de enfermería.
        acciones: lista de strings con cada acción ejecutada
        Ej: ['CANALIZACIÓN CON CATÉTER N°20',
             'TOMA DE ELECTROCARDIOGRAMA',
             'ADMINISTRACIÓN DE MEDICAMENTOS']
        """
        if not acciones:
            return BloqueClinico("cumplimiento_enfermeria", "")
        if len(acciones) == 1:
            lista = acciones[0].upper()
        elif len(acciones) == 2:
            lista = f"{acciones[0].upper()} Y {acciones[1].upper()}"
        else:
            lista = ", ".join(a.upper() for a in acciones[:-1])
            lista += f" Y {acciones[-1].upper()}"
        return BloqueClinico(
            "cumplimiento_enfermeria",
            f"SE CUMPLE CON ORDEN MÉDICA: SE REALIZA {lista}."
        )

    # ─── REVALORACIÓN ────────────────────────────────────────────────────────

    @staticmethod
    def bloque_revaloracion_encabezado(sexo: str, condicion: str,
                                        edad: int, motivo: str = "") -> BloqueClinico:
        """Encabezado de la nota de revaloración con datos del paciente."""
        texto = (
            f"PACIENTE {sexo} {condicion} DE {edad} AÑOS DE EDAD"
        )
        if motivo:
            texto += f', QUIEN REFIERE "{motivo.upper()}"'
        texto += ", ES REVALORADO(A) EN SALA DE OBSERVACIÓN."
        return BloqueClinico("revaloracion_encabezado", texto)

    @staticmethod
    def bloque_revaloracion_complicacion(descripcion: str,
                                          carro_rojo: bool,
                                          maniobras: list = None,
                                          medicamentos_carro: list = None) -> BloqueClinico:
        """Bloque de complicación durante la revaloración."""
        texto = (
            f"PACIENTE PRESENTA COMPLICACIÓN: {descripcion.upper()}. "
            f"SE NOTIFICA AL MÉDICO DE TURNO INMEDIATAMENTE."
        )
        if carro_rojo:
            texto += (
                " SE ACTIVA EQUIPO DE RESUCITACIÓN Y SE DISPONE CARRO DE PARO "
                "PARA ATENCIÓN DE URGENCIA VITAL."
            )
            if maniobras:
                m = ", ".join(m.upper() for m in maniobras)
                texto += f" SE REALIZAN LAS SIGUIENTES MANIOBRAS: {m}."
            if medicamentos_carro:
                med_str = ", ".join(m.upper() for m in medicamentos_carro)
                texto += f" SE ADMINISTRAN MEDICAMENTOS DEL CARRO DE PARO: {med_str}."
        return BloqueClinico("revaloracion_complicacion", texto)

    @staticmethod
    def bloque_revaloracion_plan_medico(medico: str, plan: str,
                                         destino: str = "") -> BloqueClinico:
        """Bloque del plan ordenado por el médico en la revaloración."""
        textos_plan = {
            "MEDICAMENTO": (
                f"MÉDICO DE TURNO DR(A). {medico.upper()} REVISA EVOLUCIÓN "
                f"DEL PACIENTE Y ORDENA NUEVO PLAN FARMACOLÓGICO."
            ),
            "EGRESO": (
                f"MÉDICO DE TURNO DR(A). {medico.upper()} REVISA EVOLUCIÓN "
                f"DEL PACIENTE Y ORDENA EGRESO."
            ),
            "HOSPITALIZACION": (
                f"MÉDICO DE TURNO DR(A). {medico.upper()} REVISA EVOLUCIÓN "
                f"DEL PACIENTE Y ORDENA HOSPITALIZACIÓN"
                + (f" EN {destino.upper()}" if destino else "") + "."
            ),
            "REMISION": (
                f"MÉDICO DE TURNO DR(A). {medico.upper()} REVISA EVOLUCIÓN "
                f"DEL PACIENTE Y ORDENA REMISIÓN"
                + (f" A {destino.upper()}" if destino else "") + "."
            ),
        }
        texto = textos_plan.get(plan, f"MÉDICO DE TURNO DR(A). {medico.upper()} ORDENA NUEVO PLAN.")
        return BloqueClinico("revaloracion_plan_medico", texto)

    @staticmethod
    def bloque_revaloracion_labs(labs: list, cierre: str,
                                  destino: str = "") -> BloqueClinico:
        """Bloque de revisión de resultados de laboratorio en la revaloración."""
        if len(labs) == 1:
            lista = labs[0].upper()
        elif len(labs) == 2:
            lista = f"{labs[0].upper()} Y {labs[1].upper()}"
        else:
            lista = ", ".join(l.upper() for l in labs[:-1]) + f" Y {labs[-1].upper()}"

        texto = (
            f"SE RECIBEN RESULTADOS DE LABORATORIO ({lista}), "
            f"LOS CUALES SON REVISADOS POR EL MÉDICO DE TURNO."
        )
        if cierre == "EGRESO":
            texto += " MÉDICO REVISA RESULTADOS Y ORDENA EGRESO DEL PACIENTE."
        elif cierre == "HOSPITALIZACION":
            texto += (
                f" MÉDICO REVISA RESULTADOS Y ORDENA HOSPITALIZACIÓN"
                + (f" EN {destino.upper()}" if destino else "") + "."
            )
        elif cierre == "REMISION":
            texto += (
                f" MÉDICO REVISA RESULTADOS Y ORDENA REMISIÓN"
                + (f" A {destino.upper()}" if destino else "") + "."
            )
        return BloqueClinico("revaloracion_labs", texto)

    @staticmethod
    def bloque_revaloracion_cierre(cierre: str, destino: str = "") -> BloqueClinico:
        """Bloque de cierre de la revaloración."""
        opciones = {
            "OBSERVACION": (
                "PACIENTE CONTINÚA EN SALA DE OBSERVACIÓN BAJO VIGILANCIA "
                "Y MONITOREO CONTINUO POR PARTE DE ENFERMERÍA."
            ),
            "HABITACION": (
                "PACIENTE ES TRASLADADO(A) A HABITACIÓN"
                + (f" {destino.upper()}" if destino else "")
                + " PARA CONTINUAR CON MANEJO INTRAHOSPITALARIO."
            ),
            "EGRESO": (
                "SE PROCEDE A GESTIONAR EL EGRESO DEL PACIENTE CON "
                "RECOMENDACIONES Y SIGNOS DE ALARMA."
            ),
            "HOSPITALIZACION": (
                "SE GESTIONA PROCESO DE HOSPITALIZACIÓN DEL PACIENTE"
                + (f" EN {destino.upper()}" if destino else "") + "."
            ),
            "REMISION": (
                "SE GESTIONA PROCESO DE REMISIÓN DEL PACIENTE"
                + (f" A {destino.upper()}" if destino else "") + "."
            ),
        }
        texto = opciones.get(cierre, "")
        return BloqueClinico("revaloracion_cierre", texto)

    # ─── ENTREGA DE TURNO ─────────────────────────────────────────────────────

    @staticmethod
    def bloque_entrega_turno(sexo: str, condicion: str, edad: int,
                              motivo: str, refiere_malestar: bool,
                              tipo_orden: str = "MEDICAMENTO",
                              medicamento: str = "", presentacion: str = "",
                              cantidad: str = "", via: str = "",
                              labs: list = None, procedimiento: str = "",
                              auxiliar_entrega: str = "",
                              auxiliar_recibe: str = "") -> BloqueClinico:
        """Genera el bloque completo de entrega de turno."""
        texto = (
            f"ENTREGO PACIENTE DE SEXO {sexo}, {condicion} DE {edad} AÑOS DE EDAD, "
            f'QUIEN REFIERE "{motivo.upper()}".'
        )
        if refiere_malestar:
            texto += " PACIENTE REFIERE MALESTAR."
            if tipo_orden == "MEDICAMENTO" and medicamento:
                texto += (
                    f" MÉDICO ORDENA APLICAR {cantidad} {presentacion} DE "
                    f"{medicamento.upper()} POR VÍA {via.upper()}. "
                    f"SE CUMPLE CON ORDEN MÉDICA Y SE APLICA {cantidad} {presentacion} "
                    f"DE {medicamento.upper()} POR VÍA {via.upper()}. "
                    f"PACIENTE TOLERA PROCEDIMIENTO."
                )
            elif tipo_orden == "EKG":
                texto += (
                    " MÉDICO ORDENA TOMA DE ELECTROCARDIOGRAMA. SE CUMPLE CON ORDEN "
                    "MÉDICA Y SE REALIZA TOMA DE ELECTROCARDIOGRAMA, EL CUAL ES "
                    "ENTREGADO AL MÉDICO PARA SU LECTURA E INTERPRETACIÓN."
                )
            elif tipo_orden == "LABORATORIO" and labs:
                lista = ", ".join(l.upper() for l in labs)
                texto += (
                    f" MÉDICO ORDENA TOMA DE LABORATORIOS: {lista}. "
                    f"SE CUMPLE CON ORDEN MÉDICA. SE TOMAN MUESTRAS Y SE ENVÍAN "
                    f"AL LABORATORIO PARA SU PROCESAMIENTO."
                )
            elif tipo_orden == "PROCEDIMIENTO" and procedimiento:
                texto += (
                    f" MÉDICO ORDENA {procedimiento.upper()}. "
                    f"SE CUMPLE CON ORDEN MÉDICA. PACIENTE TOLERA PROCEDIMIENTO."
                )
        if auxiliar_entrega:
            texto += f" ENTREGA PACIENTE {auxiliar_entrega.upper()}, AUXILIAR DE ENFERMERÍA FINALIZANDO TURNO."
        if auxiliar_recibe:
            texto += f" RECIBE {auxiliar_recibe.upper()}, AUXILIAR DE ENFERMERÍA DE TURNO."
        return BloqueClinico("entrega_turno", texto)

    # ─── RECIBO DE TURNO ──────────────────────────────────────────────────────

    @staticmethod
    def bloque_recibo_turno(sexo: str, condicion: str, edad: int,
                             motivo: str, refiere_malestar: bool,
                             tipo_orden: str = "MEDICAMENTO",
                             medicamento: str = "", presentacion: str = "",
                             cantidad: str = "", via: str = "",
                             labs: list = None, procedimiento: str = "",
                             auxiliar_entrega: str = "",
                             auxiliar_recibe: str = "") -> BloqueClinico:
        """Genera el bloque completo de recibo de turno."""
        texto = (
            f"RECIBO PACIENTE DE SEXO {sexo}, {condicion} DE {edad} AÑOS DE EDAD, "
            f'QUIEN REFIERE "{motivo.upper()}".'
        )
        if refiere_malestar:
            texto += " PACIENTE REFIERE MALESTAR."
            if tipo_orden == "MEDICAMENTO" and medicamento:
                texto += (
                    f" MÉDICO ORDENA APLICAR {cantidad} {presentacion} DE "
                    f"{medicamento.upper()} POR VÍA {via.upper()}. "
                    f"SE CUMPLE CON ORDEN MÉDICA Y SE APLICA {cantidad} {presentacion} "
                    f"DE {medicamento.upper()} POR VÍA {via.upper()}. "
                    f"PACIENTE TOLERA PROCEDIMIENTO."
                )
            elif tipo_orden == "EKG":
                texto += (
                    " MÉDICO ORDENA TOMA DE ELECTROCARDIOGRAMA. SE CUMPLE CON ORDEN "
                    "MÉDICA Y SE REALIZA TOMA DE ELECTROCARDIOGRAMA, EL CUAL ES "
                    "ENTREGADO AL MÉDICO PARA SU LECTURA E INTERPRETACIÓN."
                )
            elif tipo_orden == "LABORATORIO" and labs:
                lista = ", ".join(l.upper() for l in labs)
                texto += (
                    f" MÉDICO ORDENA TOMA DE LABORATORIOS: {lista}. "
                    f"SE CUMPLE CON ORDEN MÉDICA. SE TOMAN MUESTRAS Y SE ENVÍAN "
                    f"AL LABORATORIO PARA SU PROCESAMIENTO."
                )
            elif tipo_orden == "PROCEDIMIENTO" and procedimiento:
                texto += (
                    f" MÉDICO ORDENA {procedimiento.upper()}. "
                    f"SE CUMPLE CON ORDEN MÉDICA. PACIENTE TOLERA PROCEDIMIENTO."
                )
        if auxiliar_entrega:
            texto += f" ENTREGA TURNO {auxiliar_entrega.upper()}, AUXILIAR DE ENFERMERÍA."
        if auxiliar_recibe:
            texto += f" YO, {auxiliar_recibe.upper()}, RECIBO PACIENTE QUEDANDO COMO AUXILIAR DE ENFERMERÍA DE TURNO."
        return BloqueClinico("recibo_turno", texto)

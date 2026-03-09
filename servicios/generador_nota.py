"""
Módulo: generador_nota.py
Descripción: Motor principal de generación de notas clínicas.
             Decide qué bloques usar según el tipo de nota y procedimientos,
             y ensambla el texto final de la nota.
"""

from modelos.nota import NotaClinica
from modelos.procedimiento import Procedimiento
from modelos.bloque_clinico import MotorBloques
from utilidades.utilidades_fecha import (
    formatear_fecha_hora,
    formatear_hora,
)


class GeneradorNota:
    """
    Motor central que ensambla la nota clínica a partir de bloques reutilizables.
    Recibe una NotaClinica completa y retorna el texto final estructurado.
    """

    def __init__(self, nota: NotaClinica):
        self.nota = nota
        self.bloques: list = []

    def generar(self) -> str:
        """
        Método principal. Genera el texto completo de la nota clínica
        según su tipo y los datos registrados.
        """
        self.bloques = []

        tipo = self.nota.tipo

        if tipo == NotaClinica.TIPO_INGRESO:
            self._construir_nota_ingreso()
        elif tipo == NotaClinica.TIPO_REVALORACION:
            self._construir_nota_revaloracion()
        elif tipo == NotaClinica.TIPO_EGRESO:
            self._construir_nota_egreso()
        elif tipo == NotaClinica.TIPO_TRASLADO_AMBULANCIA:
            self._construir_nota_traslado()
        elif tipo == NotaClinica.TIPO_RECOGIDA_AMBULANCIA:
            self._construir_nota_recogida_ambulancia()
        elif tipo == NotaClinica.TIPO_HOSPITALIZACION:
            self._construir_nota_hospitalizacion()
        elif tipo == NotaClinica.TIPO_ENTREGA_TURNO:
            self._construir_nota_entrega_turno()
        elif tipo == NotaClinica.TIPO_RECIBO_TURNO:
            self._construir_nota_recibo_turno()

        texto = "\n".join(str(bloque) for bloque in self.bloques if str(bloque))
        self.nota.texto_final = texto
        return texto

    # ------------------------------------------------------------------
    # Constructores por tipo de nota
    # ------------------------------------------------------------------

    def _construir_nota_ingreso(self):
        """Construye la nota de ingreso completa."""
        paciente = self.nota.paciente
        fecha_hora = formatear_fecha_hora(self.nota.fecha_hora_inicio)

        self.bloques.append(MotorBloques.bloque_encabezado(fecha_hora))

        self.bloques.append(MotorBloques.bloque_ingreso_paciente(
            sexo=paciente.sexo,
            condicion=paciente.condicion_etaria,
            edad=paciente.edad,
            modo=paciente.modo_ingreso,
            acompanante=getattr(paciente, "acompanante", ""),
            es_gestante=getattr(paciente, "es_gestante", False),
            semanas_gestacion=getattr(paciente, "semanas_gestacion", ""),
        ))

        if paciente.motivo_consulta:
            self.bloques.append(
                MotorBloques.bloque_motivo_consulta(paciente.motivo_consulta)
            )

        if paciente.tiene_signos_vitales():
            self.bloques.append(MotorBloques.bloque_signos_vitales(
                ta=paciente.tension_arterial,
                fc=paciente.frecuencia_cardiaca,
                fr=paciente.frecuencia_respiratoria,
                temp=paciente.temperatura,
                spo2=paciente.saturacion_oxigeno,
                talla=paciente.talla,
                peso=paciente.peso,
            ))

        if self.nota.es_soat and self.nota.tipo_accidente_soat:
            self.bloques.append(
                MotorBloques.bloque_soat(self.nota.tipo_accidente_soat)
            )

        if self.nota.medico_turno:
            self.bloques.append(
                MotorBloques.bloque_valoracion_medica(
                    self.nota.medico_turno,
                    tiene_plan=bool(self.nota.ordenes_plan_medico)
                )
            )

        self._agregar_bloques_procedimientos()
        self._agregar_bloques_egreso()

    def _construir_nota_revaloracion(self):
        """Construye la nota de revaloración con todos sus bloques."""
        paciente = self.nota.paciente
        fecha_hora = formatear_fecha_hora(self.nota.fecha_hora_inicio)

        self.bloques.append(MotorBloques.bloque_encabezado(fecha_hora))

        # Encabezado con datos del paciente y estado en observación
        self.bloques.append(MotorBloques.bloque_revaloracion_encabezado(
            sexo=paciente.sexo,
            condicion=paciente.condicion_etaria,
            edad=paciente.edad,
            motivo=paciente.motivo_consulta,
        ))

        # Signos vitales: solo si el usuario eligió agregar nuevos
        if self.nota.revaloracion_agregar_signos and paciente.tiene_signos_vitales():
            self.bloques.append(MotorBloques.bloque_signos_vitales(
                ta=paciente.tension_arterial,
                fc=paciente.frecuencia_cardiaca,
                fr=paciente.frecuencia_respiratoria,
                temp=paciente.temperatura,
                spo2=paciente.saturacion_oxigeno,
            ))

        # Complicación (va antes del plan médico)
        if self.nota.revaloracion_complicacion:
            self.bloques.append(MotorBloques.bloque_revaloracion_complicacion(
                descripcion=self.nota.revaloracion_desc_complicacion,
                carro_rojo=self.nota.revaloracion_carro_rojo,
                maniobras=self.nota.revaloracion_maniobras_carro,
                medicamentos_carro=self.nota.revaloracion_medicamentos_carro,
            ))

        # Plan del médico (medicamento, egreso, hospitalización, remisión)
        if self.nota.medico_turno and self.nota.revaloracion_plan:
            self.bloques.append(MotorBloques.bloque_revaloracion_plan_medico(
                medico=self.nota.medico_turno,
                plan=self.nota.revaloracion_plan,
                destino=self.nota.revaloracion_destino_hospitalizacion
                        or self.nota.revaloracion_destino_remision,
            ))

        # Procedimientos y medicamentos ordenados en la revaloración
        self._agregar_bloques_procedimientos()

        # Laboratorios revisados
        if self.nota.revaloracion_labs_revisados and self.nota.revaloracion_labs_descritos:
            self.bloques.append(MotorBloques.bloque_revaloracion_labs(
                labs=self.nota.revaloracion_labs_descritos,
                cierre=self.nota.revaloracion_cierre,
                destino=self.nota.revaloracion_destino_hospitalizacion
                        or self.nota.revaloracion_destino_remision,
            ))

        # Cierre
        if self.nota.revaloracion_cierre:
            self.bloques.append(MotorBloques.bloque_revaloracion_cierre(
                cierre=self.nota.revaloracion_cierre,
                destino=self.nota.revaloracion_destino_hospitalizacion
                        or self.nota.revaloracion_destino_remision,
            ))

        # Egreso formal si aplica
        if self.nota.medico_ordena_egreso:
            self.bloques.append(MotorBloques.bloque_indicaciones_egreso(
                recomendaciones=self.nota.entrega_recomendaciones,
                signos_alarma=self.nota.explica_signos_alarma,
            ))
            if self.nota.fecha_hora_egreso and self.nota.modo_salida:
                hora_egreso = formatear_hora(self.nota.fecha_hora_egreso)
                self.bloques.append(MotorBloques.bloque_egreso_paciente(
                    hora_egreso=hora_egreso,
                    modo_salida=self.nota.modo_salida,
                    estado=self.nota.estado_egreso or "ESTABLES",
                ))

    def _construir_nota_egreso(self):
        """Construye la nota de egreso."""
        fecha_hora = formatear_fecha_hora(self.nota.fecha_hora_inicio)
        self.bloques.append(MotorBloques.bloque_encabezado(fecha_hora))

        if self.nota.medico_ordena_egreso:
            self.bloques.append(MotorBloques.bloque_orden_egreso())

        self.bloques.append(MotorBloques.bloque_indicaciones_egreso(
            recomendaciones=self.nota.entrega_recomendaciones,
            signos_alarma=self.nota.explica_signos_alarma,
        ))

        if self.nota.fecha_hora_egreso and self.nota.modo_salida:
            hora_egreso = formatear_hora(self.nota.fecha_hora_egreso)
            self.bloques.append(MotorBloques.bloque_egreso_paciente(
                hora_egreso=hora_egreso,
                modo_salida=self.nota.modo_salida,
                estado=self.nota.estado_egreso or "ESTABLES",
            ))

    def _construir_nota_traslado(self):
        """Construye la nota de traslado en ambulancia."""
        fecha_hora = formatear_fecha_hora(self.nota.fecha_hora_inicio)
        self.bloques.append(MotorBloques.bloque_encabezado(fecha_hora))

        paciente = self.nota.paciente
        self.bloques.append(MotorBloques.bloque_ingreso_paciente(
            sexo=paciente.sexo,
            condicion=paciente.condicion_etaria,
            edad=paciente.edad,
            modo=paciente.modo_ingreso,
            acompanante=paciente.acompanante if hasattr(paciente, "acompanante") else "",
            es_gestante=getattr(paciente, "es_gestante", False),
            semanas_gestacion=getattr(paciente, "semanas_gestacion", ""),
        ))

        if paciente.tiene_signos_vitales():
            self.bloques.append(MotorBloques.bloque_signos_vitales(
                ta=paciente.tension_arterial,
                fc=paciente.frecuencia_cardiaca,
                fr=paciente.frecuencia_respiratoria,
                temp=paciente.temperatura,
                spo2=paciente.saturacion_oxigeno,
            ))

        self.bloques.append(MotorBloques.bloque_traslado(
            destino=self.nota.destino_traslado,
            tipo_ambulancia=self.nota.tipo_ambulancia,
            estable=self.nota.paciente_estable_traslado,
            acompanado=self.nota.acompanado_personal_salud,
            observaciones=self.nota.observaciones_traslado,
        ))

    def _construir_nota_recogida_ambulancia(self):
        """Construye la nota de recogida en ambulancia."""
        fecha_hora = formatear_fecha_hora(self.nota.fecha_hora_inicio)
        self.bloques.append(MotorBloques.bloque_encabezado(fecha_hora))

        paciente = self.nota.paciente
        self.bloques.append(MotorBloques.bloque_ingreso_paciente(
            sexo=paciente.sexo,
            condicion=paciente.condicion_etaria,
            edad=paciente.edad,
            modo="EN AMBULANCIA",
            es_gestante=getattr(paciente, "es_gestante", False),
            semanas_gestacion=getattr(paciente, "semanas_gestacion", ""),
        ))

        if paciente.motivo_consulta:
            self.bloques.append(
                MotorBloques.bloque_motivo_consulta(paciente.motivo_consulta)
            )

        if paciente.tiene_signos_vitales():
            self.bloques.append(MotorBloques.bloque_signos_vitales(
                ta=paciente.tension_arterial,
                fc=paciente.frecuencia_cardiaca,
                fr=paciente.frecuencia_respiratoria,
                temp=paciente.temperatura,
                spo2=paciente.saturacion_oxigeno,
            ))

        if self.nota.medico_turno:
            self.bloques.append(
                MotorBloques.bloque_valoracion_medica(
                    self.nota.medico_turno,
                    tiene_plan=bool(self.nota.ordenes_plan_medico)
                )
            )

        self._agregar_bloques_procedimientos()

    def _construir_nota_hospitalizacion(self):
        """Construye la nota de ingreso a hospitalización."""
        fecha_hora = formatear_fecha_hora(self.nota.fecha_hora_inicio)
        self.bloques.append(MotorBloques.bloque_encabezado(fecha_hora))

        paciente = self.nota.paciente
        self.bloques.append(MotorBloques.bloque_ingreso_paciente(
            sexo=paciente.sexo,
            condicion=paciente.condicion_etaria,
            edad=paciente.edad,
            modo=paciente.modo_ingreso,
            acompanante=paciente.acompanante if hasattr(paciente, "acompanante") else "",
            es_gestante=getattr(paciente, "es_gestante", False),
            semanas_gestacion=getattr(paciente, "semanas_gestacion", ""),
        ))

        if paciente.tiene_signos_vitales():
            self.bloques.append(MotorBloques.bloque_signos_vitales(
                ta=paciente.tension_arterial,
                fc=paciente.frecuencia_cardiaca,
                fr=paciente.frecuencia_respiratoria,
                temp=paciente.temperatura,
                spo2=paciente.saturacion_oxigeno,
            ))

        if self.nota.medico_turno:
            self.bloques.append(
                MotorBloques.bloque_valoracion_medica(
                    self.nota.medico_turno,
                    tiene_plan=bool(self.nota.ordenes_plan_medico)
                )
            )

        self._agregar_bloques_procedimientos()

    def _construir_nota_entrega_turno(self):
        """Construye la nota de entrega de turno con todos sus bloques."""
        paciente = self.nota.paciente
        fecha_hora = formatear_fecha_hora(self.nota.fecha_hora_inicio)
        self.bloques.append(MotorBloques.bloque_encabezado(fecha_hora))
        self.bloques.append(MotorBloques.bloque_entrega_turno(
            sexo=paciente.sexo,
            condicion=paciente.condicion_etaria,
            edad=paciente.edad,
            motivo=paciente.motivo_consulta,
            refiere_malestar=self.nota.entrega_refiere_malestar,
            tipo_orden=getattr(self.nota, "entrega_tipo_orden", "MEDICAMENTO"),
            medicamento=self.nota.entrega_medicamento_malestar,
            presentacion=self.nota.entrega_presentacion_malestar,
            cantidad=self.nota.entrega_cantidad_malestar,
            via=self.nota.entrega_via_malestar,
            labs=getattr(self.nota, "entrega_labs_malestar", []),
            procedimiento=getattr(self.nota, "entrega_procedimiento_malestar", ""),
            auxiliar_entrega=self.nota.entrega_auxiliar_entrega,
            auxiliar_recibe=self.nota.entrega_auxiliar_recibe,
        ))

    def _construir_nota_recibo_turno(self):
        """Construye la nota de recibo de turno con todos sus bloques."""
        paciente = self.nota.paciente
        fecha_hora = formatear_fecha_hora(self.nota.fecha_hora_inicio)
        self.bloques.append(MotorBloques.bloque_encabezado(fecha_hora))
        self.bloques.append(MotorBloques.bloque_recibo_turno(
            sexo=paciente.sexo,
            condicion=paciente.condicion_etaria,
            edad=paciente.edad,
            motivo=paciente.motivo_consulta,
            refiere_malestar=self.nota.recibo_refiere_malestar,
            tipo_orden=getattr(self.nota, "recibo_tipo_orden", "MEDICAMENTO"),
            medicamento=self.nota.recibo_medicamento_malestar,
            presentacion=self.nota.recibo_presentacion_malestar,
            cantidad=self.nota.recibo_cantidad_malestar,
            via=self.nota.recibo_via_malestar,
            labs=getattr(self.nota, "recibo_labs_malestar", []),
            procedimiento=getattr(self.nota, "recibo_procedimiento_malestar", ""),
            auxiliar_entrega=self.nota.recibo_auxiliar_entrega,
            auxiliar_recibe=self.nota.recibo_auxiliar_recibe,
        ))

    # ------------------------------------------------------------------
    # Métodos auxiliares de ensamblado
    # ------------------------------------------------------------------

    def _agregar_bloques_procedimientos(self):
        """Agrega los bloques de procedimientos en el orden correcto."""
        # 1. Bloque de consulta externa si aplica
        if self.nota.es_consulta_externa and self.nota.procedimientos_consulta_externa:
            self.bloques.append(MotorBloques.bloque_consulta_externa(
                self.nota.procedimientos_consulta_externa
            ))

        # 2. Bloque plan médico (lista de órdenes dadas por el médico)
        if self.nota.ordenes_plan_medico:
            self.bloques.append(MotorBloques.bloque_plan_medico(
                self.nota.ordenes_plan_medico
            ))

        # 3. Bloque cumplimiento de enfermería (resumen de lo ejecutado)
        acciones_ejecutadas = self._calcular_acciones_ejecutadas()
        if acciones_ejecutadas:
            self.bloques.append(MotorBloques.bloque_cumplimiento_enfermeria(
                acciones_ejecutadas
            ))
        elif any(proc.tiene_medicamentos() for proc in self.nota.procedimientos):
            # Fallback: si solo hay medicamentos sin procedimientos definidos
            self.bloques.append(MotorBloques.bloque_ocho_correctos())

        # 4. Bloques de detalle por cada procedimiento ejecutado
        for procedimiento in self.nota.procedimientos:
            self._agregar_bloque_procedimiento(procedimiento)

    def _calcular_acciones_ejecutadas(self) -> list:
        """Genera la lista de acciones ejecutadas para el bloque de cumplimiento."""
        acciones = []
        for proc in self.nota.procedimientos:
            tipo = proc.tipo
            if tipo == Procedimiento.TIPO_CANALIZACION:
                acciones.append(f"CANALIZACIÓN CON {proc.tipo_cateter}")
            elif tipo == Procedimiento.TIPO_INYECTOLOGIA:
                acciones.append("INYECTOLOGÍA")
            elif tipo == Procedimiento.TIPO_CURACION:
                acciones.append("CURACIÓN DE HERIDA")
            elif tipo == Procedimiento.TIPO_SUTURA:
                acciones.append("SUTURA")
            elif tipo == Procedimiento.TIPO_INMOVILIZACION:
                acciones.append("INMOVILIZACIÓN")
            elif tipo == Procedimiento.TIPO_ELECTROCARDIOGRAMA:
                acciones.append("TOMA DE ELECTROCARDIOGRAMA")
            elif tipo == Procedimiento.TIPO_LAVADO_OCULAR:
                acciones.append(f"LAVADO OCULAR EN {proc.lavado_ojo_afectado}")
            elif tipo == Procedimiento.TIPO_MONITORIA_FETAL:
                acciones.append("TOMA DE MONITORÍA FETAL")
            elif tipo == Procedimiento.TIPO_LABORATORIOS:
                acciones.append("TOMA DE MUESTRAS PARA LABORATORIOS")
            if proc.tiene_medicamentos():
                for med in proc.medicamentos:
                    acciones.append(
                        f"ADMINISTRACIÓN DE {med.cantidad} {med.presentacion} "
                        f"DE {med.nombre.upper()} POR VÍA {med.via_administracion}"
                    )
        return acciones

    def _agregar_bloque_procedimiento(self, procedimiento: Procedimiento):
        """Agrega el bloque correspondiente a un procedimiento específico."""
        tipo = procedimiento.tipo

        if tipo == Procedimiento.TIPO_CANALIZACION:
            # Primer catéter
            self.bloques.append(MotorBloques.bloque_canalizacion(
                tipo_cateter=procedimiento.tipo_cateter,
                vena_acceso=procedimiento.vena_acceso,
                con_tapon=procedimiento.con_tapon,
                solucion=procedimiento.solucion,
                es_segunda_via=False,
            ))
            # Segundo catéter (bloque separado)
            if procedimiento.segundo_cateter and procedimiento.tipo_cateter_2:
                self.bloques.append(MotorBloques.bloque_canalizacion(
                    tipo_cateter=procedimiento.tipo_cateter_2,
                    vena_acceso=procedimiento.vena_acceso_2,
                    con_tapon=procedimiento.con_tapon_2,
                    solucion=procedimiento.solucion_2,
                    es_segunda_via=True,
                ))

        elif tipo == Procedimiento.TIPO_INYECTOLOGIA:
            self.bloques.append(MotorBloques.bloque_inyectologia(
                sitio=procedimiento.sitio_aplicacion,
            ))

        elif tipo == Procedimiento.TIPO_CURACION:
            self.bloques.append(MotorBloques.bloque_traslado_curacion())
            self.bloques.append(MotorBloques.bloque_curacion(
                tipo_herida=procedimiento.tipo_herida,
                materiales=procedimiento.materiales_curacion,
                descripcion=procedimiento.descripcion,
            ))

        elif tipo == Procedimiento.TIPO_SUTURA:
            self.bloques.append(MotorBloques.bloque_traslado_sutura())
            self.bloques.append(MotorBloques.bloque_sutura(
                anestesia=procedimiento.tipo_anestesia,
                num_puntos=procedimiento.numero_puntos,
                tipo_sutura=procedimiento.tipo_sutura,
                descripcion=procedimiento.descripcion,
            ))

        elif tipo == Procedimiento.TIPO_ELECTROCARDIOGRAMA:
            # Bloque de preparación (retirar metálicos + prótesis)
            self.bloques.append(MotorBloques.bloque_electrocardiograma(
                tiene_protesis=procedimiento.ecg_tiene_protesis_metalica,
                tipo_protesis=procedimiento.ecg_tipo_protesis,
            ))
            # Si es consulta externa, agregar bloque de entrega y plan médico
            if procedimiento.es_consulta_externa:
                self.bloques.append(MotorBloques.bloque_ecg_consulta_externa(
                    plan_medico=procedimiento.descripcion,
                ))

        elif tipo == Procedimiento.TIPO_LAVADO_OCULAR:
            self.bloques.append(MotorBloques.bloque_lavado_ocular(
                ojo=procedimiento.lavado_ojo_afectado,
                motivo=procedimiento.lavado_motivo,
            ))

        elif tipo == Procedimiento.TIPO_MONITORIA_FETAL:
            self.bloques.append(MotorBloques.bloque_monitoria_fetal(
                semanas=procedimiento.monitoria_semanas_gestacion,
                resultado=procedimiento.monitoria_resultado,
                plan_medico=procedimiento.monitoria_plan_medico,
            ))

        elif tipo == Procedimiento.TIPO_INMOVILIZACION:
            self.bloques.append(MotorBloques.bloque_inmovilizacion(
                zona=procedimiento.zona_inmovilizacion,
                tipo_inmovilizacion=procedimiento.tipo_inmovilizacion,
                medida_venda=procedimiento.medida_venda,
                descripcion=procedimiento.descripcion,
            ))

        elif tipo == Procedimiento.TIPO_LABORATORIOS:
            self.bloques.append(MotorBloques.bloque_laboratorios(
                labs_solicitados=procedimiento.laboratorios_solicitados,
                resultados=procedimiento.laboratorios_resultados,
            ))

        # Medicamentos del procedimiento
        for medicamento in procedimiento.medicamentos:
            self.bloques.append(MotorBloques.bloque_medicamento(
                cantidad=medicamento.cantidad,
                presentacion=medicamento.presentacion,
                nombre=medicamento.nombre,
                via=medicamento.via_administracion,
            ))

    def _tiene_canalizacion(self) -> bool:
        """Verifica si la nota tiene al menos un procedimiento de canalización."""
        return any(
            p.tipo == Procedimiento.TIPO_CANALIZACION
            for p in self.nota.procedimientos
        )

    def _agregar_bloques_egreso(self):
        """Agrega los bloques de egreso/cierre según la decisión médica."""
        # Observación: solo si hay canalización Y no hay egreso definido
        if getattr(self.nota, "queda_en_observacion", False) and self._tiene_canalizacion():
            self.bloques.append(MotorBloques.bloque_observacion_cierre())

        if self.nota.medico_ordena_egreso:
            self.bloques.append(MotorBloques.bloque_orden_egreso())
            self.bloques.append(MotorBloques.bloque_indicaciones_egreso(
                recomendaciones=self.nota.entrega_recomendaciones,
                signos_alarma=self.nota.explica_signos_alarma,
            ))
            if self.nota.fecha_hora_egreso and self.nota.modo_salida:
                hora_egreso = formatear_hora(self.nota.fecha_hora_egreso)
                self.bloques.append(MotorBloques.bloque_egreso_paciente(
                    hora_egreso=hora_egreso,
                    modo_salida=self.nota.modo_salida,
                    estado=self.nota.estado_egreso or "ESTABLES",
                ))

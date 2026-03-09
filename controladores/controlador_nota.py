"""
Módulo: controlador_nota.py
Descripción: Controlador que gestiona la lógica de creación y
             procesamiento de la nota clínica, conectando los modelos
             con los servicios y las vistas.
"""

from modelos.nota import NotaClinica
from modelos.paciente import Paciente
from modelos.procedimiento import Procedimiento
from modelos.medicamento import Medicamento
from servicios.generador_nota import GeneradorNota
from servicios.exportador_archivo import ExportadorArchivo
from servicios.servicio_estadisticas import ServicioEstadisticas
from utilidades.validadores import validar_nota_basica


class ControladorNota:
    """
    Controlador principal de la nota clínica.
    Coordina la interacción entre la vista y los servicios del sistema.
    """

    def __init__(self):
        self.nota_actual: NotaClinica = None
        self.exportador = ExportadorArchivo()
        self.servicio_estadisticas = ServicioEstadisticas()

    def iniciar_nueva_nota(self, tipo_nota: str) -> NotaClinica:
        """
        Crea e inicializa una nueva nota clínica del tipo indicado.

        Parámetros:
            tipo_nota: Tipo de nota a crear.

        Retorna:
            Instancia de NotaClinica inicializada.
        """
        self.nota_actual = NotaClinica()
        self.nota_actual.tipo = tipo_nota
        return self.nota_actual

    def establecer_datos_paciente(self, sexo: str, edad: int,
                                   modo_ingreso: str, motivo_consulta: str,
                                   estado_general: str = "",
                                   acompanante: str = ""):
        """Establece los datos básicos del paciente en la nota actual."""
        if not self.nota_actual:
            raise ValueError("No hay una nota activa. Llame a iniciar_nueva_nota primero.")

        paciente = self.nota_actual.paciente
        paciente.sexo = sexo
        paciente.establecer_edad(edad)
        paciente.modo_ingreso = modo_ingreso
        paciente.motivo_consulta = motivo_consulta
        paciente.estado_general = estado_general
        paciente.acompanante = acompanante

    def establecer_signos_vitales(self, ta: str = "", fc: str = "",
                                   fr: str = "", temp: str = "",
                                   spo2: str = "", talla: str = "",
                                   peso: str = ""):
        """Establece los signos vitales del paciente en la nota actual."""
        if not self.nota_actual:
            raise ValueError("No hay una nota activa.")

        paciente = self.nota_actual.paciente
        paciente.tension_arterial = ta
        paciente.frecuencia_cardiaca = fc
        paciente.frecuencia_respiratoria = fr
        paciente.temperatura = temp
        paciente.saturacion_oxigeno = spo2
        paciente.talla = talla
        paciente.peso = peso

    def establecer_medico(self, nombre_medico: str):
        """Establece el médico de turno en la nota actual."""
        if not self.nota_actual:
            raise ValueError("No hay una nota activa.")
        self.nota_actual.medico_turno = nombre_medico

    def agregar_procedimiento(self, tipo: str, **kwargs) -> Procedimiento:
        """
        Agrega un procedimiento a la nota actual con sus datos específicos.

        Parámetros:
            tipo: Tipo de procedimiento.
            **kwargs: Parámetros específicos según el tipo de procedimiento.

        Retorna:
            Instancia de Procedimiento creada.
        """
        if not self.nota_actual:
            raise ValueError("No hay una nota activa.")

        procedimiento = Procedimiento(tipo)

        if tipo == Procedimiento.TIPO_CANALIZACION:
            procedimiento.tipo_cateter = kwargs.get("tipo_cateter", "")
            procedimiento.vena_acceso = kwargs.get("vena_acceso", "")
            procedimiento.con_tapon = kwargs.get("con_tapon", False)
            procedimiento.solucion = kwargs.get("solucion", "")
            procedimiento.segundo_cateter = kwargs.get("segundo_cateter", False)
            procedimiento.tipo_cateter_2 = kwargs.get("tipo_cateter_2", "")
            procedimiento.vena_acceso_2 = kwargs.get("vena_acceso_2", "")
            procedimiento.con_tapon_2 = kwargs.get("con_tapon_2", False)
            procedimiento.solucion_2 = kwargs.get("solucion_2", "")
            procedimiento.queda_en_observacion = kwargs.get("queda_en_observacion", False)

        elif tipo == Procedimiento.TIPO_CURACION:
            procedimiento.tipo_herida = kwargs.get("tipo_herida", "")
            procedimiento.materiales_curacion = kwargs.get("materiales", [])
            procedimiento.descripcion = kwargs.get("descripcion", "")

        elif tipo == Procedimiento.TIPO_SUTURA:
            procedimiento.tipo_anestesia = kwargs.get("tipo_anestesia", "")
            procedimiento.numero_puntos = kwargs.get("numero_puntos", 0)
            procedimiento.tipo_sutura = kwargs.get("tipo_sutura", "")
            procedimiento.control_sangrado = kwargs.get("control_sangrado", False)
            procedimiento.descripcion = kwargs.get("descripcion", "")

        elif tipo == Procedimiento.TIPO_INYECTOLOGIA:
            procedimiento.sitio_aplicacion = kwargs.get("sitio_aplicacion", "")

        elif tipo == Procedimiento.TIPO_ELECTROCARDIOGRAMA:
            procedimiento.ecg_tiene_protesis_metalica = kwargs.get("ecg_tiene_protesis", False)
            procedimiento.ecg_tipo_protesis = kwargs.get("ecg_tipo_protesis", "")
            procedimiento.es_consulta_externa = kwargs.get("es_consulta_externa", False)
            procedimiento.descripcion = kwargs.get("plan_medico", "")

        elif tipo == Procedimiento.TIPO_LAVADO_OCULAR:
            procedimiento.lavado_ojo_afectado = kwargs.get("ojo_afectado", "")
            procedimiento.lavado_motivo = kwargs.get("motivo", "")
            procedimiento.es_consulta_externa = kwargs.get("es_consulta_externa", False)

        elif tipo == Procedimiento.TIPO_MONITORIA_FETAL:
            procedimiento.monitoria_semanas_gestacion = kwargs.get("semanas_gestacion", "")
            procedimiento.monitoria_resultado = kwargs.get("resultado", "")
            procedimiento.monitoria_plan_medico = kwargs.get("plan_medico", "")
            procedimiento.es_consulta_externa = kwargs.get("es_consulta_externa", False)

        elif tipo == Procedimiento.TIPO_INMOVILIZACION:
            procedimiento.zona_inmovilizacion = kwargs.get("zona_inmovilizacion", "")
            procedimiento.tipo_inmovilizacion = kwargs.get("tipo_inmovilizacion", "")
            procedimiento.medida_venda = kwargs.get("medida_venda", "")
            procedimiento.descripcion = kwargs.get("descripcion", "")

        elif tipo == Procedimiento.TIPO_LABORATORIOS:
            procedimiento.laboratorios_solicitados = kwargs.get("labs_solicitados", [])
            procedimiento.laboratorios_resultados = kwargs.get("resultados", "")

        self.nota_actual.agregar_procedimiento(procedimiento)
        return procedimiento

    def agregar_medicamento_a_procedimiento(self, procedimiento: Procedimiento,
                                             nombre: str, presentacion: str,
                                             cantidad: str, via: str,
                                             observaciones: str = "") -> Medicamento:
        """
        Agrega un medicamento a un procedimiento existente.

        Retorna:
            Instancia de Medicamento creada.
        """
        medicamento = Medicamento()
        medicamento.nombre = nombre
        medicamento.presentacion = presentacion
        medicamento.cantidad = cantidad
        medicamento.via_administracion = via
        medicamento.observaciones = observaciones
        procedimiento.agregar_medicamento(medicamento)
        return medicamento

    def establecer_datos_egreso(self, medico_ordena: bool,
                                 recomendaciones: bool, signos_alarma: bool,
                                 modo_salida: str, estado_egreso: str = "",
                                 observaciones: str = ""):
        """Establece los datos de egreso del paciente."""
        if not self.nota_actual:
            raise ValueError("No hay una nota activa.")

        self.nota_actual.medico_ordena_egreso = medico_ordena
        self.nota_actual.entrega_recomendaciones = recomendaciones
        self.nota_actual.explica_signos_alarma = signos_alarma
        self.nota_actual.modo_salida = modo_salida
        self.nota_actual.estado_egreso = estado_egreso
        self.nota_actual.observaciones_egreso = observaciones

        if medico_ordena:
            self.nota_actual.registrar_hora_egreso()

    def construir_plan_medico_automatico(self):
        """
        Construye automáticamente la lista de órdenes del plan médico
        basándose en los procedimientos y medicamentos registrados.
        Debe llamarse DESPUÉS de agregar todos los procedimientos.
        """
        if not self.nota_actual:
            return
        from modelos.procedimiento import Procedimiento
        ordenes = []
        for proc in self.nota_actual.procedimientos:
            tipo = proc.tipo
            if tipo == Procedimiento.TIPO_CANALIZACION:
                vena = f" EN {proc.vena_acceso}" if proc.vena_acceso else ""
                orden = f"CANALIZAR CON {proc.tipo_cateter}{vena}"
                if proc.con_tapon:
                    orden += " CON TAPÓN"
                if proc.solucion:
                    orden += f" Y PASAR {proc.solucion}"
                ordenes.append(orden)
                if proc.segundo_cateter and proc.tipo_cateter_2:
                    vena2 = f" EN {proc.vena_acceso_2}" if proc.vena_acceso_2 else ""
                    orden2 = f"CANALIZAR SEGUNDA VÍA CON {proc.tipo_cateter_2}{vena2}"
                    if proc.con_tapon_2:
                        orden2 += " CON TAPÓN"
                    if proc.solucion_2:
                        orden2 += f" Y PASAR {proc.solucion_2}"
                    ordenes.append(orden2)
            elif tipo == Procedimiento.TIPO_INYECTOLOGIA:
                ordenes.append(f"APLICAR INYECTOLOGÍA EN REGIÓN {proc.sitio_aplicacion}")
            elif tipo == Procedimiento.TIPO_CURACION:
                ordenes.append(f"REALIZAR CURACIÓN DE HERIDA {proc.tipo_herida}")
            elif tipo == Procedimiento.TIPO_SUTURA:
                ordenes.append(
                    f"REALIZAR SUTURA CON {proc.tipo_anestesia}, "
                    f"{proc.numero_puntos} PUNTOS TIPO {proc.tipo_sutura}"
                )
            elif tipo == Procedimiento.TIPO_INMOVILIZACION:
                orden = f"INMOVILIZAR {proc.zona_inmovilizacion}"
                if proc.tipo_inmovilizacion:
                    orden += f" CON {proc.tipo_inmovilizacion} DE {proc.medida_venda}"
                ordenes.append(orden)
            elif tipo == Procedimiento.TIPO_ELECTROCARDIOGRAMA:
                ordenes.append("TOMAR ELECTROCARDIOGRAMA")
            elif tipo == Procedimiento.TIPO_LAVADO_OCULAR:
                ordenes.append(f"REALIZAR LAVADO OCULAR EN {proc.lavado_ojo_afectado}")
            elif tipo == Procedimiento.TIPO_MONITORIA_FETAL:
                ordenes.append("REALIZAR MONITORÍA FETAL")
            elif tipo == Procedimiento.TIPO_LABORATORIOS:
                if proc.laboratorios_solicitados:
                    labs = ", ".join(proc.laboratorios_solicitados)
                    ordenes.append(f"TOMAR LABORATORIOS: {labs}")
            # Medicamentos de este procedimiento
            for med in proc.medicamentos:
                ordenes.append(
                    f"APLICAR {med.cantidad} {med.presentacion} DE "
                    f"{med.nombre.upper()} POR VÍA {med.via_administracion}"
                )
        self.nota_actual.ordenes_plan_medico = ordenes

    def establecer_plan_medico_manual(self, ordenes: list):
        """Permite establecer manualmente la lista de órdenes del plan médico."""
        if not self.nota_actual:
            raise ValueError("No hay una nota activa.")
        self.nota_actual.ordenes_plan_medico = ordenes

    def establecer_consulta_externa(self, es_consulta_externa: bool,
                                     procedimientos_nombres: list = None):
        """Activa el flujo de consulta externa en la nota actual."""
        if not self.nota_actual:
            raise ValueError("No hay una nota activa.")
        self.nota_actual.es_consulta_externa = es_consulta_externa
        self.nota_actual.procedimientos_consulta_externa = procedimientos_nombres or []

    def establecer_datos_soat(self, es_soat: bool, tipo_accidente: str = ""):
        """Activa el flujo SOAT en la nota actual."""
        if not self.nota_actual:
            raise ValueError("No hay una nota activa.")
        self.nota_actual.es_soat = es_soat
        self.nota_actual.tipo_accidente_soat = tipo_accidente

    def generar_texto_nota(self) -> str:
        """
        Genera el texto final de la nota clínica actual.

        Retorna:
            Texto completo de la nota en mayúsculas.
        """
        if not self.nota_actual:
            raise ValueError("No hay una nota activa.")

        generador = GeneradorNota(self.nota_actual)
        return generador.generar()

    def exportar_nota(self, ruta_personalizada: str = None) -> str:
        """
        Exporta la nota actual a un archivo .txt.

        Retorna:
            Ruta absoluta del archivo generado.
        """
        if not self.nota_actual or not self.nota_actual.texto_final:
            raise ValueError("Debe generar la nota antes de exportarla.")

        ruta = self.exportador.exportar(
            texto_nota=self.nota_actual.texto_final,
            tipo_nota=self.nota_actual.tipo,
            ruta_personalizada=ruta_personalizada,
        )

        self.servicio_estadisticas.registrar_nota(
            tipo_nota=self.nota_actual.tipo,
            tipos_procedimiento=self.nota_actual.obtener_tipos_procedimiento(),
        )

        return ruta

    def validar_campos_minimos(self) -> list:
        """
        Valida los campos mínimos requeridos para generar la nota.

        Retorna:
            Lista de mensajes de error (vacía si todo es válido).
        """
        if not self.nota_actual:
            return ["No hay una nota activa."]

        paciente = self.nota_actual.paciente
        return validar_nota_basica(
            tipo_nota=self.nota_actual.tipo,
            sexo=paciente.sexo,
            edad=str(paciente.edad),
            medico=self.nota_actual.medico_turno,
        )

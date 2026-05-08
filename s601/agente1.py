"""
Agente clasificador para IAGym.

Entrada: la variable `prompt`.
Salida: log de la funcion seleccionada y los parametros con los que se llamo.
"""

from __future__ import annotations

import json
import os
from typing import Any, Callable

from openai import OpenAI


MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

# Cambia este texto para probar otros casos.
prompt = input("Consulta al gym: ") # "Quiero bajar de peso y necesito una dieta semanal para entrenar en IAGym."


TOOLS = [
    {
        "type": "function",
        "name": "informar_planes_gimnasio",
        "description": (
            "Usa esta funcion cuando el cliente pida informes de IAGym: planes, "
            "precios, horarios, servicios, clases, sucursales o aparatos disponibles."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "tema_principal": {
                    "type": "string",
                    "description": "El tema central solicitado por el cliente.",
                },
                "detalles_solicitados": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": (
                        "Detalles concretos que el usuario quiere saber, por ejemplo "
                        "horarios, aparatos, planes, costos o clases."
                    ),
                },
                "nivel_detalle": {
                    "type": "string",
                    "enum": ["basico", "medio", "detallado"],
                    "description": "Profundidad de la informacion que conviene entregar.",
                },
            },
            "required": ["tema_principal", "detalles_solicitados", "nivel_detalle"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "planificar_rutina",
        "description": (
            "Usa esta funcion cuando el cliente quiera una rutina de ejercicio, "
            "entrenamiento, plan semanal, series, repeticiones, musculos o aparatos."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "objetivo": {
                    "type": "string",
                    "description": (
                        "Meta de entrenamiento: fuerza, hipertrofia, bajar grasa, "
                        "resistencia, acondicionamiento, movilidad u otra."
                    ),
                },
                "nivel": {
                    "type": "string",
                    "enum": ["principiante", "intermedio", "avanzado", "no_especificado"],
                    "description": "Nivel fisico declarado o inferido del cliente.",
                },
                "dias_por_semana": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 7,
                    "description": "Numero de dias por semana para entrenar.",
                },
                "grupos_musculares": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Grupos musculares o zonas que el cliente quiere trabajar.",
                },
                "aparatos_requeridos": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Aparatos, maquinas o equipo que deben contemplarse.",
                },
                "formato_esperado": {
                    "type": "string",
                    "description": (
                        "Formato esperado de la rutina, por ejemplo series, repeticiones, "
                        "descansos, calentamiento o plan diario."
                    ),
                },
            },
            "required": [
                "objetivo",
                "nivel",
                "dias_por_semana",
                "grupos_musculares",
                "aparatos_requeridos",
                "formato_esperado",
            ],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "planificar_dieta",
        "description": (
            "Usa esta funcion cuando el cliente pida dieta, alimentacion, menu, "
            "nutricion, bajar de peso, adelgazar, aumentar masa o ganar musculo."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "objetivo": {
                    "type": "string",
                    "enum": [
                        "adelgazar",
                        "aumentar_masa",
                        "mantener_peso",
                        "mejorar_rendimiento",
                        "no_especificado",
                    ],
                    "description": "Objetivo principal de alimentacion.",
                },
                "duracion_plan": {
                    "type": "string",
                    "description": "Duracion solicitada, por ejemplo un dia, una semana o un mes.",
                },
                "preferencias": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Preferencias, restricciones o alimentos mencionados.",
                },
                "comidas_por_dia": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 8,
                    "description": "Numero de comidas al dia solicitado o inferido.",
                },
                "nivel_detalle": {
                    "type": "string",
                    "enum": ["basico", "medio", "detallado"],
                    "description": "Profundidad esperada del plan alimenticio.",
                },
            },
            "required": [
                "objetivo",
                "duracion_plan",
                "preferencias",
                "comidas_por_dia",
                "nivel_detalle",
            ],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "manejar_no_entendido",
        "description": (
            "Usa esta funcion cuando el mensaje no corresponda claramente a informes, "
            "rutinas o dietas de IAGym, o cuando falten datos criticos para clasificar."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "mensaje_usuario": {
                    "type": "string",
                    "description": "Texto original o resumen fiel de lo que dijo el usuario.",
                },
                "motivo_no_entendido": {
                    "type": "string",
                    "description": "Razon por la que no se entiende o no se puede clasificar.",
                },
                "respuesta_intentada": {
                    "type": "string",
                    "description": (
                        "Respuesta breve que se intentaria dar para pedir aclaracion o "
                        "redirigir al usuario."
                    ),
                },
            },
            "required": [
                "mensaje_usuario",
                "motivo_no_entendido",
                "respuesta_intentada",
            ],
            "additionalProperties": False,
        },
        "strict": True,
    },
]


def _log_tool_call(nombre_funcion: str, parametros: dict[str, Any]) -> str:
    """Construye el unico resultado visible del programa."""
    return json.dumps(
        {
            "funcion_ejecutada": nombre_funcion,
            "parametros": parametros,
        },
        ensure_ascii=False,
        indent=2,
    )


def informar_planes_gimnasio(**parametros: Any) -> str:
    return _log_tool_call("informar_planes_gimnasio", parametros)


def planificar_rutina(**parametros: Any) -> str:
    return _log_tool_call("planificar_rutina", parametros)


def planificar_dieta(**parametros: Any) -> str:
    return _log_tool_call("planificar_dieta", parametros)


def manejar_no_entendido(**parametros: Any) -> str:
    return _log_tool_call("manejar_no_entendido", parametros)


FUNCIONES_DISPONIBLES: dict[str, Callable[..., str]] = {
    "informar_planes_gimnasio": informar_planes_gimnasio,
    "planificar_rutina": planificar_rutina,
    "planificar_dieta": planificar_dieta,
    "manejar_no_entendido": manejar_no_entendido,
}


INSTRUCCIONES = """
Eres el agente de recepcion de IAGym, un gimnasio ficticio.
Tu tarea no es responder al cliente directamente: tu unica tarea es elegir una
sola funcion objetivo segun la intencion del mensaje.

Reglas:
- Selecciona exactamente una tool.
- Si el usuario mezcla temas, elige el objetivo dominante.
- Si el mensaje es ambiguo o esta fuera del contexto de IAGym, usa manejar_no_entendido.
- Llena los parametros con lo que el usuario dijo; si falta un dato, usa valores
  razonables como "no_especificado", listas vacias o una duracion general.
- No inventes ejecuciones reales: la funcion solo debe reportar parametros.
""".strip()


def seleccionar_y_loguear(prompt_usuario: str) -> str:
    client = OpenAI(api_key="API_KEY")

    response = client.responses.create(
        model=MODEL,
        instructions=INSTRUCCIONES,
        input=prompt_usuario,
        tools=TOOLS,
        tool_choice="required",
        parallel_tool_calls=False,
        max_tool_calls=1,
    )

    tool_calls = [
        item for item in response.output if getattr(item, "type", None) == "function_call"
    ]

    if not tool_calls:
        return manejar_no_entendido(
            mensaje_usuario=prompt_usuario,
            motivo_no_entendido="El modelo no eligio ninguna tool.",
            respuesta_intentada="Puedes preguntarme por planes, rutinas o dietas de IAGym.",
        )

    tool_call = tool_calls[0]
    nombre_funcion = tool_call.name
    parametros = json.loads(tool_call.arguments)

    funcion = FUNCIONES_DISPONIBLES.get(nombre_funcion, manejar_no_entendido)
    if funcion is manejar_no_entendido and nombre_funcion not in FUNCIONES_DISPONIBLES:
        return manejar_no_entendido(
            mensaje_usuario=prompt_usuario,
            motivo_no_entendido=f"Tool desconocida seleccionada: {nombre_funcion}",
            respuesta_intentada="Puedes preguntarme por planes, rutinas o dietas de IAGym.",
        )

    return funcion(**parametros)


if __name__ == "__main__":
    print(seleccionar_y_loguear(prompt))

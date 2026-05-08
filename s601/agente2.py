"""
Agente clasificador para reservas de hotel y lugares turisticos.

Entrada: la variable `prompt`.
Salida: log de la funcion seleccionada y los parametros con los que se llamo.
"""

from __future__ import annotations

import json
import os
from typing import Any, Callable

from openai import OpenAI


MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

# Cambia este texto desde consola para probar otros casos.
prompt = input("Consulta de viaje: ")


TOOLS = [
    {
        "type": "function",
        "name": "reservar_hotel",
        "description": (
            "Usa esta funcion cuando el usuario quiera reservar, buscar o cotizar "
            "un hotel, habitacion, hospedaje, estancia o alojamiento."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "destino": {
                    "type": "string",
                    "description": "Ciudad, zona o destino donde se desea el hotel.",
                },
                "fecha_entrada": {
                    "type": "string",
                    "description": "Fecha de llegada en texto libre o 'no_especificada'.",
                },
                "fecha_salida": {
                    "type": "string",
                    "description": "Fecha de salida en texto libre o 'no_especificada'.",
                },
                "huespedes": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 20,
                    "description": "Cantidad total de personas que se hospedaran.",
                },
                "habitaciones": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 10,
                    "description": "Numero de habitaciones requeridas.",
                },
                "presupuesto": {
                    "type": "string",
                    "description": (
                        "Presupuesto mencionado por noche o total; usa 'no_especificado' "
                        "si no aparece."
                    ),
                },
                "categoria_hotel": {
                    "type": "string",
                    "enum": [
                        "economico",
                        "medio",
                        "premium",
                        "lujo",
                        "no_especificado",
                    ],
                    "description": "Nivel o categoria esperada del hotel.",
                },
                "preferencias": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": (
                        "Preferencias como desayuno, alberca, gimnasio, vista, playa, "
                        "centro, estacionamiento, mascotas o accesibilidad."
                    ),
                },
            },
            "required": [
                "destino",
                "fecha_entrada",
                "fecha_salida",
                "huespedes",
                "habitaciones",
                "presupuesto",
                "categoria_hotel",
                "preferencias",
            ],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "ubicar_lugares_turisticos",
        "description": (
            "Usa esta funcion cuando el usuario quiera encontrar, ubicar o recibir "
            "sugerencias de lugares turisticos, atracciones, museos, playas, parques, "
            "zonas historicas, restaurantes o actividades en un destino."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "destino": {
                    "type": "string",
                    "description": "Ciudad, pais, colonia o zona donde se buscan lugares.",
                },
                "tipo_lugar": {
                    "type": "string",
                    "description": (
                        "Tipo de lugar solicitado: museo, playa, parque, monumento, "
                        "restaurante, vida nocturna, familiar, aventura u otro."
                    ),
                },
                "intereses": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Gustos o temas mencionados por el usuario.",
                },
                "zona_referencia": {
                    "type": "string",
                    "description": (
                        "Punto de referencia cercano, hotel, aeropuerto, centro o "
                        "'no_especificada'."
                    ),
                },
                "radio_km": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 100,
                    "description": "Radio aproximado de busqueda en kilometros.",
                },
                "momento_visita": {
                    "type": "string",
                    "description": (
                        "Momento deseado para visitar: manana, tarde, noche, fin de "
                        "semana, fecha concreta o 'no_especificado'."
                    ),
                },
                "nivel_detalle": {
                    "type": "string",
                    "enum": ["basico", "medio", "detallado"],
                    "description": "Profundidad con la que se desea ubicar o sugerir lugares.",
                },
            },
            "required": [
                "destino",
                "tipo_lugar",
                "intereses",
                "zona_referencia",
                "radio_km",
                "momento_visita",
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
            "Usa esta funcion cuando el mensaje no corresponda claramente a reserva "
            "de hotel o ubicacion de lugares turisticos, o cuando falten datos "
            "criticos para clasificar."
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


def reservar_hotel(**parametros: Any) -> str:
    return _log_tool_call("reservar_hotel", parametros)


def ubicar_lugares_turisticos(**parametros: Any) -> str:
    return _log_tool_call("ubicar_lugares_turisticos", parametros)


def manejar_no_entendido(**parametros: Any) -> str:
    return _log_tool_call("manejar_no_entendido", parametros)


FUNCIONES_DISPONIBLES: dict[str, Callable[..., str]] = {
    "reservar_hotel": reservar_hotel,
    "ubicar_lugares_turisticos": ubicar_lugares_turisticos,
    "manejar_no_entendido": manejar_no_entendido,
}


INSTRUCCIONES = """
Eres un agente de viajes para reservas de hotel y ubicacion de lugares turisticos.
Tu tarea no es responder al usuario directamente: tu unica tarea es elegir una
sola funcion objetivo segun la intencion del mensaje.

Reglas:
- Selecciona exactamente una tool.
- Si el usuario mezcla reservar hotel y lugares turisticos, elige el objetivo dominante.
- Si el mensaje es ambiguo o esta fuera del contexto de viajes, usa manejar_no_entendido.
- Llena los parametros con lo que el usuario dijo; si falta un dato, usa valores
  razonables como "no_especificado", "no_especificada", listas vacias o numeros
  conservadores.
- No inventes reservas reales ni ubicaciones verificadas: la funcion solo debe
  reportar parametros.
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
            respuesta_intentada=(
                "Puedes pedirme reservar un hotel o ubicar lugares turisticos."
            ),
        )

    tool_call = tool_calls[0]
    nombre_funcion = tool_call.name
    parametros = json.loads(tool_call.arguments)

    funcion = FUNCIONES_DISPONIBLES.get(nombre_funcion, manejar_no_entendido)
    if funcion is manejar_no_entendido and nombre_funcion not in FUNCIONES_DISPONIBLES:
        return manejar_no_entendido(
            mensaje_usuario=prompt_usuario,
            motivo_no_entendido=f"Tool desconocida seleccionada: {nombre_funcion}",
            respuesta_intentada=(
                "Puedes pedirme reservar un hotel o ubicar lugares turisticos."
            ),
        )

    return funcion(**parametros)


if __name__ == "__main__":
    print(seleccionar_y_loguear(prompt))

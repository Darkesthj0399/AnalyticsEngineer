from typing import Literal
from anthropic import Anthropic
from pydantic import BaseModel, ValidationError

# 1. EL CLIENTE
client = Anthropic()

# 2. EL MOLDE: los campos y valores permitidos
class Clasificacion(BaseModel):
    motivo: Literal["insistencia_comercial", "producto", "atencion", "cobros", "otro", "no_aplica"]
    sentimiento: Literal["positivo", "negativo", "mixto", "no_aplica"]

# 3. LAS REGLAS
reglas = """Eres un clasificador de sentimiento de las respuestas de los clientes a las llamadas que realiza un operario bancario.
Clasifica el motivo de la calificación. Puede ser SOLO UNO de esta lista: insistencia_comercial, producto, atencion, cobros, otro, no_aplica. Usa otro cuando es un comentario de un cliente que no calza en las demás categorías.
El sentimiento puede ser SOLO UNO de esta lista: positivo, negativo, mixto, no_aplica.

Responde SOLO con este JSON, sin texto antes ni después:
{"motivo": "...", "sentimiento": "..."}

Si el comentario no es una evaluación de una llamada, responde:
{"motivo": "no_aplica", "sentimiento": "no_aplica"}"""

# 4. PEDIDO + VALIDACIÓN + REINTENTO
def clasificar(comentario, max_intentos=2):
    for intento in range(max_intentos):
        respuesta = client.messages.create(
            model="claude-haiku-5-5",
            max_tokens=50,
            thinking={"type": "disabled"},
            system=reglas,
            messages=[{"role": "user", "content": comentario}],
        )
        texto = respuesta.content[0].text
        print(f"Intento {intento + 1} | stop_reason: {respuesta.stop_reason} | "
              f"tokens entrada: {respuesta.usage.input_tokens}, salida: {respuesta.usage.output_tokens}")
        try:
            return Clasificacion.model_validate_json(texto)
        except ValidationError as e:
            print(f"Falló la validación: {e}")
    return None

# 5. PRUEBA
comentarios = [
    "¿qué hora es en Tokio?",
    "El operador me llamó tres veces en el día para ofrecerme un préstamo, ya no quiero que me llamen.",
]

for c in comentarios:
    resultado = clasificar(c)
    print(c, "→", resultado, "\n")
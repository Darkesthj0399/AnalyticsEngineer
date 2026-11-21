from anthropic import Anthropic

# 1. EL CLIENTE (el mesero): se conecta y busca ANTHROPIC_API_KEY por su cuenta
client = Anthropic()


reglas = """Eres un clasificador de sentimiento de las respuestas de los clientes a las llamadas que realiza un operario bancario.
Clasifica los motivos por los cuales se da la calificación, pueden ser SOLO un motivo de esta lista: insistencia_comercial, producto, atencion, cobros, otro y no_aplica. Otro lo utilizas cuando es comentario de un cliente pero no calza dentro de las demas categorias.
Y el sentimiento puede ser SOLO UNO  de esta lista:
positivo, negativo, mixto y no_aplica

Responde SOLO con una línea en este formato exacto:
motivo|sentimiento

No agregues explicación, saludo ni puntuación extra.
Si el comentario no es una evaluación de una llamada, responde: no_aplica|no_aplica"""


comentario = "¿qué hora es en Tokio?"

# 2. EL PEDIDO
respuesta = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=20,
    thinking={"type": "disabled"},
    system= reglas,
    messages=[
        {"role": "user", "content":comentario},
    ],
)

# 3. LA BANDEJA
print([bloque.type for bloque in respuesta.content])
print("stop_reason:", respuesta.stop_reason)
for bloque in respuesta.content:
    if bloque.type == "text":
        print(bloque.text)
print("Tokens entrada:", respuesta.usage.input_tokens, "| salida:", respuesta.usage.output_tokens) # tokens de entrada y de salida
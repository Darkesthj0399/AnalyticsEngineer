from anthropic import Anthropic

# 1. EL CLIENTE (el mesero): se conecta y busca ANTHROPIC_API_KEY por su cuenta
client = Anthropic()

comentario = "Me llamaron tres veces esta semana para ofrecerme la tarjeta, ya dije que no. Igual el asesor fue amable."

# 2. EL PEDIDO
respuesta = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=1000,
    messages=[
        {"role": "user", "content": f"Clasifica este comentario de un cliente bancario en motivo y sentimiento: {comentario}"},
    ],
)

# 3. LA BANDEJA
print([bloque.type for bloque in respuesta.content])
print("stop_reason:", respuesta.stop_reason)
for bloque in respuesta.content:
    if bloque.type == "text":
        print(bloque.text)
print("Tokens entrada:", respuesta.usage.input_tokens, "| salida:", respuesta.usage.output_tokens) # tokens de entrada y de salida
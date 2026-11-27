from typing import Literal
from pydantic import BaseModel, ValidationError

class Respuesta(BaseModel):
    categoria: Literal["alimentos", "transporte", "no_aplica"]
    confianza: float

texto = '{"categoria": "ropa", "confianza": 0.9}'

try:
    r = Respuesta.model_validate_json(texto)
    print(r.categoria)
except ValidationError as e:
    print(e)
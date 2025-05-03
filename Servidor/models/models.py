from pydantic import BaseModel
from datetime import date

class RendimientoPartido(BaseModel):
    
    fecha: date
    rendimiento: float

    class Config:
        from_attributes = True  
# Modelo para la respuesta completa
class JugadorRendimiento(BaseModel):
    jugador_id: str
    partidos: list[RendimientoPartido]  
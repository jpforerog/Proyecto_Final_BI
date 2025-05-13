from pydantic import BaseModel
from datetime import date


class JugadoresRequest(BaseModel):
    jugadores_ids: list[str]

class RendimientoPartido(BaseModel):
    
    fecha: date
    rendimiento: float

    class Config:
        from_attributes = True  

class JugadorRendimiento(BaseModel):
    jugador_id: str
    partidos: list[RendimientoPartido]  

class JugadorCluster(BaseModel):
    jugador_id:str
    partidos: list[RendimientoPartido]
    posiciones: list[str]

    # Ejemplo 1: Método para calcular el rendimiento promedio
    def rendimiento_promedio(self) -> float:
        if not self.partidos:
            return 0.0
        return sum(p.rendimiento for p in self.partidos) / len(self.partidos)

    # Ejemplo 2: Método para verificar si una posición está en la lista
    def tiene_posicion(self, posicion: str) -> bool:
        return posicion.lower() in [p.lower() for p in self.posiciones]

    # Ejemplo 3: Método para filtrar partidos por umbral de rendimiento
    def partidos_efectivos(self, umbral: float = 7.0) -> list[RendimientoPartido]:
        return [p for p in self.partidos if p.rendimiento >= umbral]
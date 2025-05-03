# routers/jugadores.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from database.database import get_db

router = APIRouter(
    prefix="/jugadores",
    tags=["Jugadores"]
)


@router.get("/")
def obtener_jugadores(db: Session = Depends(get_db)):
    try:
        query= text("""
            SELECT DISTINCT jugador_id 
            FROM PARTIDOS 
            WHERE jugador_id IS NOT NULL
        """)
        result = db.execute(query)
        jugadores = [row.jugador_id for row in result]
        
        if not jugadores:
            raise HTTPException(
                status_code=404,
                detail="No se encontraron jugadores"
            )
            
        return {"jugadores_ids": jugadores}
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener jugadores: {str(e)}"
        )
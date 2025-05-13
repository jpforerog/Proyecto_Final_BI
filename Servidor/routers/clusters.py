# routers/clusters.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from database.database import get_db

router = APIRouter(
    prefix="/grupos",
    tags=["Grupos"]
)


@router.get("/{grupo_id}")
def obtener_jugadores_grupo(grupo_id:float,db: Session = Depends(get_db)):
    try:
        query= text("""
            SELECT DISTINCT jugador_id 
            FROM PARTIDOS 
            WHERE jugador_id IS NOT NULL
                    AND cluster = :grupo_id
        """)
        result = db.execute(query,{"grupo_id": grupo_id})
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
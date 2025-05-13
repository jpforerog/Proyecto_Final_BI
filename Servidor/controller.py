from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models.models import RendimientoPartido, JugadorRendimiento,JugadorCluster,JugadoresRequest
from database.database import  get_db
from sqlalchemy.sql import text
from routers.jugadores import router as jugadores_router
from routers.clusters import router as grupos_router

app = FastAPI()

app.include_router(jugadores_router)
app.include_router(grupos_router)



# Obtener todos los ítems
@app.get("/partidos/")
def read_items(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM PARTIDOS")).fetchall()
    return [row._asdict() for row in result]


@app.get("/partidos/{jugador_id}")
def read_items1(jugador_id: str , db: Session = Depends(get_db)):
    try:
        query = text("""
            SELECT * 
            FROM PARTIDOS 
            WHERE jugador_id = :jugador_id  
        """)
        
        # Ejecutar con parámetro
        result = db.execute(query, {"jugador_id": jugador_id})
        partidos = [row._asdict() for row in result]
        
        if not partidos:
            raise HTTPException(status_code=404, detail="No hay partidos")
            
        return partidos
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener partidos: {str(e)}"
        )

@app.get("/partidos/rendimiento/{jugador_id}", response_model=JugadorRendimiento)
def rendimiento_partido(jugador_id: str , db: Session = Depends(get_db)):
    try:
        # Consulta específica para las 2 columnas
        query = text("""
            SELECT Fecha, Rendimiento
            FROM PARTIDOS 
            WHERE Fecha IS NOT NULL 
              AND Rendimiento IS NOT NULL
                    AND jugador_id = :jugador_id
        """)
        result = db.execute(query,{"jugador_id":jugador_id})
        partidos = [
            {"fecha": row.Fecha, "rendimiento": row.Rendimiento}
            for row in result
        ]
        
        if not partidos:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontraron partidos para el jugador {jugador_id}"
            )
            
        return {
            "jugador_id": jugador_id,
            "partidos": partidos
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener datos: {str(e)}"
        )
    

@app.post("/partidos/grupo/", response_model=list[JugadorCluster])
def obtener_rendimiento_grupo(jugadores: JugadoresRequest, db: Session = Depends(get_db)):
    try:
        resultados = []
        
        for jugador_id in jugadores.jugadores_ids:
            # Consulta modificada para incluir posiciones
            query = text("""
                SELECT Fecha, Rendimiento, Posc
                FROM PARTIDOS 
                WHERE Fecha IS NOT NULL 
                    AND Rendimiento IS NOT NULL
                    AND Posc IS NOT NULL
                    AND jugador_id = :jugador_id
            """)
            
            result = db.execute(query, {"jugador_id": jugador_id})
            registros = result.fetchall()
            
            if not registros:
                continue  # O manejar error según necesidad
                
            # Procesar datos
            partidos = []
            posiciones = set()
            
            for row in registros:
                partidos.append({
                    "fecha": row.Fecha,
                    "rendimiento": row.Rendimiento
                })
                posiciones.add(row.Posc)
            
            resultados.append({
                "jugador_id": jugador_id,
                "partidos": partidos,
                "posiciones": list(posiciones)
            })
            
        return resultados
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar la solicitud: {str(e)}"
        )
    


"""# Obtener un ítem por ID
@app.get("/items/{item_id}")
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Ítem no encontrado")
    return item"""
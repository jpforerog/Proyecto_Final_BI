from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

# Configuración de la base de datos SQLite
#---------------------------------------------------------------------------------------------------------------
Path_completo = "C:/Users/jupaf/Documents/Proyectos_BI/Proyecto Final/Aplicacion/Servidor/database/partidos.db"
DATABASE_URL = f"sqlite:///{Path_completo}"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Proveedor de sesión de base de datos para inyección de dependencias.
    Uso:
    db = next(get_db())
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
from sqlalchemy import inspect
from database.database import engine

inspector = inspect(engine)
tablas = inspector.get_table_names()
print("Tablas en la base de datos:", tablas)
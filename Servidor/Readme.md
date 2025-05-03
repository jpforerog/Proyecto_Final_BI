Instalar requerimentos
pip install -r requirements.txt

crear la base de datos
python .\crear_database\csv_to_sqlite.py

Mover partidos.db a la carpeta database

Path_completo cambiar el path de la base de datos en database.py

iniciar servidor
uvicorn controller:app --reload
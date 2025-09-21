import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv('../.env')

DATABASE_URL = os.environ.get('DATABASE_URL')

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("Conexión exitosa:", result.fetchone())
except Exception as e:
    print("Error de conexión:", e)
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional
import os

# Cargar variables de entorno
load_dotenv()

# Configuración de la base de datos
DB_USER = os.getenv("MYSQL_USER")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
DB_HOST = os.getenv("MYSQL_HOST")
DB_PORT = os.getenv("MYSQL_PORT")
DB_NAME = os.getenv("MYSQL_DATABASE")

# Crear URL de conexión
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Crear motor de base de datos
engine = create_engine(DATABASE_URL)

# Crear aplicación FastAPI
app = FastAPI(title="NYT Articles API")

# Modelo Pydantic para los artículos
class Article(BaseModel):
    id: str
    web_url: str
    abstract: str
    print_sections: Optional[str] = None
    print_pages: Optional[str] = None
    main_headline: str
    multimedia_count: int
    average_of_height: Optional[float] = None
    median_of_width: Optional[float] = None
    keywords_count: int
    document_type: str
    pub_date: str
    word_count: int

    class Config:
        from_attributes = True

@app.get("/articles", response_model=list[Article])
async def get_all_articles():
    try:
        # Crear conexión
        with engine.connect() as connection:
            # Ejecutar consulta
            result = connection.execute(text("SELECT * FROM tb_nytimes_articles"))
            
            # Convertir resultados a lista de diccionarios
            articles = [row._mapping for row in result]
            
            return articles
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
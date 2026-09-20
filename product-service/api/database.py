from base import Base
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from models.produto import Produto

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

Base.metadata.create_all(engine)
print("Tabelas criadas com sucesso!")
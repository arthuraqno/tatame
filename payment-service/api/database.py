import os
from base import Base
from sqlalchemy import create_engine
from dotenv import load_dotenv
from models.pagamento import Pagamento

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

Base.metadata.create_all(engine)
print("Tabelas criadas com sucesso!")
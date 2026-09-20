from fastapi import FastAPI
from routes.produto import router as produto_router

app = FastAPI()
app.include_router(produto_router)

@app.get("/")
def home():
    {"messagem" : "Product Service funcionando!"}
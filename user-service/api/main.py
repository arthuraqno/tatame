from fastapi import FastAPI
from routes.usuario import router as usuario_router

app = FastAPI()
app.include_router(usuario_router)

@app.get("/")
def home():
    return {"mensagem": "User Service funcionando!"}
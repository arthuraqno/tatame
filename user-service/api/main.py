from fastapi import FastAPI
from routes.usuario import router as usuario_router
from routes.oauth import router as oauth_router

app = FastAPI()
app.include_router(usuario_router)
app.include_router(oauth_router)

@app.get("/")
def home():
    return {"mensagem": "User Service funcionando!"}
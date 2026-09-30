from fastapi import FastAPI
from routes.carrinho import router as carrinho_router

app = FastAPI()
app.include_router(carrinho_router)

@app.get("/")
def home():
    return {"mensagem": "Cart Service funcionando!"}
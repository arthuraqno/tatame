from fastapi import FastAPI
from routes.pedido import router as pedido_router

app = FastAPI()
app.include_router(pedido_router)

@app.get("/")
def home():
    return {"mensagem": "Order Service funcionando!"}
from fastapi import FastAPI
from routes.pagamento import router as pagamento_router

app = FastAPI()
app.include_router(pagamento_router)

app.get("/")
def home():
    return {"mensagem": "Payment Service funcionando!"}
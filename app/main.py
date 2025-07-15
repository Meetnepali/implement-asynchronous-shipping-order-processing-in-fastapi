import uvicorn
from fastapi import FastAPI
from app.routers import orders
import logging

app = FastAPI()

# Setup root logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s')

app.include_router(orders.router, prefix="/orders", tags=["orders"])

@app.get("/")
def root():
    return {"message": "Shipping Orders API"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)

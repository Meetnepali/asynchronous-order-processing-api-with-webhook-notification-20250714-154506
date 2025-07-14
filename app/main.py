from fastapi import FastAPI
from app.routers import orders

app = FastAPI(title="Asynchronous Order Processing API", description="Service to place and retrieve orders, and notify an external webhook asynchronously.")

# Routers
app.include_router(orders.router, prefix="/orders", tags=["Orders"])

from fastapi import FastAPI
from routers import product, client, order

app = FastAPI()

app.include_router(product.router)
app.include_router(client.router)
app.include_router(order.router)

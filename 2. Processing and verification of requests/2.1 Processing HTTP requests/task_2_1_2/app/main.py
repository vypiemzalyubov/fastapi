from fastapi import FastAPI
from app.models.product import Product


app = FastAPI()

sample_products = []


@app.get("/product/{product_id}")
async def get_product(product_id: int):
    pass


@app.get("/products/search")
async def get_product(keyword: str, category: str = None, limit: int = 10):
    pass

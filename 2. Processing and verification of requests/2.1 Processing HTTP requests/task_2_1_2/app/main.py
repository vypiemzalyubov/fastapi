from typing import Annotated
from fastapi import FastAPI, Path
from app.models.product import Product
from app.helper import get_product_by_id, get_products_by_parameters


app = FastAPI(title="Task 2.1.2")


@app.get("/product/{product_id}", response_model=Product)
async def get_product(product_id: Annotated[int, Path()]):
    return get_product_by_id(product_id)


@app.get("/products/search")
async def get_products_list(keyword: str, category: str = None, limit: int = 10):
    return get_products_by_parameters(keyword, category, limit)

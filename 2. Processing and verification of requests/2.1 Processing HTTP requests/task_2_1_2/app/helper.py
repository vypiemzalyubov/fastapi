from fastapi import HTTPException
from app.data import sample_products


def get_product_by_id(product_id) -> dict:
    product = [
        product for product in sample_products if product["product_id"] == product_id]
    if product:
        return product[0]
    else:
        raise HTTPException(
            status_code=404, detail=f"No product with id {product_id}")


def get_products_by_parameters(keyword: str, category: str = None, limit: int = 10) -> list:
    if category:
        filter_list = list(
            filter(lambda product: keyword in product["name"].lower() and category in product["category"], sample_products))
    else:
        filter_list = list(
            filter(lambda product: keyword in product["name"].lower(), sample_products))
    return filter_list[:limit]

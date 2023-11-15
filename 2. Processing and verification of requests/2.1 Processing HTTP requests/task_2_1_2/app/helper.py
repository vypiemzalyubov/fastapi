from fastapi import HTTPException


def get_product_by_id(product_id) -> dict:
    product = [product for product in sample_products if product["product_id"] == product_id]
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


sample_product_1 = {
    "product_id": 123,
    "name": "Smartphone",
    "category": "Electronics",
    "price": 599.99
}

sample_product_2 = {
    "product_id": 456,
    "name": "Phone Case",
    "category": "Accessories",
    "price": 19.99
}

sample_product_3 = {
    "product_id": 789,
    "name": "Iphone",
    "category": "Electronics",
    "price": 1299.99
}

sample_product_4 = {
    "product_id": 101,
    "name": "Headphones",
    "category": "Accessories",
    "price": 99.99
}

sample_product_5 = {
    "product_id": 202,
    "name": "Smartwatch",
    "category": "Electronics",
    "price": 299.99
}

sample_products = [sample_product_1, sample_product_2,
                   sample_product_3, sample_product_4, sample_product_5]

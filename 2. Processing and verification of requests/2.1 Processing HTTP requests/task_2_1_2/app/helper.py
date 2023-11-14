from fastapi import HTTPException


def get_product_by_id(product_id):
    for product in sample_products:
        for v in product.values():
            if v == product_id:
                return product
            else:
                raise HTTPException(
                    status_code=404, detail=f"No product with id {product_id}")


def get_products_by_parameters(keyword: str, category: str = None, limit: int = 10):
    filter_list = []
    if category:
        for product in sample_products:
            if keyword in product["name"].lower() and category in product["category"]:
                filter_list.append(product)
    else:
        for product in sample_products:
            if keyword in product["name"].lower():
                filter_list.append(product)
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

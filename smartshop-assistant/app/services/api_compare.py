import requests
from app import db
from app.models.product import Product

def fetch_and_save_products_from_apis():
    # API 1: Dummy JSON
    response1 = requests.get("https://api.escuelajs.co/api/v1/products")
    api1_products = []
    if response1.status_code == 200:
        data = response1.json()[:5]
        for item in data:
            product = Product.query.filter_by(name=item['title'], price=item['price']).first()
            if not product:
                product = Product(
                    name=item['title'],
                    price=item['price']
                )
                db.session.add(product)
                db.session.commit()
            db.session.refresh(product)
            api1_products.append(product)

    # API 2: Fake Store
    response2 = requests.get("https://fakestoreapi.com/products")
    api2_products = []
    if response2.status_code == 200:
        data = response2.json()[:5]  # Just get 2 products for demo
        for item in data:
            product = Product.query.filter_by(name=item['title'], price=item['price']).first()
            if not product:
                product = Product(
                    name=item['title'],
                    price=item['price']
                )
                db.session.add(product)
                db.session.commit()
            db.session.refresh(product)
            api2_products.append(product)

    return api1_products, api2_products

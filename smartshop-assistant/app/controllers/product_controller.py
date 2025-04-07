from flask import request, redirect, render_template, url_for
from flask_login import current_user, login_required
from app import db
from app.models.product import Product
from app.models.product_preference import ProductPreference
from app.services.api_compare import fetch_and_save_products_from_apis

class ProductController:

    @staticmethod
    @login_required
    def index():
        """
        Display the product list (home page).
        """
        products = Product.query.all()
        return render_template('index.html', products=products)

    @staticmethod
    @login_required
    def add_product():
        """
        Add a new product to the database.
        """
        name = request.form['name']
        price = float(request.form['price'])
        product = Product(name=name, price=price)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('main.index'))

    @staticmethod
    @login_required
    def save_preference():
        """
        Save a user's product preference to the database.
        """
        product_id = request.form['product_id']
        existing = ProductPreference.query.filter_by(user_id=current_user.id, product_id=product_id).first()

        if not existing:
            preference = ProductPreference(user_id=current_user.id, product_id=product_id)
            db.session.add(preference)
            db.session.commit()

        return redirect(url_for('main.index'))

    @staticmethod
    @login_required
    def compare_products():
        """
        Compare products from external APIs and store them.
        """
        products = fetch_and_save_products_from_apis()
        return render_template('compare.html', products=products)

    @staticmethod
    @login_required
    def dashboard():
        """
        Display the user's product preferences.
        """
        preferences = ProductPreference.query.filter_by(user_id=current_user.id).all()
        return render_template('dashboard.html', preferences=preferences)

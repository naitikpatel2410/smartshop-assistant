from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user, login_user, logout_user
from app import db
from app.models.product import Product
from app.models.product_preference import ProductPreference
from app.models.user import User  # Import User model
from app.services.api_compare import fetch_and_save_products_from_apis

main_bp = Blueprint('main', __name__)

# Login Route
@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    print("User already authenticated:", current_user.is_authenticated)

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))  # Redirect to the home page if already logged in

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Fetch user by username
        user = User.query.filter_by(username=username).first()

        # Check if user exists and passwords match
        if user and user.password == password:  # Not hashing passwords, as per your request
            login_user(user)
            return redirect(url_for('main.index'))  # Redirect to the home page after login
        else:
            return "Invalid login credentials", 400

    return render_template('login.html')

@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

# Home Page (Shows Products and Preferences)
@main_bp.route('/')
@login_required
def index():
    # Show products and preferences
    products = Product.query.all()
    preferences = ProductPreference.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', products=products, preferences=preferences)


# Search Route
@main_bp.route('/search', methods=['POST'])
@login_required
def search():
    api1_products, api2_products = fetch_and_save_products_from_apis()
    preferences = ProductPreference.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', api1_products=api1_products, api2_products=api2_products, preferences=preferences)



# Add Product Preference Route (Saves preference without redirecting)
@main_bp.route('/add_preference/<int:product_id>', methods=['POST'])
@login_required
def add_preference(product_id):
    # Save the user preference without redirecting
    preference = ProductPreference(user_id=current_user.id, product_id=product_id)
    db.session.add(preference)
    db.session.commit()

    # Fetch updated preferences and products
    products = Product.query.all()
    preferences = ProductPreference.query.filter_by(user_id=current_user.id).all()

    # Render the same page with updated data
    return render_template('index.html', products=products, preferences=preferences)


# Dashboard Route (Shows the saved preferences)
@main_bp.route('/dashboard')
@login_required
def dashboard():
    preferences = ProductPreference.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', preferences=preferences)

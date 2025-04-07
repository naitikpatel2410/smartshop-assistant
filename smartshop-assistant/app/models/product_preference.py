from app import db
from app.models.product import Product
from app.models.user import User

class ProductPreference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('preferences', lazy=True))
    product = db.relationship('Product', backref=db.backref('preferences', lazy=True))  # Add this line

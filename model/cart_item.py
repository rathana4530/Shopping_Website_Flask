from app import db
from datetime import datetime


class CartItem(db.Model):
    __tablename__ = 'cart_item'
    cart_item_id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.cart_id'), nullable=False)
    variant_id = db.Column(db.Integer, db.ForeignKey('product_variants.variant_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price = db.Column(db.Numeric(10, 2), nullable=False)

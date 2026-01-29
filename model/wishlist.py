from app import db
from datetime import datetime

class Wishlist(db.Model):
    __tablename__ = 'wishlist'
    wishlist_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
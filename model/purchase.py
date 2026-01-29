from app import db
from datetime import datetime

class Purchase(db.Model):
    __tablename__ = 'purchase'
    purchase_id = db.Column(db.Integer, primary_key=True)
    total_amount = db.Column(db.Numeric(12, 2), nullable=False)
    purchase_status = db.Column(db.String(50), nullable=False, default='pending')
    payment_method = db.Column(db.String(50), nullable=False)
    payment_status = db.Column(db.String(50), nullable=False, default='unpaid')
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)

    # items = db.relationship('PurchaseItem', backref='purchase', lazy=True, cascade='all, delete-orphan')

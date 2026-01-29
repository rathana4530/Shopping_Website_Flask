from app import db
from sqlalchemy import text
from datetime import datetime
import enum


class Order(db.Model):
    __tablename__ = 'order'
    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    total_amount = db.Column(db.Numeric(12, 2), nullable=False)
    order_status = db.Column(db.String(50), nullable=False, default='pending')
    payment_method = db.Column(db.String(50), nullable=False)
    payment_status = db.Column(db.String(50), nullable=False, default='unpaid')
    coupons_code = db.Column(db.String(10))
    discount_value = db.Column(db.Numeric(10, 2), default=0)
    address = db.Column(db.Text, nullable=False)
    delivery_status = db.Column(db.String(50), nullable=False, default='pending')
    order_date = db.Column(db.DateTime, default=datetime.utcnow)


# ==================================================

def getOrderyList():
    try:
        return Order.query.all()

    except Exception as e:
        print(f"Error fetching order: {e}")
        return []

def getOrderById(order_id:int):
    try:
        order = Order.query.get_or_404(order_id)
        if order is None:
            return {'Error': 'Order not found'}
        return order

    except Exception as e:
        print(f"Error fetching order: {e}")
        return []

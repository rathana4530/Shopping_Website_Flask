from app import db
from sqlalchemy import text
from datetime import datetime
import enum


class OrderItem(db.Model):
    __tablename__ = 'order_item'
    order_item_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'), nullable=False)
    variant_id = db.Column(db.Integer, db.ForeignKey('product_variants.variant_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)


# ==================================================

def getOrderDetailsById(order_id:int):
    try:
        order_item = OrderItem.query.get_or_404(order_id)
        if order_item is None:
            return {'Error': 'Order details not found'}
        return order_item

    except Exception as e:
        print(f"Error fetching order details: {e}")
        return []

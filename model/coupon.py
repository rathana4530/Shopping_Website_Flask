from app import db

class Coupon(db.Model):
    __tablename__ = 'coupon'
    coupon_id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    discount_type = db.Column(db.String(50), nullable=False)
    discount_value = db.Column(db.Numeric(10, 2), nullable=False)
    min_order_amount = db.Column(db.Numeric(10, 2))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(db.Boolean, default=True)
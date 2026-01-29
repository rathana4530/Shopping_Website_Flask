from app import db

class PurchaseItem(db.Model):
    __tablename__ = 'purchase_item'
    purchase_item_id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchase.purchase_id'), nullable=False)
    variant_id = db.Column(db.Integer, db.ForeignKey('product_variants.variant_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
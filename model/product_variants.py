from app import db
from sqlalchemy import text


class ProductVariant(db.Model):
    __tablename__ = 'product_variants'
    variant_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    color_id = db.Column(db.Integer, db.ForeignKey('color.color_id'), nullable=False)
    size_id = db.Column(db.Integer, db.ForeignKey('size.size_id'), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    sku = db.Column(db.String(100), unique=True)

    # cart_items = db.relationship('CartItem', backref='variant', lazy=True)
    # order_items = db.relationship('OrderItem', backref='variant', lazy=True)
    # purchase_items = db.relationship('PurchaseItem', backref='variant', lazy=True)

def getAllProductVariant():
    try:
        return ProductVariant.query.all()
    except Exception as e:
        print(f"Error fetching product variants: {e}")
        return []


def getProductVariantbyId(variant_id: int):
    try:
        varint = ProductVariant.query.get_or_404(variant_id)
        if varint is None:
            return {'Error': 'Product variant not found'}
        return varint

    except Exception as e:
        print(f"Error fetching Product variant: {e}")
        return []
from app import db
from sqlalchemy import text


class Product(db.Model):
    __tablename__ = 'product'
    product_id = db.Column(db.Integer, primary_key=True)
    productname = db.Column(db.String(128), nullable=False)
    barcode = db.Column(db.String(128), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(128))
    description = db.Column(db.String(128))

    multi_images = db.relationship(
        'MultiImage',
        backref='product',
        cascade='all, delete-orphan'
    )


def getAllProduct():
    try:
        return Product.query.all()
    except Exception as e:
        print(f"Error fetching product: {e}")
        return []


def getProductbyId(product_id: int):
    try:
        product = Product.query.get_or_404(product_id)
        if product is None:
            return {'Error': 'Product not found'}
        return product

    except Exception as e:
        print(f"Error fetching product: {e}")
        return []
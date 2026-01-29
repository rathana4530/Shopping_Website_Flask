from app import db
from sqlalchemy import text

class MultiImage(db.Model):
    __tablename__ = 'multi_image'

    multi_image_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    image = db.Column(db.String(255), nullable=False)

def getProductImages(product_id: int):
    try:
        images = MultiImage.query.filter_by(product_id=product_id).all()
        if images is None:
            return {'Error': 'Image not found'}
        return images

    except Exception as e:
        print(f"Error fetching image: {e}")
        return []
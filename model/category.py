from app import db
from sqlalchemy import text


class Category(db.Model):
    __tablename__ = 'category'
    category_id = db.Column(db.Integer, primary_key=True)
    categoryname = db.Column(db.String(128), unique=True, nullable=False)
    description = db.Column(db.String(128))

    products = db.relationship('Product', backref='category')

def getCategoryList():
    try:
        return Category.query.all()

    except Exception as e:
        print(f"Error fetching categories: {e}")
        return []

def getCategoryById(category_id:int):
    try:
        category = Category.query.get_or_404(category_id)
        if category is None:
            return {'Error': 'Category not found'}
        return category

    except Exception as e:
        print(f"Error fetching categories: {e}")
        return []

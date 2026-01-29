from app import db
from sqlalchemy import text


class Size(db.Model):
    __tablename__ = 'size'
    size_id = db.Column(db.Integer, primary_key=True)
    size_name = db.Column(db.String(128), unique=True, nullable=False)

    # variants = db.relationship('ProductVariant', backref='size', lazy=True)


def getSizeList():
    try:
        return Size.query.all()

    except Exception as e:
        print(f"Error fetching size: {e}")
        return []

def getSizeById(size_id:int):
    try:
        size = Size.query.get_or_404(size_id)
        if size is None:
            return {'Error': 'size not found'}
        return size

    except Exception as e:
        print(f"Error fetching size: {e}")
        return []

from app import db
from sqlalchemy import text


class Color(db.Model):
    __tablename__ = 'color'
    color_id = db.Column(db.Integer, primary_key=True)
    color_name = db.Column(db.String(128), unique=True, nullable=False)
    color_code = db.Column(db.String(128))

    # variants = db.relationship('ProductVariant', backref='color', lazy=True)

def getColorList():
    try:
        return Color.query.all()

    except Exception as e:
        print(f"Error fetching color: {e}")
        return []

def getColorById(color_id:int):
    try:
        color = Color.query.get_or_404(color_id)
        if color is None:
            return {'Error': 'color not found'}
        return color

    except Exception as e:
        print(f"Error fetching color: {e}")
        return []

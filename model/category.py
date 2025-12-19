from app import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    categoryname = db.Column(db.String(128), unique=True, nullable=False)
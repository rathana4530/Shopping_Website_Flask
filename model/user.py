from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    image = db.Column(db.Text)
    status = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # carts = db.relationship('Cart', backref='user', lazy=True)
    # orders = db.relationship('Order', backref='user', lazy=True)
    # wishlists = db.relationship('Wishlist', backref='user', lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

# ==========================================================

def getAllUser():
    try:
        return User.query.all()
    except Exception as e:
        print(f"Error fetching user: {e}")
        return []


def getUserbyId(user_id: int):
    try:
        user = User.query.get_or_404(user_id)
        if user is None:
            return {'Error': 'User not found'}
        return user

    except Exception as e:
        print(f"Error fetching user: {e}")
        return []

def getUserByName(username: str):
    try:
        user = User.query.filter_by(username=username).first()
        if user is None:
            return {'Error': 'User not found'}
        return user
    except Exception as e:
        print(f"Error fetching user: {e}")
        return []
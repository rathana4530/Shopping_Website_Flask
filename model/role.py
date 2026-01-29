from app import db


class Role(db.Model):
    __tablename__ = 'role'
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), nullable=False)

    # users = db.relationship('User', backref='role', lazy=True)


def getAllRole():
    try:
        return Role.query.all()
    except Exception as e:
        print(f"Error fetching role: {e}")
        return []

def getRolebyId(role_id: int):
    try:
        role = Role.query.get_or_404(role_id)
        if role is None:
            return {'Error': 'role not found'}
        return role

    except Exception as e:
        print(f"Error fetching role: {e}")
        return []
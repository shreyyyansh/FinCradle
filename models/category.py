from extensions import db

class Category(db.Model):
    __tablename__ = "categories"   # ← THIS FIXES IT

    category_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(10), nullable=False)  # income or expense
    include_weekly = db.Column(db.Boolean, default=True)
    include_monthly = db.Column(db.Boolean, default=True)
    include_yearly = db.Column(db.Boolean, default=True)

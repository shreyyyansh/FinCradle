from extensions import db

class Income(db.Model):
    __tablename__ = "income"

    income_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    category_id = db.Column(db.Integer)
    amount = db.Column(db.Float)
    date = db.Column(db.Date)

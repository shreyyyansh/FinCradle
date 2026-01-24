from extensions import db

class Expense(db.Model):
    __tablename__ = "expenses"

    expense_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    category_id = db.Column(db.Integer)
    amount = db.Column(db.Float)
    date = db.Column(db.Date)
    note = db.Column(db.String(200))

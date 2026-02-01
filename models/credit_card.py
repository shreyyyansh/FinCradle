from extensions import db

class CreditCard(db.Model):
    __tablename__ = "credit_cards"   # ✅ MUST MATCH DB

    card_id = db.Column(db.Integer, primary_key=True)
    bank = db.Column(db.String(100))
    card_name = db.Column(db.String(100))

from extensions import db

class CardReward(db.Model):
    reward_id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey("credit_card.card_id"))
    category_id = db.Column(db.Integer, db.ForeignKey("category.category_id"))
    cashback_percent = db.Column(db.Float)

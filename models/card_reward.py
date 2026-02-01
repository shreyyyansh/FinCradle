from extensions import db

class CardReward(db.Model):
    __tablename__ = "card_rewards"   # ✅ MUST MATCH DB

    reward_id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey("credit_cards.card_id"))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.category_id"))
    cashback_percent = db.Column(db.Float)

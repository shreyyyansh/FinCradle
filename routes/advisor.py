from flask import Blueprint, render_template
from flask_login import login_required, current_user
from extensions import db
from models.expense import Expense
from models.category import Category
from models.credit_card import CreditCard
from models.card_reward import CardReward

advisor = Blueprint("advisor", __name__)

@advisor.route("/ai-advisor")
@login_required
def ai_advisor():

    expenses = Expense.query.filter_by(user_id=current_user.user_id).all()
    cards = CreditCard.query.all()
    rewards = CardReward.query.all()

    report = []
    total_missed = 0

    for e in expenses:
        best = None
        best_cashback = 0

        for r in rewards:
            if r.category_id == e.category_id:
                cashback = (r.cashback_percent/100) * e.amount
                if cashback > best_cashback:
                    best_cashback = cashback
                    best = CreditCard.query.get(r.card_id)

        if best:
            total_missed += best_cashback
            report.append({
                "category": e.category.name,
                "amount": e.amount,
                "best_card": best.card_name,
                "bank": best.bank,
                "cashback": round(best_cashback,2)
            })

    return render_template("ai_advisor.html",
                           report=report,
                           total_missed=round(total_missed,2))

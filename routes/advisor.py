from flask import Blueprint, render_template
from flask_login import login_required, current_user
from extensions import db
from models.income import Income
from models.expense import Expense
from models.card_reward import CardReward
from models.credit_card import CreditCard

advisor = Blueprint("advisor", __name__)

@advisor.route("/advisor")
@login_required
def advisor_home():

    # ---------- TOTALS ----------
    total_income = db.session.query(
        db.func.coalesce(db.func.sum(Income.amount), 0)
    ).filter_by(user_id=current_user.user_id).scalar()

    total_expense = db.session.query(
        db.func.coalesce(db.func.sum(Expense.amount), 0)
    ).filter_by(user_id=current_user.user_id).scalar()

    # ---------- OVESPENDING ----------
    overspending = None
    if total_income > 0 and total_expense > total_income:
        overspending = "You are spending more than your income."
    elif total_income > 0 and total_expense / total_income > 0.7:
        overspending = "Your expenses exceed 70% of your income."
    else:
        overspending = "Your spending is under control."

    # ---------- TREND ----------
    trend = "Add more transactions to detect trends."
    if total_income > 0:
        if total_expense < total_income * 0.5:
            trend = "Excellent saving trend."
        elif total_expense < total_income * 0.8:
            trend = "Stable spending trend."
        else:
            trend = "Rising expense trend."

    # ---------- CARD RECOMMENDATION ----------
    card_tip = None
    top_card = (
    db.session.query(CreditCard.card_name, CreditCard.bank)
    .join(CardReward, CreditCard.card_id == CardReward.card_id)
    .order_by(CardReward.cashback_percent.desc())
    .first()
    )


    if top_card:
        card_tip = f"Use {top_card.card_name} ({top_card.bank}) for maximum cashback."

    return render_template(
        "advisor.html",
        income=total_income,
        expense=total_expense,
        overspending=overspending,
        trend=trend,
        card_tip=card_tip
    )

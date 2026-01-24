from flask import Blueprint, send_file
from flask_login import login_required, current_user
from extensions import db
from models.expense import Expense
from models.category import Category
from sqlalchemy import extract
from datetime import date, timedelta
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import io
from models.income import Income


ai = Blueprint("ai", __name__)

# ---------------- WEEKLY ----------------
@ai.route("/weekly-report")
@login_required
def weekly():
    today = date.today()
    start = today - timedelta(days=today.weekday())

    data = db.session.query(
        Category.name,
        db.func.sum(Expense.amount)
    ).select_from(Expense).join(
        Category, Category.category_id == Expense.category_id
    ).filter(
        Expense.user_id == current_user.user_id,
        Category.include_weekly == True,
        Expense.date >= start
    ).group_by(Category.name).all()

    return {"weekly": [[c, float(a)] for c, a in data]}

# ---------------- MONTHLY ----------------
@ai.route("/monthly-report")
@login_required
def monthly():
    m = date.today().month
    y = date.today().year

    data = db.session.query(
        Category.name,
        db.func.sum(Expense.amount)
    ).select_from(Expense).join(
        Category, Category.category_id == Expense.category_id
    ).filter(
        Expense.user_id == current_user.user_id,
        Category.include_monthly == True,
        extract("month", Expense.date) == m,
        extract("year", Expense.date) == y
    ).group_by(Category.name).all()

    return {"monthly": [[c, float(a)] for c, a in data]}

# ---------------- YEARLY ----------------
@ai.route("/yearly-report")
@login_required
def yearly():
    y = date.today().year

    data = db.session.query(
        Category.name,
        db.func.sum(Expense.amount)
    ).select_from(Expense).join(
        Category, Category.category_id == Expense.category_id
    ).filter(
        Expense.user_id == current_user.user_id,
        Category.include_yearly == True,
        extract("year", Expense.date) == y
    ).group_by(Category.name).all()

    return {"yearly": [[c, float(a)] for c, a in data]}

# ---------------- AI SUMMARY ----------------
@ai.route("/ai-summary")
@login_required
def ai_summary():
    total = db.session.query(db.func.sum(Expense.amount)).filter(
        Expense.user_id == current_user.user_id
    ).scalar() or 0

    return {"summary": f"You have spent ₹{float(total):.2f} this year."}

# ---------------- OVESPEND ----------------
@ai.route("/overspend")
@login_required
def overspend():
    m = date.today().month
    y = date.today().year

    this_month = db.session.query(db.func.sum(Expense.amount)).filter(
        Expense.user_id == current_user.user_id,
        extract("month", Expense.date) == m,
        extract("year", Expense.date) == y
    ).scalar() or 0

    last_month = db.session.query(db.func.sum(Expense.amount)).filter(
        Expense.user_id == current_user.user_id,
        extract("month", Expense.date) == m - 1,
        extract("year", Expense.date) == y
    ).scalar() or 0

    if this_month > last_month:
        msg = "You are spending more than last month."
    else:
        msg = "Your spending is under control."

    return {"message": msg}

# ---------------- TREND ----------------
@ai.route("/trend")
@login_required
def trend():
    return {"trend": "Your financial trend will improve as more data is added."}

# ---------------- PDF ----------------
@ai.route("/download-pdf")
@login_required
def download_pdf():
    buffer = io.BytesIO()
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(buffer)
    elements = []

    elements.append(Paragraph("Expense Report", styles["Title"]))
    elements.append(Paragraph(f"User ID: {current_user.user_id}", styles["Normal"]))
    elements.append(Paragraph(" ", styles["Normal"]))

    data = db.session.query(
        Category.name,
        db.func.sum(Expense.amount)
    ).select_from(Expense).join(
        Category, Category.category_id == Expense.category_id
    ).filter(
        Expense.user_id == current_user.user_id
    ).group_by(Category.name).all()

    for c, amt in data:
        elements.append(Paragraph(f"{c}: ₹{float(amt):.2f}", styles["Normal"]))

    doc.build(elements)
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="expense_report.pdf", mimetype="application/pdf")


@ai.route("/income-expense")
@login_required
def income_vs_expense():
    income = db.session.query(db.func.sum(Income.amount)).filter(
        Income.user_id == current_user.user_id
    ).scalar() or 0

    expense = db.session.query(db.func.sum(Expense.amount)).filter(
        Expense.user_id == current_user.user_id
    ).scalar() or 0

    savings = income - expense

    return {
        "finance": [
            ["Income", float(income)],
            ["Expense", float(expense)],
            ["Savings", float(savings)]
        ]
    }

@ai.route("/category-leak")
@login_required
def category_leak():
    m = date.today().month
    y = date.today().year

    data = db.session.query(
        Category.name,
        db.func.sum(db.case((extract("month", Expense.date)==m, Expense.amount), else_=0)),
        db.func.sum(db.case((extract("month", Expense.date)==m-1, Expense.amount), else_=0))
    ).select_from(Expense).join(
        Category, Category.category_id == Expense.category_id
    ).filter(
        Expense.user_id == current_user.user_id
    ).group_by(Category.name).all()

    alerts = []

    for name, this_m, last_m in data:
        this_m = this_m or 0
        last_m = last_m or 0

        if last_m > 0:
            change = ((this_m - last_m) / last_m) * 100

            if change > 20:
                alerts.append(f"{name} increased by {round(change,1)}%")

    if not alerts:
        return {"leak": "No abnormal category increase detected."}

    return {"leak": " | ".join(alerts)}

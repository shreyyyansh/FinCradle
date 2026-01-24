from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from extensions import db
from models.income import Income
from models.expense import Expense
from models.category import Category
from datetime import date

finance = Blueprint("finance", __name__)

@finance.route("/dashboard")
@login_required
def dashboard():
    incomes = Income.query.filter_by(user_id=current_user.user_id).all()
    expenses = Expense.query.filter_by(user_id=current_user.user_id).all()

    income_cats = Category.query.filter_by(user_id=current_user.user_id, type="income").all()
    expense_cats = Category.query.filter_by(user_id=current_user.user_id, type="expense").all()

    total_income = sum(i.amount for i in incomes)
    total_expense = sum(e.amount for e in expenses)

    return render_template("dashboard.html",
        incomes=incomes,
        expenses=expenses,
        savings=total_income-total_expense,
        income_categories=income_cats,
        expense_categories=expense_cats
    )

@finance.route("/add-income", methods=["POST"])
@login_required
def add_income():
    new = Income(
        user_id=current_user.user_id,
        category_id=request.form["category"],
        amount=request.form["amount"],
        date=date.today()
    )
    db.session.add(new)
    db.session.commit()
    return redirect(url_for("finance.dashboard"))

@finance.route("/add-expense", methods=["POST"])
@login_required
def add_expense():
    new = Expense(
        user_id=current_user.user_id,
        category_id=request.form["category"],
        amount=request.form["amount"],
        date=date.today(),
        note=request.form["note"]
    )
    db.session.add(new)
    db.session.commit()
    return redirect(url_for("finance.dashboard"))

@finance.route("/categories", methods=["GET","POST"])
@login_required
def categories():
    if request.method=="POST":
        cat = Category(
            user_id=current_user.user_id,
            name=request.form["name"],
            type=request.form["type"],
            include_weekly=bool(request.form.get("weekly")),
            include_monthly=bool(request.form.get("monthly")),
            include_yearly=bool(request.form.get("yearly"))
        )
        db.session.add(cat)
        db.session.commit()

    cats = Category.query.filter_by(user_id=current_user.user_id).all()
    return render_template("categories.html", categories=cats)

@finance.route("/delete-category/<int:id>")
@login_required
def delete_category(id):
    cat = Category.query.get(id)
    db.session.delete(cat)
    db.session.commit()
    return redirect(url_for("finance.categories"))

@finance.route("/income-expense")
@login_required
def income_expense():
    from sqlalchemy import func

    income_data = db.session.query(
        func.date(Income.date),
        func.sum(Income.amount)
    ).filter(Income.user_id==current_user.user_id).group_by(func.date(Income.date)).all()

    expense_data = db.session.query(
        func.date(Expense.date),
        func.sum(Expense.amount)
    ).filter(Expense.user_id==current_user.user_id).group_by(func.date(Expense.date)).all()

    data = {}

    for d,amt in income_data:
        data[str(d)] = {"income": float(amt), "expense": 0}

    for d,amt in expense_data:
        if str(d) not in data:
            data[str(d)] = {"income":0,"expense":float(amt)}
        else:
            data[str(d)]["expense"] = float(amt)

    result = []
    for k in sorted(data.keys()):
        result.append({
            "date": k,
            "income": data[k]["income"],
            "expense": data[k]["expense"]
        })

    return {"finance": result}

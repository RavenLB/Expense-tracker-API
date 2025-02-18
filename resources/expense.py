from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
from sqlalchemy import func

from db import db
from models import ExpenseModel, CategoryModel
from schemas import ExpenseSchema, ExpenseUpdateSchema, ExpenseSummarySchema

blp = Blueprint("Expenses", __name__, description="Operations on expenses")

@blp.route("/expense/<int:expense_id>")
class Expense(MethodView):
    @jwt_required()
    @blp.response(200, ExpenseSchema)
    def get(self, expense_id):
        user_id = get_jwt_identity()
        expense = ExpenseModel.query.filter_by(id=expense_id, user_id=user_id).first()
        if not expense:
            abort(404, message="Expense not found.")
        return expense

    @jwt_required()
    def delete(self, expense_id):
        user_id = get_jwt_identity()
        expense = ExpenseModel.query.filter_by(id=expense_id, user_id=user_id).first()
        if not expense:
            abort(404, message="Expense not found.")
        
        db.session.delete(expense)
        db.session.commit()
        return {"message": "Expense deleted."}

    @jwt_required()
    @blp.arguments(ExpenseUpdateSchema)
    @blp.response(200, ExpenseSchema)
    def put(self, expense_data, expense_id):
        user_id = get_jwt_identity()
        expense = ExpenseModel.query.filter_by(id=expense_id, user_id=user_id).first()
        if not expense:
            abort(404, message="Expense not found.")

        if expense_data.get("category_id"):
            if not CategoryModel.query.get(expense_data["category_id"]):
                abort(404, message="Category not found.")

        for key, value in expense_data.items():
            setattr(expense, key, value)

        db.session.add(expense)
        db.session.commit()
        return expense

@blp.route("/expense")
class ExpenseList(MethodView):
    @jwt_required()
    @blp.response(200, ExpenseSchema(many=True))
    def get(self):
        user_id = get_jwt_identity()
        return ExpenseModel.query.filter_by(user_id=user_id).all()

    @jwt_required()
    @blp.arguments(ExpenseSchema)
    @blp.response(201, ExpenseSchema)
    def post(self, expense_data):
        user_id = get_jwt_identity()
        if not CategoryModel.query.get(expense_data["category_id"]):
            abort(404, message="Category not found.")

        expense = ExpenseModel(**expense_data, user_id=user_id)
        try:
            db.session.add(expense)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return expense

@blp.route("/expense/summary")
class ExpenseSummary(MethodView):
    @jwt_required()
    @blp.response(200, ExpenseSummarySchema)
    def get(self):
        user_id = get_jwt_identity()
        expenses = ExpenseModel.query.filter_by(user_id=user_id).all()
        
        total = sum(expense.amount for expense in expenses)
        count = len(expenses)
        average = total / count if count > 0 else 0
        
        categories = {}
        for expense in expenses:
            cat_name = expense.category.name
            categories[cat_name] = categories.get(cat_name, 0) + expense.amount

        return {
            "total_amount": total,
            "count": count,
            "average": average,
            "categories": categories
        }

@blp.route("/expense/summary/<string:period>")
class ExpensePeriodSummary(MethodView):
    @jwt_required()
    @blp.response(200, ExpenseSummarySchema)
    def get(self, period):
        user_id = get_jwt_identity()
        now = datetime.utcnow()

        if period == "week":
            start_date = now - timedelta(days=7)
        elif period == "month":
            start_date = now - timedelta(days=30)
        elif period == "three_months":
            start_date = now - timedelta(days=90)
        else:
            abort(400, message="Invalid period. Use 'week', 'month', or 'three_months'")

        expenses = ExpenseModel.query.filter(
            ExpenseModel.user_id == user_id,
            ExpenseModel.date >= start_date
        ).all()

        total = sum(expense.amount for expense in expenses)
        count = len(expenses)
        average = total / count if count > 0 else 0

        categories = {}
        for expense in expenses:
            cat_name = expense.category.name
            categories[cat_name] = categories.get(cat_name, 0) + expense.amount

        return {
            "total_amount": total,
            "count": count,
            "average": average,
            "categories": categories
        }
from db import db
from datetime import datetime
from sqlalchemy.schema import CheckConstraint


class ExpenseModel(db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.Float(precision=2), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    category = db.relationship("CategoryModel", back_populates="expenses")
    user = db.relationship("UserModel", back_populates="expenses")

    __table_args__ = (
        CheckConstraint('amount > 0', name='check_positive_amount'),
    )
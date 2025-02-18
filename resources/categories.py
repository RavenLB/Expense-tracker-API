from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import CategoryModel
from schemas import CategorySchema

blp = Blueprint("Categories", __name__, description="Operations on categories")

@blp.route("/category/<int:category_id>")
class Category(MethodView):
    @jwt_required()
    @blp.response(200, CategorySchema)
    def get(self, category_id):
        category = CategoryModel.query.get_or_404(category_id)
        return category

    @jwt_required()
    def delete(self, category_id):
        category = CategoryModel.query.get_or_404(category_id)
        if category.expenses.all():
            abort(400, message="Cannot delete category with expenses.")
        db.session.delete(category)
        db.session.commit()
        return {"message": "Category deleted."}

@blp.route("/category")
class CategoryList(MethodView):
    @jwt_required()
    @blp.response(200, CategorySchema(many=True))
    def get(self):
        return CategoryModel.query.all()

    @jwt_required()
    @blp.arguments(CategorySchema)
    @blp.response(201, CategorySchema)
    def post(self, category_data):
        category = CategoryModel(**category_data)
        try:
            db.session.add(category)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A category with that name already exists.")
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return category

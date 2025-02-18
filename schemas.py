from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

class PlainExpenseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    amount = fields.Float(required=True, validate=validate.Range(min=0.01))
    date = fields.DateTime(required=True)

class PlainCategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))

class ExpenseSchema(PlainExpenseSchema):
    category_id = fields.Int(required=True, load_only=True)
    user_id = fields.Int(dump_only=True)
    category = fields.Nested(PlainCategorySchema(), dump_only=True)

class CategorySchema(PlainCategorySchema):
    expenses = fields.List(fields.Nested(PlainExpenseSchema()), dump_only=True)

class ExpenseUpdateSchema(Schema):
    name = fields.Str()
    amount = fields.Float()
    date = fields.DateTime()
    category_id = fields.Int()

class ExpenseSummarySchema(Schema):
    total_amount = fields.Float()
    count = fields.Int()
    average = fields.Float()
    categories = fields.Dict(keys=fields.Str(), values=fields.Float())
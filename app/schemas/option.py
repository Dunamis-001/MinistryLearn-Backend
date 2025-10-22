from marshmallow import Schema, fields, validate


class OptionSchema(Schema):
    id = fields.Int(dump_only=True)
    question_id = fields.Int()
    text = fields.Str()
    is_correct = fields.Bool()


class OptionCreateSchema(Schema):
    text = fields.Str(required=True, validate=validate.Length(min=1, max=500))
    is_correct = fields.Bool(missing=False)
from marshmallow import Schema, fields, validate


class QuestionSchema(Schema):
    id = fields.Int(dump_only=True)
    assessment_id = fields.Int()
    prompt = fields.Str()
    type = fields.Str(validate=validate.OneOf(['mcq', 'short_answer']))
    points = fields.Int()
    position = fields.Int()


class QuestionCreateSchema(Schema):
    prompt = fields.Str(required=True, validate=validate.Length(min=1, max=1000))
    type = fields.Str(required=True, validate=validate.OneOf(['mcq', 'short_answer']))
    points = fields.Int(missing=1, validate=validate.Range(min=1, max=100))
    position = fields.Int(missing=1)


class QuestionUpdateSchema(Schema):
    prompt = fields.Str(validate=validate.Length(min=1, max=1000))
    type = fields.Str(validate=validate.OneOf(['mcq', 'short_answer']))
    points = fields.Int(validate=validate.Range(min=1, max=100))
    position = fields.Int()
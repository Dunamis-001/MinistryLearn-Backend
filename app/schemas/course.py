from marshmallow import Schema, fields, validate


class CourseSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    category = fields.Str()
    difficulty = fields.Str(validate=validate.OneOf(['Beginner', 'Intermediate', 'Advanced']))
    campus = fields.Str()

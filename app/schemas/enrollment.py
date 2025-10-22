from marshmallow import Schema, fields, validate


class EnrollmentSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int()
    course_id = fields.Int()
    status = fields.Str(validate=validate.OneOf(['active', 'completed', 'dropped']))
    progress = fields.Int(validate=validate.Range(min=0, max=100))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class EnrollmentCreateSchema(Schema):
    course_id = fields.Int(required=True)
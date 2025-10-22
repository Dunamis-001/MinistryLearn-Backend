from marshmallow import Schema, fields, validate


class AssessmentSchema(Schema):
    id = fields.Int(dump_only=True)
    course_id = fields.Int()
    title = fields.Str()
    type = fields.Str(validate=validate.OneOf(['quiz', 'assignment']))
    total_points = fields.Int()
    due_at = fields.DateTime()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class AssessmentCreateSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    type = fields.Str(required=True, validate=validate.OneOf(['quiz', 'assignment']))
    total_points = fields.Int(missing=100, validate=validate.Range(min=1, max=1000))
    due_at = fields.DateTime()


class AssessmentUpdateSchema(Schema):
    title = fields.Str(validate=validate.Length(min=1, max=200))
    type = fields.Str(validate=validate.OneOf(['quiz', 'assignment']))
    total_points = fields.Int(validate=validate.Range(min=1, max=1000))
    due_at = fields.DateTime()

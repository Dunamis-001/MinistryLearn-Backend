from marshmallow import Schema, fields, validate


class SubmissionSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int()
    assessment_id = fields.Int()
    score = fields.Int()
    status = fields.Str(validate=validate.OneOf(['submitted', 'graded', 'returned']))
    feedback = fields.Str()
    submitted_at = fields.DateTime(dump_only=True)
    graded_at = fields.DateTime(dump_only=True)


class SubmissionCreateSchema(Schema):
    assessment_id = fields.Int(required=True)


class SubmissionUpdateSchema(Schema):
    score = fields.Int(validate=validate.Range(min=0, max=1000))
    status = fields.Str(validate=validate.OneOf(['submitted', 'graded', 'returned']))
    feedback = fields.Str(validate=validate.Length(max=2000))
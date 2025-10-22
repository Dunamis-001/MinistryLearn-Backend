from marshmallow import Schema, fields


class SubmissionItemSchema(Schema):
    id = fields.Int(dump_only=True)
    submission_id = fields.Int()
    question_id = fields.Int()
    answer_text = fields.Str()
    selected_option_id = fields.Int()
    points_awarded = fields.Int()


class SubmissionItemCreateSchema(Schema):
    question_id = fields.Int(required=True)
    answer_text = fields.Str()
    selected_option_id = fields.Int()
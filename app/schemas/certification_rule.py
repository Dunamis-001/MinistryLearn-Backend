from marshmallow import Schema, fields, validate


class CertificationRuleSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    description = fields.Str()
    required_course_ids = fields.List(fields.Int())
    min_score = fields.Int()
    expiry_months = fields.Int()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class CertificationRuleCreateSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    description = fields.Str(validate=validate.Length(max=1000))
    required_course_ids = fields.List(fields.Int(), required=True)
    min_score = fields.Int(missing=70, validate=validate.Range(min=0, max=100))
    expiry_months = fields.Int(validate=validate.Range(min=1, max=120))


class CertificationRuleUpdateSchema(Schema):
    name = fields.Str(validate=validate.Length(min=1, max=200))
    description = fields.Str(validate=validate.Length(max=1000))
    required_course_ids = fields.List(fields.Int())
    min_score = fields.Int(validate=validate.Range(min=0, max=100))
    expiry_months = fields.Int(validate=validate.Range(min=1, max=120))
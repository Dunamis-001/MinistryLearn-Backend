from marshmallow import Schema, fields


class CertificationSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int()
    certification_rule_id = fields.Int()
    issued_at = fields.DateTime(dump_only=True)
    expires_at = fields.DateTime()
    certificate_url = fields.Str()
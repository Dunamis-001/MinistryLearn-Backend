from marshmallow import Schema, fields


class MediaAssetSchema(Schema):
    id = fields.Int(dump_only=True)
    owner_user_id = fields.Int()
    public_id = fields.Str()
    url = fields.Str()
    width = fields.Int()
    height = fields.Int()
    bytes = fields.Int()
    format = fields.Str()
    created_at = fields.DateTime(dump_only=True)
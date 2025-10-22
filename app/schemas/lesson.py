from marshmallow import Schema, fields, validate


class LessonSchema(Schema):
    id = fields.Int(dump_only=True)
    module_id = fields.Int()
    title = fields.Str()
    content = fields.Str()
    media_asset_id = fields.Int()
    position = fields.Int()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class LessonCreateSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    content = fields.Str(validate=validate.Length(max=10000))
    media_asset_id = fields.Int()
    position = fields.Int(missing=1)


class LessonUpdateSchema(Schema):
    title = fields.Str(validate=validate.Length(min=1, max=200))
    content = fields.Str(validate=validate.Length(max=10000))
    media_asset_id = fields.Int()
    position = fields.Int()

from marshmallow import Schema, fields, validate


class ModuleSchema(Schema):
    id = fields.Int(dump_only=True)
    course_id = fields.Int()
    title = fields.Str()
    position = fields.Int()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class ModuleCreateSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    position = fields.Int(missing=1)


class ModuleUpdateSchema(Schema):
    title = fields.Str(validate=validate.Length(min=1, max=200))
    position = fields.Int()

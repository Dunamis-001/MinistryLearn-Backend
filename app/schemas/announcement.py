from marshmallow import Schema, fields, validate


class AnnouncementSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    body = fields.Str()
    audience = fields.Str(validate=validate.OneOf(['all', 'course', 'role']))
    course_id = fields.Int()
    role_name = fields.Str()
    created_by = fields.Int()
    created_at = fields.DateTime(dump_only=True)


class AnnouncementCreateSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    body = fields.Str(required=True, validate=validate.Length(min=1, max=5000))
    audience = fields.Str(required=True, validate=validate.OneOf(['all', 'course', 'role']))
    course_id = fields.Int()
    role_name = fields.Str()


class AnnouncementUpdateSchema(Schema):
    title = fields.Str(validate=validate.Length(min=1, max=200))
    body = fields.Str(validate=validate.Length(min=1, max=5000))
    audience = fields.Str(validate=validate.OneOf(['all', 'course', 'role']))
    course_id = fields.Int()
    role_name = fields.Str()
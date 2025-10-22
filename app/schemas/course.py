from marshmallow import Schema, fields, validate


class CourseSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    category = fields.Str()
    difficulty = fields.Str(validate=validate.OneOf(['Beginner', 'Intermediate', 'Advanced']))
    campus = fields.Str()
    thumbnail_url = fields.Str()
    published = fields.Bool()
    created_by = fields.Int()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class CourseCreateSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    description = fields.Str(validate=validate.Length(max=1000))
    category = fields.Str(validate=validate.Length(max=100))
    difficulty = fields.Str(validate=validate.OneOf(['Beginner', 'Intermediate', 'Advanced']))
    campus = fields.Str(validate=validate.Length(max=100))
    thumbnail_url = fields.Str()
    published = fields.Bool(missing=False)


class CourseUpdateSchema(Schema):
    title = fields.Str(validate=validate.Length(min=1, max=200))
    description = fields.Str(validate=validate.Length(max=1000))
    category = fields.Str(validate=validate.Length(max=100))
    difficulty = fields.Str(validate=validate.OneOf(['Beginner', 'Intermediate', 'Advanced']))
    campus = fields.Str(validate=validate.Length(max=100))
    thumbnail_url = fields.Str()
    published = fields.Bool()


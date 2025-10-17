from marshmallow import Schema, fields

class RegisterSchema(Schema):
    email = fields.Email(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True, validate=lambda s: len(s) >= 8)

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
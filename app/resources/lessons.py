from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models.lesson import Lesson
from ..models.module import Module
from ..models.course import Course
from ..models.user import User
from ..schemas.lesson import LessonSchema, LessonCreateSchema, LessonUpdateSchema
from ..utils.rbac import role_required


lesson_schema = LessonSchema()
lesson_create_schema = LessonCreateSchema()
lesson_update_schema = LessonUpdateSchema()


def register(api):
    api.add_resource(LessonListResource, "/modules/<int:module_id>/lessons")
    api.add_resource(LessonResource, "/lessons/<int:lesson_id>")


class LessonListResource(Resource):
    def get(self, module_id):
        """Get lessons for a module"""
        lessons = Lesson.query.filter_by(module_id=module_id).order_by(Lesson.position).all()
        return [lesson.to_dict() for lesson in lessons], 200
   
    @jwt_required()
    @role_required(['Admin', 'Instructor'])
    def post(self, module_id):
        """Create a new lesson"""
        try:
            module = Module.query.get_or_404(module_id)
            course = Course.query.get(module.course_id)
            user_id = get_jwt_identity()
           
            if course.created_by != user_id and not User.query.get(user_id).has_role('Admin'):
                return {"message": "Forbidden"}, 403
           
            data = lesson_create_schema.load(request.get_json() or {})
           
            lesson = Lesson(
                module_id=module_id,
                title=data["title"],
                content=data.get("content"),
                media_asset_id=data.get("media_asset_id"),
                position=data.get("position", 1)
            )
           
            db.session.add(lesson)
            db.session.commit()
           
            return lesson.to_dict(), 201
        except Exception as e:
            return {"message": "Lesson creation failed"}, 400


class LessonResource(Resource):
    def get(self, lesson_id):
        """Get lesson details"""
        lesson = Lesson.query.get_or_404(lesson_id)
        return lesson.to_dict(), 200
   
    @jwt_required()
    @role_required(['Admin', 'Instructor'])
    def put(self, lesson_id):
        """Update lesson"""
        try:
            lesson = Lesson.query.get_or_404(lesson_id)
            module = Module.query.get(lesson.module_id)
            course = Course.query.get(module.course_id)
            user_id = get_jwt_identity()
           
            if course.created_by != user_id and not User.query.get(user_id).has_role('Admin'):
                return {"message": "Forbidden"}, 403
           
            data = lesson_update_schema.load(request.get_json() or {})
           
            for key, value in data.items():
                setattr(lesson, key, value)
           
            db.session.commit()
            return lesson.to_dict(), 200
        except Exception as e:
            return {"message": "Lesson update failed"}, 400
   
    @jwt_required()
    @role_required(['Admin', 'Instructor'])
    def delete(self, lesson_id):
        """Delete lesson"""
        try:
            lesson = Lesson.query.get_or_404(lesson_id)
            module = Module.query.get(lesson.module_id)
            course = Course.query.get(module.course_id)
            user_id = get_jwt_identity()
           
            if course.created_by != user_id and not User.query.get(user_id).has_role('Admin'):
                return {"message": "Forbidden"}, 403
           
            db.session.delete(lesson)
            db.session.commit()
            return {"message": "Lesson deleted"}, 200
        except Exception as e:
            return {"message": "Lesson deletion failed"}, 400
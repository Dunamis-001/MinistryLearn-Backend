from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models.course import Course
from ..models.user import User
from ..schemas.course import CourseSchema, CourseCreateSchema, CourseUpdateSchema
from ..utils.pagination import paginate
from ..utils.rbac import role_required


course_schema = CourseSchema()
course_create_schema = CourseCreateSchema()
course_update_schema = CourseUpdateSchema()


def register(api):
    api.add_resource(CourseListResource, "/courses")
    api.add_resource(CourseResource, "/courses/<int:course_id>")


class CourseListResource(Resource):
    def get(self):
        """Get paginated list of published courses"""
        query = Course.query.filter_by(published=True)
       
        # Apply filters
        campus = request.args.get('campus')
        category = request.args.get('category')
        difficulty = request.args.get('difficulty')
        search = request.args.get('search')
       
        if campus:
            query = query.filter(Course.campus == campus)
        if category:
            query = query.filter(Course.category == category)
        if difficulty:
            query = query.filter(Course.difficulty == difficulty)
        if search:
            query = query.filter(Course.title.ilike(f'%{search}%'))
       
        return paginate(query.order_by(Course.created_at.desc()))
   
    @jwt_required()
    @role_required(['Admin', 'Instructor'])
    def post(self):
        """Create a new course"""
        try:
            data = course_create_schema.load(request.get_json() or {})
            user_id = get_jwt_identity()
           
            course = Course(
                title=data["title"],
                description=data.get("description"),
                category=data.get("category"),
                difficulty=data.get("difficulty"),
                campus=data.get("campus"),
                thumbnail_url=data.get("thumbnail_url"),
                published=data.get("published", False),
                created_by=user_id
            )
           
            db.session.add(course)
            db.session.commit()
           
            return course.to_dict(), 201
        except Exception as e:
            return {"message": "Course creation failed"}, 400


class CourseResource(Resource):
    def get(self, course_id):
        """Get course details"""
        course = Course.query.get_or_404(course_id)
        return course.to_dict(), 200
   
    @jwt_required()
    @role_required(['Admin', 'Instructor'])
    def put(self, course_id):
        """Update course"""
        try:
            course = Course.query.get_or_404(course_id)
            user_id = get_jwt_identity()
           
            # Check if user can edit this course
            if course.created_by != user_id and not User.query.get(user_id).has_role('Admin'):
                return {"message": "Forbidden"}, 403
           
            data = course_update_schema.load(request.get_json() or {})
           
            for key, value in data.items():
                setattr(course, key, value)
           
            db.session.commit()
            return course.to_dict(), 200
        except Exception as e:
            return {"message": "Course update failed"}, 400
   
    @jwt_required()
    @role_required(['Admin', 'Instructor'])
    def delete(self, course_id):
        """Delete course"""
        try:
            course = Course.query.get_or_404(course_id)
            user_id = get_jwt_identity()
           
            # Check if user can delete this course
            if course.created_by != user_id and not User.query.get(user_id).has_role('Admin'):
                return {"message": "Forbidden"}, 403
           
            db.session.delete(course)
            db.session.commit()
            return {"message": "Course deleted"}, 200
        except Exception as e:
            return {"message": "Course deletion failed"}, 400
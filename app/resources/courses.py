from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
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
    api.add_resource(CourseApprovalResource, "/courses/<int:course_id>/approve")
    api.add_resource(InstructorCoursesResource, "/instructor/courses")
    api.add_resource(PendingCoursesResource, "/admin/courses/pending")


class CourseListResource(Resource):
    def get(self):
        """Get paginated list of published and approved courses"""
        query = Course.query.filter_by(published=True, approved=True)
       
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
        """Create a new course - requires admin approval"""
        try:
            data = course_create_schema.load(request.get_json() or {})
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
           
            # Only admins can create approved courses, instructors need approval
            is_admin = user.has_role('Admin')
           
            course = Course(
                title=data["title"],
                description=data.get("description"),
                category=data.get("category"),
                difficulty=data.get("difficulty"),
                campus=data.get("campus"),
                thumbnail_url=data.get("thumbnail_url"),
                published=False,  # Must be approved first
                approved=is_admin,  # Auto-approve if admin creates
                approved_by=user_id if is_admin else None,
                approved_at=datetime.utcnow() if is_admin else None,
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
        """Update course - Instructor edits require approval, Admin edits auto-approve"""
        try:
            course = Course.query.get_or_404(course_id)
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            is_admin = user.has_role('Admin')
           
            # Check if user can edit this course
            if course.created_by != user_id and not is_admin:
                return {"message": "Forbidden"}, 403
           
            data = course_update_schema.load(request.get_json() or {})
           
            # Handle approval workflow
            # If Instructor edits: require admin approval (set approved=False, unpublish if was published)
            # If Admin edits: auto-approve (set approved=True)
            if not is_admin:
                # Instructor editing - requires approval
                # Prevent instructor from publishing unapproved courses
                if 'published' in data and data['published']:
                    return {"message": "Course must be approved by admin before publishing"}, 400
                
                # If course was published, unpublish it until admin approves changes
                if course.published:
                    data['published'] = False  # Override to unpublish
                course.approved = False
                course.approved_by = None
                course.approved_at = None
            else:
                # Admin editing - auto-approve
                course.approved = True
                course.approved_by = user_id
                course.approved_at = datetime.utcnow()
           
            # Apply updates
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


class CourseApprovalResource(Resource):
    @jwt_required()
    @role_required(['Admin'])
    def post(self, course_id):
        """Approve a course (Admin only)"""
        try:
            course = Course.query.get_or_404(course_id)
            user_id = get_jwt_identity()
            
            course.approved = True
            course.approved_by = user_id
            course.approved_at = datetime.utcnow()
            
            db.session.commit()
            return course.to_dict(), 200
        except Exception as e:
            return {"message": "Course approval failed"}, 400
    
    @jwt_required()
    @role_required(['Admin'])
    def delete(self, course_id):
        """Reject a course (Admin only)"""
        try:
            course = Course.query.get_or_404(course_id)
            
            course.approved = False
            course.approved_by = None
            course.approved_at = None
            
            db.session.commit()
            return {"message": "Course rejected"}, 200
        except Exception as e:
            return {"message": "Course rejection failed"}, 400


class InstructorCoursesResource(Resource):
    @jwt_required()
    @role_required(['Instructor'])
    def get(self):
        """Get all courses created by the current instructor"""
        user_id = get_jwt_identity()
        query = Course.query.filter_by(created_by=user_id)
        
        return paginate(query.order_by(Course.created_at.desc()))


class PendingCoursesResource(Resource):
    @jwt_required()
    @role_required(['Admin'])
    def get(self):
        """Get all pending courses awaiting approval"""
        query = Course.query.filter_by(approved=False)
        
        return paginate(query.order_by(Course.created_at.desc()))
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models.enrollment import Enrollment
from ..models.course import Course
from ..schemas.enrollment import EnrollmentSchema, EnrollmentCreateSchema
from ..utils.pagination import paginate
from ..services.email_service import EmailService


enrollment_schema = EnrollmentSchema()
enrollment_create_schema = EnrollmentCreateSchema()


def register(api):
    api.add_resource(EnrollmentListResource, "/enrollments")
    api.add_resource(EnrollmentResource, "/enrollments/<int:enrollment_id>")
    api.add_resource(CourseEnrollmentResource, "/courses/<int:course_id>/enroll")


class EnrollmentListResource(Resource):
    @jwt_required()
    def get(self):
        """Get user's enrollments"""
        user_id = get_jwt_identity()
        query = Enrollment.query.filter_by(user_id=user_id)
        return paginate(query.order_by(Enrollment.created_at.desc()))


class EnrollmentResource(Resource):
    @jwt_required()
    def get(self, enrollment_id):
        """Get enrollment details"""
        user_id = get_jwt_identity()
        enrollment = Enrollment.query.filter_by(
            id=enrollment_id,
            user_id=user_id
        ).first_or_404()
        return enrollment.to_dict(), 200
   
    @jwt_required()
    def delete(self, enrollment_id):
        """Unenroll from course"""
        user_id = get_jwt_identity()
        enrollment = Enrollment.query.filter_by(
            id=enrollment_id,
            user_id=user_id
        ).first_or_404()
       
        db.session.delete(enrollment)
        db.session.commit()
        return {"message": "Unenrolled successfully"}, 200


class CourseEnrollmentResource(Resource):
    @jwt_required()
    def post(self, course_id):
        """Enroll in a course"""
        try:
            user_id = get_jwt_identity()
           
            # Check if course exists and is published
            course = Course.query.filter_by(id=course_id, published=True).first_or_404()
           
            # Check if already enrolled
            existing = Enrollment.query.filter_by(
                user_id=user_id,
                course_id=course_id
            ).first()
           
            if existing:
                return {"message": "Already enrolled in this course"}, 409
           
            # Create enrollment
            enrollment = Enrollment(
                user_id=user_id,
                course_id=course_id,
                status='active',
                progress=0
            )
           
            db.session.add(enrollment)
            db.session.commit()
           
            # Send enrollment confirmation email
            email_service = EmailService()
            email_service.send_enrollment_confirmation(
                enrollment.user.email,
                course.title
            )
           
            return enrollment.to_dict(), 201
        except Exception as e:
            return {"message": "Enrollment failed"}, 400
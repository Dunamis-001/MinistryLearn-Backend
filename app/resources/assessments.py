from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models.assessment import Assessment
from ..models.course import Course
from ..models.user import User
from ..schemas.assessment import AssessmentSchema, AssessmentCreateSchema, AssessmentUpdateSchema
from ..utils.rbac import role_required


assessment_schema = AssessmentSchema()
assessment_create_schema = AssessmentCreateSchema()
assessment_update_schema = AssessmentUpdateSchema()


def register(api):
    api.add_resource(AssessmentListResource, "/courses/<int:course_id>/assessments")
    api.add_resource(AssessmentResource, "/assessments/<int:assessment_id>")


class AssessmentListResource(Resource):
    def get(self, course_id):
        """Get assessments for a course"""
        assessments = Assessment.query.filter_by(course_id=course_id).all()
        return [assessment.to_dict() for assessment in assessments], 200
   
    @jwt_required()
    @role_required(['Admin', 'Instructor'])
    def post(self, course_id):
        """Create a new assessment"""
        try:
            course = Course.query.get_or_404(course_id)
            user_id = get_jwt_identity()
           
            if course.created_by != user_id and not User.query.get(user_id).has_role('Admin'):
                return {"message": "Forbidden"}, 403
           
            data = assessment_create_schema.load(request.get_json() or {})
           
            assessment = Assessment(
                course_id=course_id,
                title=data["title"],
                type=data["type"],
                total_points=data.get("total_points", 100),
                due_at=data.get("due_at")
            )
           
            db.session.add(assessment)
            db.session.commit()
           
            return assessment.to_dict(), 201
        except Exception as e:
            return {"message": "Assessment creation failed"}, 400


class AssessmentResource(Resource):
    def get(self, assessment_id):
        """Get assessment details"""
        assessment = Assessment.query.get_or_404(assessment_id)
        return assessment.to_dict(), 200
   
    @jwt_required()
    @role_required(['Admin', 'Instructor'])
    def put(self, assessment_id):
        """Update assessment"""
        try:
            assessment = Assessment.query.get_or_404(assessment_id)
            course = Course.query.get(assessment.course_id)
            user_id = get_jwt_identity()
           
            if course.created_by != user_id and not User.query.get(user_id).has_role('Admin'):
                return {"message": "Forbidden"}, 403
           
            data = assessment_update_schema.load(request.get_json() or {})
           
            for key, value in data.items():
                setattr(assessment, key, value)
           
            db.session.commit()
            return assessment.to_dict(), 200
        except Exception as e:
            return {"message": "Assessment update failed"}, 400
   
    @jwt_required()
    @role_required(['Admin', 'Instructor'])
    def delete(self, assessment_id):
        """Delete assessment"""
        try:
            assessment = Assessment.query.get_or_404(assessment_id)
            course = Course.query.get(assessment.course_id)
            user_id = get_jwt_identity()
           
            if course.created_by != user_id and not User.query.get(user_id).has_role('Admin'):
                return {"message": "Forbidden"}, 403
           
            db.session.delete(assessment)
            db.session.commit()
            return {"message": "Assessment deleted"}, 200
        except Exception as e:
            return {"message": "Assessment deletion failed"}, 400
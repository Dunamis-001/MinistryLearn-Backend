from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models.submission import Submission
from ..models.assessment import Assessment
from ..schemas.submission import SubmissionSchema, SubmissionCreateSchema, SubmissionUpdateSchema
from ..utils.pagination import paginate
from ..utils.rbac import role_required


submission_schema = SubmissionSchema()
submission_create_schema = SubmissionCreateSchema()
submission_update_schema = SubmissionUpdateSchema()


def register(api):
    api.add_resource(SubmissionListResource, "/submissions")
    api.add_resource(SubmissionResource, "/submissions/<int:submission_id>")
    api.add_resource(AssessmentSubmissionResource, "/assessments/<int:assessment_id>/submit")


class SubmissionListResource(Resource):
    @jwt_required()
    def get(self):
        """Get user's submissions or all submissions (for instructors/admins)"""
        user_id = get_jwt_identity()
        query = Submission.query.filter_by(user_id=user_id)
        return paginate(query.order_by(Submission.submitted_at.desc()))


class SubmissionResource(Resource):
    @jwt_required()
    def get(self, submission_id):
        """Get submission details"""
        user_id = get_jwt_identity()
        submission = Submission.query.filter_by(
            id=submission_id,
            user_id=user_id
        ).first_or_404()
        return submission.to_dict(), 200
   
    @jwt_required()
    @role_required(['Admin', 'Instructor'])
    def put(self, submission_id):
        """Grade submission"""
        try:
            submission = Submission.query.get_or_404(submission_id)
            data = submission_update_schema.load(request.get_json() or {})
           
            submission.score = data.get("score")
            submission.status = data.get("status", "graded")
            submission.feedback = data.get("feedback")
           
            db.session.commit()
            return submission.to_dict(), 200
        except Exception as e:
            return {"message": "Submission update failed"}, 400


class AssessmentSubmissionResource(Resource):
    @jwt_required()
    def post(self, assessment_id):
        """Submit assessment"""
        try:
            user_id = get_jwt_identity()
           
            # Check if already submitted
            existing = Submission.query.filter_by(
                user_id=user_id,
                assessment_id=assessment_id
            ).first()
           
            if existing:
                return {"message": "Already submitted"}, 409
           
            # Create submission
            submission = Submission(
                user_id=user_id,
                assessment_id=assessment_id,
                status='submitted'
            )
           
            db.session.add(submission)
            db.session.commit()
           
            return submission.to_dict(), 201
        except Exception as e:
            return {"message": "Submission failed"}, 400
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models.certification import Certification
from ..models.certification_rule import CertificationRule
from ..schemas.certification import CertificationSchema
from ..schemas.certification_rule import CertificationRuleSchema, CertificationRuleCreateSchema, CertificationRuleUpdateSchema
from ..utils.rbac import role_required


certification_schema = CertificationSchema()
certification_rule_schema = CertificationRuleSchema()
certification_rule_create_schema = CertificationRuleCreateSchema()
certification_rule_update_schema = CertificationRuleUpdateSchema()


def register(api):
    api.add_resource(UserCertificationsResource, "/certifications")
    api.add_resource(CertificationRuleListResource, "/certification-rules")
    api.add_resource(CertificationRuleResource, "/certification-rules/<int:rule_id>")


class UserCertificationsResource(Resource):
    @jwt_required()
    def get(self):
        """Get user's certifications"""
        user_id = get_jwt_identity()
        certifications = Certification.query.filter_by(user_id=user_id).all()
        return [cert.to_dict() for cert in certifications], 200


class CertificationRuleListResource(Resource):
    def get(self):
        """Get all certification rules"""
        rules = CertificationRule.query.all()
        return [rule.to_dict() for rule in rules], 200
   
    @jwt_required()
    @role_required(['Admin'])
    def post(self):
        """Create certification rule"""
        try:
            data = certification_rule_create_schema.load(request.get_json() or {})
           
            rule = CertificationRule(
                name=data["name"],
                description=data.get("description"),
                required_course_ids=data["required_course_ids"],
                min_score=data.get("min_score", 70),
                expiry_months=data.get("expiry_months")
            )
           
            db.session.add(rule)
            db.session.commit()
           
            return rule.to_dict(), 201
        except Exception as e:
            return {"message": "Certification rule creation failed"}, 400


class CertificationRuleResource(Resource):
    def get(self, rule_id):
        """Get certification rule details"""
        rule = CertificationRule.query.get_or_404(rule_id)
        return rule.to_dict(), 200
   
    @jwt_required()
    @role_required(['Admin'])
    def put(self, rule_id):
        """Update certification rule"""
        try:
            rule = CertificationRule.query.get_or_404(rule_id)
            data = certification_rule_update_schema.load(request.get_json() or {})
           
            for key, value in data.items():
                setattr(rule, key, value)
           
            db.session.commit()
            return rule.to_dict(), 200
        except Exception as e:
            return {"message": "Certification rule update failed"}, 400
   
    @jwt_required()
    @role_required(['Admin'])
    def delete(self, rule_id):
        """Delete certification rule"""
        try:
            rule = CertificationRule.query.get_or_404(rule_id)
            db.session.delete(rule)
            db.session.commit()
            return {"message": "Certification rule deleted"}, 200
        except Exception as e:
            return {"message": "Certification rule deletion failed"}, 400
from datetime import datetime, timedelta
from ..extensions import db
from ..models.certification import Certification
from ..models.certification_rule import CertificationRule
from ..models.enrollment import Enrollment
from ..models.submission import Submission
from .email_service import EmailService

class CertificationService:
    def __init__(self):
        self.email_service = EmailService()
    
    def check_and_award_certifications(self, user_id):
        """Check if user qualifies for any certifications and award them"""
        user_certifications = []
        
        # Get all certification rules
        rules = CertificationRule.query.all()
        
        for rule in rules:
            # Check if user already has this certification
            existing = Certification.query.filter_by(
                user_id=user_id,
                certification_rule_id=rule.id
            ).first()
            
            if existing:
                continue
            
            # Check if user meets requirements
            if self._meets_certification_requirements(user_id, rule):
                # Award certification
                certification = self._award_certification(user_id, rule)
                user_certifications.append(certification)
                
                # Send email notification
                self.email_service.send_certification_awarded(
                    certification.user.email,
                    rule.name
                )
        
        return user_certifications
    
    def _meets_certification_requirements(self, user_id, rule):
        """Check if user meets certification requirements"""
        # Check if user has completed all required courses
        for course_id in rule.required_course_ids:
            enrollment = Enrollment.query.filter_by(
                user_id=user_id,
                course_id=course_id,
                status='completed'
            ).first()
            
            if not enrollment:
                return False
            
            # Check if user meets minimum score requirement
            if rule.min_score:
                # Get all assessments for this course
                from ..models.assessment import Assessment
                assessments = Assessment.query.filter_by(course_id=course_id).all()
                
                for assessment in assessments:
                    submission = Submission.query.filter_by(
                        user_id=user_id,
                        assessment_id=assessment.id,
                        status='graded'
                    ).first()
                    
                    if not submission or submission.score < rule.min_score:
                        return False
        
        return True
    
    def _award_certification(self, user_id, rule):
        """Award certification to user"""
        # Calculate expiry date if specified
        expires_at = None
        if rule.expiry_months:
            expires_at = datetime.utcnow() + timedelta(days=rule.expiry_months * 30)
        
        # Create certification
        certification = Certification(
            user_id=user_id,
            certification_rule_id=rule.id,
            expires_at=expires_at,
            certificate_url=None  # Will be generated later
        )
        
        db.session.add(certification)
        db.session.commit()
        
        return certification
    
    def get_user_certifications(self, user_id):
        """Get all certifications for a user"""
        certifications = Certification.query.filter_by(user_id=user_id).all()
        return [cert.to_dict() for cert in certifications]
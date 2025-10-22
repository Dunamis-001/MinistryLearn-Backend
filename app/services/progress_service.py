from ..extensions import db
from ..models.enrollment import Enrollment
from ..models.course import Course
from ..models.module import Module
from ..models.lesson import Lesson
from .certification_service import CertificationService

class ProgressService:
    def __init__(self):
        self.certification_service = CertificationService()
    
    def update_course_progress(self, user_id, course_id):
        """Update course progress based on completed lessons"""
        enrollment = Enrollment.query.filter_by(
            user_id=user_id,
            course_id=course_id
        ).first()
        
        if not enrollment:
            return 0
        
        # Get total lessons in course
        total_lessons = db.session.query(Lesson).join(Module).filter(
            Module.course_id == course_id
        ).count()
        
        if total_lessons == 0:
            return 0
        
        # For now, we'll use a simple progress calculation
        # In a real app, you'd track which lessons are completed
        # This is a placeholder - you'd need to implement lesson completion tracking
        
        # Calculate progress percentage
        progress = min(100, (total_lessons * 10))  # Placeholder calculation
        
        enrollment.progress = progress
        
        # Check if course is completed
        if progress >= 100:
            enrollment.status = 'completed'
            # Check for certifications
            self.certification_service.check_and_award_certifications(user_id)
        
        db.session.commit()
        return progress
    
    def get_course_progress(self, user_id, course_id):
        """Get progress for a specific course"""
        enrollment = Enrollment.query.filter_by(
            user_id=user_id,
            course_id=course_id
        ).first()
        
        if not enrollment:
            return None
        
        return {
            'progress': enrollment.progress,
            'status': enrollment.status,
            'course_id': course_id
        }
    
    def get_user_progress_summary(self, user_id):
        """Get progress summary for all user's courses"""
        enrollments = Enrollment.query.filter_by(user_id=user_id).all()
        
        summary = {
            'total_courses': len(enrollments),
            'completed_courses': len([e for e in enrollments if e.status == 'completed']),
            'active_courses': len([e for e in enrollments if e.status == 'active']),
            'average_progress': sum(e.progress for e in enrollments) / len(enrollments) if enrollments else 0
        }
        
        return summary
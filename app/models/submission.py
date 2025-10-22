from datetime import datetime
from ..extensions import db


class Submission(db.Model):
    __tablename__ = "submissions"


    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    assessment_id = db.Column(db.Integer, db.ForeignKey("assessments.id"), nullable=False)
    score = db.Column(db.Integer)
    status = db.Column(db.String, nullable=False, default='submitted')  # 'submitted', 'graded', 'returned'
    feedback = db.Column(db.Text)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    graded_at = db.Column(db.DateTime)


    # Relationships
    user = db.relationship("User", back_populates="submissions")
    assessment = db.relationship("Assessment", back_populates="submissions")
    submission_items = db.relationship("SubmissionItem", back_populates="submission", cascade="all, delete-orphan")


    # Unique constraint
    __table_args__ = (db.UniqueConstraint('user_id', 'assessment_id', name='unique_user_assessment'),)


    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'assessment_id': self.assessment_id,
            'score': self.score,
            'status': self.status,
            'feedback': self.feedback,
            'submitted_at': self.submitted_at.isoformat(),
            'graded_at': self.graded_at.isoformat() if self.graded_at else None
        }

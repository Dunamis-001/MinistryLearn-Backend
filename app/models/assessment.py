from datetime import datetime
from ..extensions import db


class Assessment(db.Model):
    __tablename__ = "assessments"


    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    title = db.Column(db.String, nullable=False)
    type = db.Column(db.String)  # 'quiz', 'assignment'
    total_points = db.Column(db.Integer, nullable=False, default=100)
    due_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    # Relationships
    course = db.relationship("Course", back_populates="assessments")
    questions = db.relationship("Question", back_populates="assessment", cascade="all, delete-orphan")
    submissions = db.relationship("Submission", back_populates="assessment", cascade="all, delete-orphan")


    def to_dict(self):
        return {
            'id': self.id,
            'course_id': self.course_id,
            'title': self.title,
            'type': self.type,
            'total_points': self.total_points,
            'due_at': self.due_at.isoformat() if self.due_at else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

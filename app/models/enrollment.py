from datetime import datetime
from ..extensions import db


class Enrollment(db.Model):
    __tablename__ = "enrollments"


    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    status = db.Column(db.String, nullable=False, default='active')  # 'active', 'completed', 'dropped'
    progress = db.Column(db.Integer, nullable=False, default=0)  # 0-100
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    # Relationships
    user = db.relationship("User", back_populates="enrollments")
    course = db.relationship("Course", back_populates="enrollments")


    # Unique constraint
    __table_args__ = (db.UniqueConstraint('user_id', 'course_id', name='unique_user_course'),)


    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'course_id': self.course_id,
            'status': self.status,
            'progress': self.progress,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

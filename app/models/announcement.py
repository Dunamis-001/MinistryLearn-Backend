from datetime import datetime
from ..extensions import db


class Announcement(db.Model):
    __tablename__ = "announcements"


    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.Text, nullable=False)
    audience = db.Column(db.String)  # 'all', 'course', 'role'
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))
    role_name = db.Column(db.String)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    # Relationships
    course = db.relationship("Course", back_populates="announcements")
    creator = db.relationship("User", back_populates="created_announcements", foreign_keys=[created_by])


    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'audience': self.audience,
            'course_id': self.course_id,
            'role_name': self.role_name,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat()
        }

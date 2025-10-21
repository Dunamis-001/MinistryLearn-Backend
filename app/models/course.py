from datetime import datetime
from ..extensions import db


class Course(db.Model):
    __tablename__ = "courses"


    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String)
    difficulty = db.Column(db.String)  # 'Beginner', 'Intermediate', 'Advanced'
    campus = db.Column(db.String)
    thumbnail_url = db.Column(db.Text)
    published = db.Column(db.Boolean, nullable=False, default=False)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    # Relationships
    creator = db.relationship("User", back_populates="created_courses", foreign_keys=[created_by])
    modules = db.relationship("Module", back_populates="course", cascade="all, delete-orphan")
    assessments = db.relationship("Assessment", back_populates="course", cascade="all, delete-orphan")
    enrollments = db.relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")
    announcements = db.relationship("Announcement", back_populates="course", cascade="all, delete-orphan")


    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'difficulty': self.difficulty,
            'campus': self.campus,
            'thumbnail_url': self.thumbnail_url,
            'published': self.published,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


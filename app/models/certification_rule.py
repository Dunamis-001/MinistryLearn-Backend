from datetime import datetime
from ..extensions import db


class CertificationRule(db.Model):
    __tablename__ = "certification_rules"


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.Text)
    required_course_ids = db.Column(db.ARRAY(db.Integer))  # array of course ids
    min_score = db.Column(db.Integer, default=70)
    expiry_months = db.Column(db.Integer)  # optional
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    # Relationships
    certifications = db.relationship("Certification", back_populates="certification_rule", cascade="all, delete-orphan")


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'required_course_ids': self.required_course_ids,
            'min_score': self.min_score,
            'expiry_months': self.expiry_months,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

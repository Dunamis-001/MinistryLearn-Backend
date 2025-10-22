from datetime import datetime
from ..extensions import db


class Certification(db.Model):
    __tablename__ = "certifications"


    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    certification_rule_id = db.Column(db.Integer, db.ForeignKey("certification_rules.id"), nullable=False)
    issued_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    certificate_url = db.Column(db.Text)  # cloudinary url


    # Relationships
    user = db.relationship("User", back_populates="certifications")
    certification_rule = db.relationship("CertificationRule", back_populates="certifications")


    # Unique constraint
    __table_args__ = (db.UniqueConstraint('user_id', 'certification_rule_id', name='unique_user_certification_rule'),)


    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'certification_rule_id': self.certification_rule_id,
            'issued_at': self.issued_at.isoformat(),
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'certificate_url': self.certificate_url
        }

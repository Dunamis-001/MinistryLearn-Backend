from ..extensions import db


class Question(db.Model):
    __tablename__ = "questions"


    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey("assessments.id"), nullable=False)
    prompt = db.Column(db.Text, nullable=False)
    type = db.Column(db.String)  # 'mcq', 'short_answer'
    points = db.Column(db.Integer, nullable=False, default=1)
    position = db.Column(db.Integer, nullable=False, default=1)


    # Relationships
    assessment = db.relationship("Assessment", back_populates="questions")
    options = db.relationship("Option", back_populates="question", cascade="all, delete-orphan")
    submission_items = db.relationship("SubmissionItem", back_populates="question", cascade="all, delete-orphan")


    def to_dict(self):
        return {
            'id': self.id,
            'assessment_id': self.assessment_id,
            'prompt': self.prompt,
            'type': self.type,
            'points': self.points,
            'position': self.position
        }

from ..extensions import db


class Option(db.Model):
    __tablename__ = "options"


    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)
    text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False, default=False)


    # Relationships
    question = db.relationship("Question", back_populates="options")
    submission_items = db.relationship("SubmissionItem", back_populates="selected_option")


    def to_dict(self):
        return {
            'id': self.id,
            'question_id': self.question_id,
            'text': self.text,
            'is_correct': self.is_correct
        }

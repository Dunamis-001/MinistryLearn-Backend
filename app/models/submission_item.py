from ..extensions import db


class SubmissionItem(db.Model):
    __tablename__ = "submission_items"


    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey("submissions.id"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)
    answer_text = db.Column(db.Text)
    selected_option_id = db.Column(db.Integer, db.ForeignKey("options.id"))
    points_awarded = db.Column(db.Integer)


    # Relationships
    submission = db.relationship("Submission", back_populates="submission_items")
    question = db.relationship("Question", back_populates="submission_items")
    selected_option = db.relationship("Option", back_populates="submission_items")


    def to_dict(self):
        return {
            'id': self.id,
            'submission_id': self.submission_id,
            'question_id': self.question_id,
            'answer_text': self.answer_text,
            'selected_option_id': self.selected_option_id,
            'points_awarded': self.points_awarded
        }
        
from datetime import datetime
from ..extensions import db
import json


class Lesson(db.Model):
    __tablename__ = "lessons"


    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey("modules.id"), nullable=False)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text)  # rich text/HTML/MD
    media_asset_id = db.Column(db.Integer, db.ForeignKey("media_assets.id"))  # Video or image
    video_url = db.Column(db.Text)  # Direct video URL (YouTube, Vimeo, etc.)
    assessment_id = db.Column(db.Integer, db.ForeignKey("assessments.id"))  # Linked quiz/assessment
    study_materials = db.Column(db.Text)  # JSON array of study material objects
    position = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    # Relationships
    module = db.relationship("Module", back_populates="lessons")
    media_asset = db.relationship("MediaAsset", back_populates="lesson")
    assessment = db.relationship("Assessment", foreign_keys=[assessment_id])


    def to_dict(self):
        study_materials_list = []
        if self.study_materials:
            try:
                study_materials_list = json.loads(self.study_materials)
            except:
                study_materials_list = []
        
        return {
            'id': self.id,
            'module_id': self.module_id,
            'title': self.title,
            'content': self.content,
            'media_asset_id': self.media_asset_id,
            'video_url': self.video_url,
            'assessment_id': self.assessment_id,
            'study_materials': study_materials_list,
            'position': self.position,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

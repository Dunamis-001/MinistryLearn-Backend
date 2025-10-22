from datetime import datetime
from ..extensions import db


class Lesson(db.Model):
    __tablename__ = "lessons"


    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey("modules.id"), nullable=False)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text)  # rich text/HTML/MD
    media_asset_id = db.Column(db.Integer, db.ForeignKey("media_assets.id"))
    position = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    # Relationships
    module = db.relationship("Module", back_populates="lessons")
    media_asset = db.relationship("MediaAsset", back_populates="lesson")


    def to_dict(self):
        return {
            'id': self.id,
            'module_id': self.module_id,
            'title': self.title,
            'content': self.content,
            'media_asset_id': self.media_asset_id,
            'position': self.position,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

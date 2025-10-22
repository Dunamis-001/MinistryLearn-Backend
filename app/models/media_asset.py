from datetime import datetime
from ..extensions import db


class MediaAsset(db.Model):
    __tablename__ = "media_assets"


    id = db.Column(db.Integer, primary_key=True)
    owner_user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    public_id = db.Column(db.String)  # cloudinary public id
    url = db.Column(db.Text)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    bytes = db.Column(db.Integer)
    format = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    # Relationships
    owner = db.relationship("User", back_populates="media_assets")
    lesson = db.relationship("Lesson", back_populates="media_asset")


    def to_dict(self):
        return {
            'id': self.id,
            'owner_user_id': self.owner_user_id,
            'public_id': self.public_id,
            'url': self.url,
            'width': self.width,
            'height': self.height,
            'bytes': self.bytes,
            'format': self.format,
            'created_at': self.created_at.isoformat()
        }

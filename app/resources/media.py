from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models.media_asset import MediaAsset
from ..schemas.media_asset import MediaAssetSchema
from ..services.cloudinary_service import CloudinaryService


media_asset_schema = MediaAssetSchema()


def register(api):
    api.add_resource(MediaUploadResource, "/media/upload")


class MediaUploadResource(Resource):
    @jwt_required()
    def post(self):
        """Upload media file to Cloudinary"""
        try:
            if 'file' not in request.files:
                return {"message": "No file provided"}, 400
           
            file = request.files['file']
            if file.filename == '':
                return {"message": "No file selected"}, 400
           
            user_id = get_jwt_identity()
            cloudinary_service = CloudinaryService()
           
            # Upload to Cloudinary
            result = cloudinary_service.upload_image(file)
           
            # Save to database
            media_asset = MediaAsset(
                owner_user_id=user_id,
                public_id=result["public_id"],
                url=result["url"],
                width=result["width"],
                height=result["height"],
                bytes=result["bytes"],
                format=result["format"]
            )
           
            db.session.add(media_asset)
            db.session.commit()
           
            return media_asset.to_dict(), 201
        except Exception as e:
            return {"message": f"Upload failed: {str(e)}"}, 400
import cloudinary
import cloudinary.uploader
import cloudinary.api
from ..config import Config

class CloudinaryService:
    def __init__(self):
        if Config.CLOUDINARY_URL:
            cloudinary.config(cloudinary_url=Config.CLOUDINARY_URL)
    
    def upload_image(self, file, folder="ministrylearn", transformation=None):
        """Upload image to Cloudinary with optional transformations"""
        try:
            options = {
                "folder": folder,
                "resource_type": "image"
            }
            
            if transformation:
                options["transformation"] = transformation
            
            result = cloudinary.uploader.upload(file, **options)
            
            return {
                "public_id": result["public_id"],
                "url": result["secure_url"],
                "width": result["width"],
                "height": result["height"],
                "bytes": result["bytes"],
                "format": result["format"]
            }
        except Exception as e:
            raise Exception(f"Cloudinary upload failed: {str(e)}")
    
    def upload_video(self, file, folder="ministrylearn"):
        """Upload video to Cloudinary"""
        try:
            result = cloudinary.uploader.upload(
                file,
                folder=folder,
                resource_type="video"
            )
            
            return {
                "public_id": result["public_id"],
                "url": result["secure_url"],
                "bytes": result["bytes"],
                "format": result["format"]
            }
        except Exception as e:
            raise Exception(f"Cloudinary video upload failed: {str(e)}")
    
    def delete_asset(self, public_id):
        """Delete asset from Cloudinary"""
        try:
            result = cloudinary.uploader.destroy(public_id)
            return result
        except Exception as e:
            raise Exception(f"Cloudinary delete failed: {str(e)}")
    
    def get_thumbnail_url(self, public_id, width=300, height=200):
        """Generate thumbnail URL for video"""
        try:
            url = cloudinary.CloudinaryImage(public_id).build_url(
                transformation=[
                    {"width": width, "height": height, "crop": "fill"},
                    {"quality": "auto", "format": "jpg"}
                ]
            )
            return url
        except Exception as e:
            raise Exception(f"Thumbnail generation failed: {str(e)}")
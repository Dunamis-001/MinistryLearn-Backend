from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models.announcement import Announcement
from ..schemas.announcement import AnnouncementSchema, AnnouncementCreateSchema, AnnouncementUpdateSchema
from ..utils.pagination import paginate
from ..utils.rbac import role_required


announcement_schema = AnnouncementSchema()
announcement_create_schema = AnnouncementCreateSchema()
announcement_update_schema = AnnouncementUpdateSchema()


def register(api):
    api.add_resource(AnnouncementListResource, "/announcements")
    api.add_resource(AnnouncementResource, "/announcements/<int:announcement_id>")


class AnnouncementListResource(Resource):
    def get(self):
        """Get announcements"""
        query = Announcement.query.order_by(Announcement.created_at.desc())
        return paginate(query)
   
    @jwt_required()
    @role_required(['Admin', 'Instructor'])
    def post(self):
        """Create announcement"""
        try:
            data = announcement_create_schema.load(request.get_json() or {})
            user_id = get_jwt_identity()
           
            announcement = Announcement(
                title=data["title"],
                body=data["body"],
                audience=data["audience"],
                course_id=data.get("course_id"),
                role_name=data.get("role_name"),
                created_by=user_id
            )
           
            db.session.add(announcement)
            db.session.commit()
           
            return announcement.to_dict(), 201
        except Exception as e:
            return {"message": "Announcement creation failed"}, 400


class AnnouncementResource(Resource):
    def get(self, announcement_id):
        """Get announcement details"""
        announcement = Announcement.query.get_or_404(announcement_id)
        return announcement.to_dict(), 200
   
    @jwt_required()
    @role_required(['Admin', 'Instructor'])
    def put(self, announcement_id):
        """Update announcement"""
        try:
            announcement = Announcement.query.get_or_404(announcement_id)
            user_id = get_jwt_identity()
           
            if announcement.created_by != user_id and not User.query.get(user_id).has_role('Admin'):
                return {"message": "Forbidden"}, 403
           
            data = announcement_update_schema.load(request.get_json() or {})
           
            for key, value in data.items():
                setattr(announcement, key, value)
           
            db.session.commit()
            return announcement.to_dict(), 200
        except Exception as e:
            return {"message": "Announcement update failed"}, 400
   
    @jwt_required()
    @role_required(['Admin', 'Instructor'])
    def delete(self, announcement_id):
        """Delete announcement"""
        try:
            announcement = Announcement.query.get_or_404(announcement_id)
            user_id = get_jwt_identity()
           
            if announcement.created_by != user_id and not User.query.get(user_id).has_role('Admin'):
                return {"message": "Forbidden"}, 403
           
            db.session.delete(announcement)
            db.session.commit()
            return {"message": "Announcement deleted"}, 200
        except Exception as e:
            return {"message": "Announcement deletion failed"}, 400
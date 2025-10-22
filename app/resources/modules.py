from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models.module import Module
from ..models.course import Course
from ..models.user import User
from ..schemas.module import ModuleSchema, ModuleCreateSchema, ModuleUpdateSchema
from ..utils.rbac import role_required


module_schema = ModuleSchema()
module_create_schema = ModuleCreateSchema()
module_update_schema = ModuleUpdateSchema()


def register(api):
    api.add_resource(ModuleListResource, "/courses/<int:course_id>/modules")
    api.add_resource(ModuleResource, "/modules/<int:module_id>")


class ModuleListResource(Resource):
    def get(self, course_id):
        """Get modules for a course"""
        modules = Module.query.filter_by(course_id=course_id).order_by(Module.position).all()
        return [module.to_dict() for module in modules], 200
   
    @jwt_required()
    @role_required(['Admin', 'Instructor'])
    def post(self, course_id):
        """Create a new module"""
        try:
            # Check if user can edit this course
            course = Course.query.get_or_404(course_id)
            user_id = get_jwt_identity()
           
            if course.created_by != user_id and not User.query.get(user_id).has_role('Admin'):
                return {"message": "Forbidden"}, 403
           
            data = module_create_schema.load(request.get_json() or {})
           
            module = Module(
                course_id=course_id,
                title=data["title"],
                position=data.get("position", 1)
            )
           
            db.session.add(module)
            db.session.commit()
           
            return module.to_dict(), 201
        except Exception as e:
            return {"message": "Module creation failed"}, 400


class ModuleResource(Resource):
    def get(self, module_id):
        """Get module details"""
        module = Module.query.get_or_404(module_id)
        return module.to_dict(), 200
   
    @jwt_required()
    @role_required(['Admin', 'Instructor'])
    def put(self, module_id):
        """Update module"""
        try:
            module = Module.query.get_or_404(module_id)
            course = Course.query.get(module.course_id)
            user_id = get_jwt_identity()
           
            if course.created_by != user_id and not User.query.get(user_id).has_role('Admin'):
                return {"message": "Forbidden"}, 403
           
            data = module_update_schema.load(request.get_json() or {})
           
            for key, value in data.items():
                setattr(module, key, value)
           
            db.session.commit()
            return module.to_dict(), 200
        except Exception as e:
            return {"message": "Module update failed"}, 400
   
    @jwt_required()
    @role_required(['Admin', 'Instructor'])
    def delete(self, module_id):
        """Delete module"""
        try:
            module = Module.query.get_or_404(module_id)
            course = Course.query.get(module.course_id)
            user_id = get_jwt_identity()
           
            if course.created_by != user_id and not User.query.get(user_id).has_role('Admin'):
                return {"message": "Forbidden"}, 403
           
            db.session.delete(module)
            db.session.commit()
            return {"message": "Module deleted"}, 200
        except Exception as e:
            return {"message": "Module deletion failed"}, 400

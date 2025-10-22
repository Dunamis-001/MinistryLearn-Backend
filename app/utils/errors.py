from flask import jsonify


def handle_error(error):
    """Handle common errors and return appropriate responses"""
    if hasattr(error, 'code'):
        if error.code == 400:
            return jsonify({"message": "Bad Request", "error": str(error)}), 400
        elif error.code == 401:
            return jsonify({"message": "Unauthorized"}), 401
        elif error.code == 403:
            return jsonify({"message": "Forbidden"}), 403
        elif error.code == 404:
            return jsonify({"message": "Not Found"}), 404
        elif error.code == 409:
            return jsonify({"message": "Conflict"}), 409
        elif error.code == 422:
            return jsonify({"message": "Validation Error", "errors": str(error)}), 422
        elif error.code == 500:
            return jsonify({"message": "Internal Server Error"}), 500
   
    return jsonify({"message": "An error occurred"}), 500

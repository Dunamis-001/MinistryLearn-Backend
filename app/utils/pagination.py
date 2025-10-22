from flask import request


def paginate(query, page=None, per_page=None):
    """Paginate a SQLAlchemy query"""
    if page is None:
        page = request.args.get('page', 1, type=int)
    if per_page is None:
        per_page = request.args.get('per_page', 10, type=int)
   
    # Limit per_page to prevent abuse
    per_page = min(per_page, 100)
   
    pagination = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
   
    return {
        'items': [item.to_dict() for item in pagination.items],
        'page': pagination.page,
        'per_page': pagination.per_page,
        'total': pagination.total,
        'pages': pagination.pages,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev
    }

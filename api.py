from flask import Blueprint, request, jsonify
from models import db, Resource

api_bp = Blueprint('api', __name__)

@api_bp.route('/resources', methods=['POST'])
def create_resource():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'message': 'Name is required'}), 400
    
    new_resource = Resource(name=data['name'], description=data.get('description'))
    db.session.add(new_resource)
    db.session.commit()
    return {'id': new_resource.id, 'name': new_resource.name}, 201

@api_bp.route('/resources', methods=['GET'])
def get_resources():
    resources = Resource.query.all()
    return jsonify([{'id': res.id, 'name': res.name, 'description': res.description} for res in resources])

@api_bp.route('/resources/<int:id>', methods=['GET'])
def get_resource(id):
    resource = Resource.query.get_or_404(id)
    return {'id': resource.id, 'name': resource.name, 'description': resource.description}

@api_bp.route('/resources/<int:id>', methods=['PUT'])
def update_resource(id):
    resource = Resource.query.get(id)
    if not resource:
        return jsonify({'message': 'Resource not found'}), 404

    data = request.get_json()
    resource.name = data.get('name', resource.name)
    resource.description = data.get('description', resource.description)

    db.session.commit()
    return jsonify({
        'id': resource.id,
        'name': resource.name,
        'description': resource.description
    })


@api_bp.route('/resources/<int:id>', methods=['DELETE'])
def delete_resource(id):
    resource = Resource.query.get_or_404(id)
    db.session.delete(resource)
    db.session.commit()
    return {'message': 'Resource deleted successfully'}, 204

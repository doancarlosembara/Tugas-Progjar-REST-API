# models.py
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint, request, jsonify

db = SQLAlchemy()

# Create a Blueprint for the API
api_bp = Blueprint('api', __name__)

class Resource(db.Model):
    __tablename__ = 'resource'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Resource {self.name}>'

# API routes

@api_bp.route('/resources', methods=['POST'])
def create_resource():
    data = request.get_json()
    new_resource = Resource(name=data['name'], description=data['description'])
    db.session.add(new_resource)
    db.session.commit()
    return jsonify({'id': new_resource.id}), 201

@api_bp.route('/resources', methods=['GET'])
def get_resources():
    resources = Resource.query.all()
    return jsonify([{'id': resource.id, 'name': resource.name, 'description': resource.description} for resource in resources])

@api_bp.route('/resources/<int:id>', methods=['GET'])
def get_resource(id):
    resource = Resource.query.get_or_404(id)
    return jsonify({'id': resource.id, 'name': resource.name, 'description': resource.description})

@api_bp.route('/resources/<int:id>', methods=['PUT'])
def update_resource(id):
    resource = Resource.query.get_or_404(id)
    data = request.get_json()
    resource.name = data.get('name', resource.name)
    resource.description = data.get('description', resource.description)
    db.session.commit()
    return jsonify({'id': resource.id, 'name': resource.name, 'description': resource.description})

@api_bp.route('/resources/<int:id>', methods=['DELETE'])
def delete_resource(id):
    resource = Resource.query.get_or_404(id)
    db.session.delete(resource)
    db.session.commit()
    return jsonify({'message': 'Resource deleted successfully'}), 204

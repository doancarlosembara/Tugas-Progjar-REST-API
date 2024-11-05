# app.py
from flask import Flask, request, jsonify
from models import db, Resource, api_bp  # Ensure api_bp is imported

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resources.db'  # Database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Register the API blueprint
app.register_blueprint(api_bp, url_prefix='/api')  # Use the appropriate prefix for your API

# The blueprint already contains the routes for create, read, update, and delete operations.
# Here are the endpoints that can be included within the blueprint

@app.route('/api/resources', methods=['POST'])
def create_resource():
    data = request.get_json()
    new_resource = Resource(name=data['name'], description=data['description'])
    db.session.add(new_resource)
    db.session.commit()
    return jsonify({'id': new_resource.id}), 201

@app.route('/api/resources', methods=['GET'])
def get_resources():
    resources = Resource.query.all()
    return jsonify([{'id': resource.id, 'name': resource.name, 'description': resource.description} for resource in resources])

@app.route('/api/resources/<int:id>', methods=['GET'])
def get_resource(id):
    resource = Resource.query.get_or_404(id)
    return jsonify({'id': resource.id, 'name': resource.name, 'description': resource.description})

@app.route('/api/resources/<int:id>', methods=['PUT'])
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

@app.route('/api/resources/<int:id>', methods=['DELETE'])
def delete_resource(id):
    resource = Resource.query.get_or_404(id)
    db.session.delete(resource)
    db.session.commit()
    return jsonify({'message': 'Resource deleted successfully'}), 204

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database tables
    app.run(debug=True)

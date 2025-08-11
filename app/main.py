from flask import Flask, request, jsonify
from adapters.sqlalchemy_user_repository import db, UserRepository

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/dbname'
db.init_app(app)
user_repo = UserRepository()

@app.route('/')
def hello():
    return 'Hello, Flask with MariaDB!'

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    if not username or not email:
        return jsonify({'error': 'Username and email required'}), 400
    user = user_repo.add_user(username, email)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'guid': user.guid,
        'created_at': user.created_at.isoformat(),
        'updated_at': user.updated_at.isoformat()
    }), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = user_repo.get_all_users()
    return jsonify([
        {
            'id': u.id,
            'username': u.username,
            'email': u.email,
            'guid': u.guid,
            'created_at': u.created_at.isoformat(),
            'updated_at': u.updated_at.isoformat()
        } for u in users
    ])

@app.route('/users/<username>', methods=['GET'])
def get_user_by_name(username):
    user = user_repo.get_user_by_username(username)
    if user:
        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'guid': user.guid,
            'created_at': user.created_at.isoformat(),
            'updated_at': user.updated_at.isoformat()
        })
    return jsonify({'error': 'User not found'}), 404

@app.route('/users/<username>', methods=['DELETE'])
def delete_user_by_name(username):
    success = user_repo.delete_user_by_username(username)
    if success:
        return jsonify({'message': f'User {username} deleted.'})
    return jsonify({'error': 'User not found'}), 404

@app.route('/users/search', methods=['GET'])
def search_users():
    # You can now search users with a GET request to /users/search?q=part_of_name.
    username_part = request.args.get('q', '')
    users = user_repo.get_users_by_username_part(username_part)
    return jsonify([
        {
            'id': u.id,
            'username': u.username,
            'email': u.email,
            'guid': u.guid,
            'created_at': u.created_at.isoformat(),
            'updated_at': u.updated_at.isoformat()
        } for u in users
    ])

@app.route('/users/<username>', methods=['PUT'])
def update_user(username):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    user = user_repo.get_user_by_username(username)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Update fields if present in request
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']

    db.session.commit()

    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'guid': user.guid,
        'created_at': user.created_at.isoformat(),
        'updated_at': user.updated_at.isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True)

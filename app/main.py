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

if __name__ == '__main__':
    app.run(debug=True)

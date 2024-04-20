# from flask import Flask, request, jsonify, send_file
# import jwt
# import datetime
# import hashlib
# import secrets
# import os
#
# app = Flask(__name__)
#
# # Custom hash function for generating secret key
# def generate_secret_key():
#     current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     unique_string = current_time + secrets.token_urlsafe(16)
#     return hashlib.sha256(unique_string.encode()).hexdigest()[:7]  # Take first 7 characters
#
# # Generated Secret Key
# SECRET_KEY = generate_secret_key()
#
# # Function to generate a personalized JWT token
# def generate_token(user_id, user_type, username):
#     payload = {
#         'user_id': user_id,
#         'user_type': user_type,
#         'username': username,  # Additional personalized information
#         'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)  # Token expiration time
#     }
#     token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
#     return token
#
# # Convert JWT token to 7-digit code
# def convert_to_seven_digit_code(token):
#     hash_value = hashlib.sha256(token.encode()).hexdigest()
#     return hash_value[:7]
#
# # Endpoint to serve index.html
# @app.route('/')
# def index():
#     return send_file('index.html')
#
# # Endpoint to generate JWT token
# @app.route('/generate_token', methods=['POST'])
# def generate_jwt_token():
#     data = request.json
#     user_id = data.get('user_id')
#     user_type = data.get('user_type')
#     username = data.get('username')
#
#     token = generate_token(user_id, user_type, username)
#     code = convert_to_seven_digit_code(token)
#
#     return jsonify({'code': code}), 200
#
# if __name__ == '__main__':
#     app.run(debug=True)
#
#




# from flask import Flask, request, jsonify, send_file
# from flask_sqlalchemy import SQLAlchemy
# import jwt
# import datetime
# import hashlib
# import secrets
# import os
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# db = SQLAlchemy(app)
#
# # Custom hash function for generating secret key
# def generate_secret_key():
#     current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     unique_string = current_time + secrets.token_urlsafe(16)
#     return hashlib.sha256(unique_string.encode()).hexdigest()[:7]  # Take first 7 characters
#
# # Generated Secret Key
# SECRET_KEY = generate_secret_key()
#
# # Define User model
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.String(50), nullable=False)
#     user_type = db.Column(db.String(50), nullable=False)
#     username = db.Column(db.String(50), nullable=False)
#     code = db.Column(db.String(7), nullable=False)
#
#     def __repr__(self):
#         return f"User('{self.user_id}', '{self.user_type}', '{self.username}', '{self.code}')"
#
# # Initialize the database
# with app.app_context():
#     db.create_all()
#
# # Function to generate a personalized JWT token
# def generate_token(user_id, user_type, username):
#     payload = {
#         'user_id': user_id,
#         'user_type': user_type,
#         'username': username,  # Additional personalized information
#         'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)  # Token expiration time
#     }
#     token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
#     return token
#
# # Convert JWT token to 7-digit code
# def convert_to_seven_digit_code(token):
#     hash_value = hashlib.sha256(token.encode()).hexdigest()
#     return hash_value[:7]
#
# # Endpoint to serve index.html
# @app.route('/')
# def index():
#     return send_file('index.html')
#
# # Endpoint to generate JWT token
# @app.route('/generate_token', methods=['POST'])
# def generate_jwt_token():
#     data = request.json
#     user_id = data.get('user_id')
#     user_type = data.get('user_type')
#     username = data.get('username')
#
#     token = generate_token(user_id, user_type, username)
#     code = convert_to_seven_digit_code(token)
#
#     # Save user input and hash code to the database
#     new_user = User(user_id=user_id, user_type=user_type, username=username, code=code)
#     db.session.add(new_user)
#     db.session.commit()
#
#     return jsonify({'code': code}), 200
#
# if __name__ == '__main__':
#     app.run(debug=True)






from flask import Flask, request, jsonify, send_file, render_template
from flask_sqlalchemy import SQLAlchemy
import jwt
import datetime
import hashlib
import secrets
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secure secret key
db = SQLAlchemy(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    user_type = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    code = db.Column(db.String(7), nullable=False)

    def __repr__(self):
        return f"User('{self.user_id}', '{self.user_type}', '{self.username}', '{self.code}')"

# Initialize the database
with app.app_context():
    db.create_all()

# Function to generate a personalized JWT token
def generate_token(user_id, user_type, username):
    payload = {
        'user_id': user_id,
        'user_type': user_type,
        'username': username,  # Additional personalized information
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)  # Token expiration time
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token

# Convert JWT token to 7-digit code
def convert_to_seven_digit_code(token):
    hash_value = hashlib.sha256(token.encode()).hexdigest()
    return hash_value[:7]

# Endpoint to serve index.html
@app.route('/')
def index():
    return send_file('index.html')

# Endpoint to generate JWT token
@app.route('/generate_token', methods=['POST'])
def generate_jwt_token():
    data = request.json
    user_id = data.get('user_id')
    user_type = data.get('user_type')
    username = data.get('username')

    token = generate_token(user_id, user_type, username)
    code = convert_to_seven_digit_code(token)

    # Save user input and hash code to the database
    new_user = User(user_id=user_id, user_type=user_type, username=username, code=code)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'code': code}), 200

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Hash the provided password to match with the stored hash in the database
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user = User.query.filter_by(username=username, code=hashed_password).first()

        if user:
            return 'Login Successful'  # You can redirect to another page upon successful login
        else:
            return 'Login Failed. Invalid username or password.'

    return render_template('login.html')  # Create a login form template (login.html)

if __name__ == '__main__':
    app.run(debug=True)


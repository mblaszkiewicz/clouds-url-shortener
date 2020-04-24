from flask import Flask, jsonify, request, abort
from db_authentication import *
import jwt

app = Flask(__name__)
# Private key used with JWT algorithm
private_key = 'secret_key'
# Object containing users' credentials
users_db = UsersDatabase()


@app.route('/users', methods=["POST"])
def create_new_user():
    """Creates a new user by saving its credentials in app memory. If username or password is missing, throws 400 HTML exception.
    Successful user creation finishes in JSON: { success: True }
    """

    # Checking if both required fields are in the form fields of the request
    if 'username' not in request.form.keys() or 'password' not in request.form.keys():
        abort(400)
    users_db.create_new_user(request.form.get('username'), request.form.get('password'))
    return jsonify({"success": True}), 200


@app.route('/users/login', methods=["POST"])
def login_user():
    """Login operation, generates tokens for users.
    When either of the required fields is missing or user data is incorrect, returns 403 HTML exception.
    Otherwise, returns JSON with the token
    """

    # Checking if both required fields are in the request form
    if 'username' not in request.form.keys() or 'password' not in request.form.keys():
        abort(403)
    username = request.form.get('username')
    password = request.form.get('password')

    # Checking if credentials are correct with the data
    if not users_db.check_user_credentials(username, password):
        abort(403)

    # Creating a token using JWT and a private key defined above
    token = jwt.encode({'user': username}, private_key)
    return jsonify(token=token.decode('UTF-8')), 200

#
# if __name__ == '__main__':
#     app.run(debug=True, port=5001)

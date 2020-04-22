from flask import Flask, jsonify, request, abort
from db_authentication import *
import jwt

app = Flask(__name__)
private_key = 'secret.key'


@app.route('/users', methods=["POST"])
def create_new_user():
    if 'username' not in request.form.keys() or 'password' not in request.form.keys():
        abort(404)
    create_new_user(request.form.get('username'), request.form.get('password'))
    return jsonify({"success: True"}, 200)


@app.route('/users/login', methods=["POST"])
def login_user():
    if 'username' not in request.form.keys() or 'password' not in request.form.keys():
        abort(404)
    username = request.form.get('username')
    password = request.form.get('password')
    if not check_user_credentials(username, password):
        abort(403)
    token = jwt.encode({'user': username}, private_key)
    return jsonify(token=token.decode('UTF-8')), 200


@app.route('/index', methods=["GET", "POST"])
def get_index():
    if request.method == "GET":
        return "GET"
    elif request.method == "POST":
        return "POST"

#
# if __name__ == '__main__':
#     app.run(debug=True, port=5001)

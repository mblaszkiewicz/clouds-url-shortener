from flask import render_template, request, jsonify
from flask import Flask, redirect, abort
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from db import *
from functools import wraps
import jwt

app = Flask(__name__)
private_key = 'secret.key'


def check_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'x-access-token' in request.headers:
            token = request.headers.get('x-access-token')
        else:
            abort(403)
        try:
            jwt.decode(token, private_key)
        except jwt.DecodeError:
            abort(403)
        return f(*args, **kwargs)
    return decorated


# function for checking the correctness of url
def is_valid_url(url):
    validate = URLValidator()
    try:
        validate(url)
        return True
    except ValidationError:
        return False


@app.route('/index', methods=['GET'])
def index_func():
    # for GET request, show the main page
    return render_template("index.html")


@app.route('/index', methods=['POST'])
@check_token
def index_func():
    # for POST request, post the parameter to dataset
    original_url = request.form['original_url']
    # when the url is valid, do POST, and return the generated short_url
    if is_valid_url(original_url):
        post_url(original_url)
        my_short_url = get_short_url_fromDB(original_url)
        return render_template("index.html", short_url=my_short_url)
    # when the url is invalid, input again
    else:
        print("Invalid url, input again.")
        return render_template("index.html")


@app.route('/index', methods=['DELETE'])
@check_token
def index_func():
    # for DELETE request, delete the dataset
    delete_data()
    print("URLs deleted.")
    return str("URLs deleted.")


@app.route('/<short_url>', methods=['GET'])
def redirect_to_original_url(short_url):
    # for GET request, redirect the generated short_url to its original_url
    original_url = get_url(short_url)
    return redirect(original_url)


@app.route('/<short_url>', methods=['POST'])
@check_token
def redirect_to_original_url(short_url):
    pass


@app.route('/<short_url>', methods=['PUT'])
@check_token
def redirect_to_original_url(short_url):
    # for PUT request, update the url
    original_url = get_url(short_url)
    post_url(original_url)
    return "URL updated."


@app.route('/<short_url>', methods=['DELETE'])
@check_token
def redirect_to_original_url(short_url):
    # for DELETE request, delete the specific item in dataset
    delete_url(short_url)
    return "Short_url deleted."


if __name__ == '__main__':
    app.run(debug=True, port=5001)

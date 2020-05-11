from flask import Flask, redirect, abort, jsonify, request
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from db_urls import *
from functools import wraps
import jwt

app = Flask(__name__)
# Private key used with JWT algorithm, has to be the same as the one used in the auth service
private_key = 'secret_key'
# Object storing mappings details
db = Database()


def check_token(f):
    """Decorator to be placed on functions which execution should be possible only to token holders. Should be used
    to protect the routes that are to be protected from unauthorized use by unregistered users.

    When the token field is not present in the header or token cannot be decoded (e.g., was created with different
    private key than the one defined here), function raises 403 HTML exception.

    Based on Flask tutorial resources at https://prettyprinted.com
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        if 'x-access-token' in request.headers:
            token = request.headers.get('x-access-token')
        else:
            abort(403)
            return
        try:
            jwt.decode(token, private_key)
        except jwt.DecodeError:
            abort(403)
        return f(*args, **kwargs)

    return decorated


def is_valid_url(url):
    """Checking the correctness of URL using a validator from Django framework.
    """
    validate = URLValidator()
    try:
        validate(url)
        return True
    except ValidationError:
        return False


@app.route('/', methods=['GET'])
@check_token
def index_get():
    """Returns all the mappings stored in the app
    """
    return jsonify(db.get_mappings()), 200


@app.route('/', methods=['POST'])
@check_token
def index_post():
    """Creates a new mapping for a URL given in as a field of a form
    """
    if 'url' not in request.form:
        abort(400)
    original_url = request.form['url']
    # When the url is invalid, abort and throw 400 HTML exception; else return the short_url
    if not is_valid_url(original_url):
        print("Invalid URL, abort 400")
        abort(400)
    else:
        # If URL already exist, return the existing ID; if not, first create a new mapping
        try:
            idx = db.get_url_id(original_url)
        except ValueError:
            idx = db.add_mapping(original_url)
        return jsonify({"short_url": idx}), 201


@app.route('/', methods=['DELETE'])
@check_token
def index_delete():
    """Deleting all mappings stored in the memory
    """
    db.delete_mappings()
    print("All URLs deleted")
    return "", 204


@app.route('/<short_url>', methods=['GET'])
def redirect_to_original_url(short_url):
    """ Redirect the generated short_url (ID) to its original url
    """
    short_url = int(short_url)
    try:
        original_url = db.get_mapping(short_url)
        return redirect(original_url), 301
    except KeyError:
        print("KeyError")
        abort(404)


@app.route('/<short_url>', methods=['PUT'])
@check_token
def refresh_mapping(short_url):
    short_url = int(short_url)
    """Assigning a new short URL (ID) for a chosen mapping
    """
    try:
        original_url = db.get_mapping(short_url)
        db.delete_mapping(short_url)
        idx = db.add_mapping(original_url)
        return jsonify({"short_url": idx}), 200
    except KeyError:
        abort(404)
    except Exception:
        abort(400)


@app.route('/<short_url>', methods=['DELETE'])
@check_token
def delete_mapping(short_url):
    """ Delete a given mapping (mapping identified by the ID)
    """
    short_url = int(short_url)
    try:
        db.delete_mapping(short_url)
        return "", 204
    except KeyError:
        abort(404)

# if __name__ == '__main__':
#     app.run(debug=True, port=5001)

import pandas as pd

users_db = {}


def create_new_user_db(username, password):
    users_db[username] = password
    return


def check_user_credentials(username, password):
    if users_db[username] == password:
        return True
    return False


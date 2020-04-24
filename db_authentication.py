class UsersDatabase:
    def __init__(self):
        self.users_db = {}

    def create_new_user(self, username, password):
        """Function to add a new user to the database. Might throw KeyError if username does not exist. """
        self.users_db[username] = password
        return

    def check_user_credentials(self, username, password):
        """Checking user credentials against the users dictionary"""
        return username in self.users_db.keys() and self.users_db[username] == password

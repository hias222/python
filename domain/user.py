class User:
    def __init__(self, id, username, email, guid):
        self.id = id
        self.username = username
        self.email = email
        self.guid = guid

    def __repr__(self):
        return f'<User {self.username}>'

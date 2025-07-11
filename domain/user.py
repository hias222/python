class User:
    def __init__(self, id, username, email, guid, created_at, updated_at):
        self.id = id
        self.username = username
        self.email = email
        self.guid = guid
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return f'<User {self.username}>'

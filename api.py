class api:
    create = "/api/admin/accounts/create"
    follow = "/api/following/create"
    note = "/api/notes/create"
    reactions = "/api/notes/reactions/create"
    profile = "/api/i/update"


class create:
    def __init__(self, username, password, token):
        self.data = {"username": username, "password": password, "i": token}

    def get_data(self):
        return self.data


class follow:
    def __init__(self, userId, token):
        self.data = {"userId": userId, "i": token}

    def get_data(self):
        return self.data


class note:
    def __init__(self, visibility, text, token):
        self.data = {"visibility": visibility, "text": text, "i": token}

    def get_data(self):
        return self.data

class renote:
    def __init__(self, local, visibility, noteId, token):
        self.data = {"localOnly": local,"visibility": visibility,"renoteId": noteId,"i": token}

    def get_data(self):
        return self.data


class reactions:
    def __init__(self, noteId, reaction, token):
        self.data = {"noteId": noteId, "reaction": reaction, "i": token}

    def get_data(self):
        return self.data


class profile:
    def __init__(self, name, avatarId, token):
        self.data = {"name": name, "avatarId": avatarId, "i": token}

    def get_data(self):
        return self.data

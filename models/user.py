import json


class User(dict):
    def __init__(self, id, username, first_name, last_name):
        dict.__init__(self, id=id, username=username, first_name=first_name, last_name=last_name)
        self.id = id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return "[" + self.id + ", " + self.username + ", " + self.first_name + ", " + self.last_name + "]"

    @staticmethod
    def object_decoder(object_user):
        return User(object_user["id"], object_user["username"],
                    object_user["first_name"],
                    object_user["last_name"])

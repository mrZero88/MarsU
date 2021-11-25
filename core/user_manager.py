import json
from types import SimpleNamespace

from tinydb import Query

from models.user import User
from utils.command import Command


class UserManager:
    def __init__(self, db):
        self.db = db
        self.usersTable = self.db.table("users")
        self.user = None

    def load_user(self):
        if self.exists_users():
            self.load_user_from_database()
        else:
            self.load_user_from_computer()
            self.insert_user_in_database()

    def exists_users(self):
        return True if self.usersTable.all() else False

    def insert_user_in_database(self):
        if self.user is not None:
            self.usersTable.insert(self.user)

    def load_user_from_database(self):
        json_string = json.dumps(self.usersTable.all()[0])
        self.user = json.loads(json_string, object_hook=User.object_decoder)

    def load_user_from_computer(self):
        user_id, username, user_names = self.get_user_data()
        first_name, last_name = user_names.split()
        self.user = User(user_id, username, first_name, last_name)

    def get_user_data(self):
        command = "grep $(whoami) /etc/passwd | tr -s \":\" | awk -F '[:,]' '{print $3\",\"$1\",\"$5}'"
        output = Command.run_command_with_output_nosplit(command)
        return output.split(",")

    def get_user(self):
        return self.user

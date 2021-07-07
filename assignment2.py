from encryption import encryption
from drive import drive
import os


class secure_cloud:
    users = {}
    files = {}

    # add a user and generate their private key
    def add_user(self, user_name, password):
        private_key = self.encryption.get_private_key(user_name)

        public_key = private_key.public_key()

        self.users[user_name] = {"user_name": user_name, "password": password, "private_key": private_key, "public_key": public_key}

    # remove a user
    def remove_user(self, user_name):
        for user in self.users:
            if user_name == self.users[user]["user_name"]:
                del self.users[user]
                os. remove(user_name)
                break

    # login the user provided they match an existing username and password
    def login(self, user_name, password):
        for user in self.users:
            if user_name == self.users[user]["user_name"] and password == self.users[user]["password"]:
                return (True, user_name)

        return (False, None)

    # log out the user
    def logout(self, user_name):
        print(f"[{user_name}] has logged out!")
        return (False, None)

    # encrypt and create file
    def create_file(self, user_name, file_name, file_content):
        signature = self.encryption.sign(self.users[user_name]["private_key"], user_name.encode('utf-8'))
        file_content = encryption.encrypt(self.users[user_name]["public_key"], file_content.encode('utf-8'))
        file_id = self.drive.get_id(file_name)
        self.files[file_name] = {"file_content": file_content.decode("ISO-8859-1"), "signature": signature, "user_name": user_name, "file_id": file_id}
        self.drive.create_file(file_name, file_content.decode("ISO-8859-1"))

    # retrieve and decrypt file
    def view_file(self, file_name):
        decryption_key = self.users[self.files[file_name]["user_name"]]["public_key"]
        if encryption.verify_signarture("", decryption_key,
                                        self.files[file_name]["signature"],
                                        self.files[file_name]["user_name"].encode('utf-8')):
            return encryption.decrypt(self.users[self.files[file_name]["user_name"]]["private_key"], self.files[file_name]["file_content"].encode("ISO-8859-1")).decode()

    def __init__(self):
        self.encryption = encryption()
        self.drive = drive()

        self.add_user("Admin", "root")
        self.add_user("Negative Bond", "00-1")
        self.add_user("Jeffery Bond", "007")
        self.add_user("Arthur Bond", "008")
        self.add_user("Amy Bond", "009")
        self.add_user("Johnathan Bond", "0010")

        # basic CLI
        while True:
            UN = input("user_name: ")
            PW = input("password: ")
            login_attempt = self.login(UN, PW)
            if login_attempt[0]:
                print(f"[{login_attempt[1]}] has logged in!")
                while login_attempt[0]:
                    current_input = input(f"[{login_attempt[1]}] ")

                    if(current_input == "exit"):
                        login_attempt = self.logout(login_attempt[1])

                    elif (current_input == "add_user"):
                        UN = input(f"[{login_attempt[1]}] new user_name: ")
                        PW = input(f"[{login_attempt[1]}] new password: ")
                        self.add_user(UN, PW)
                        print(f"[{login_attempt[1]}] {UN} has been created!")

                    elif (current_input == "remove_user"):
                        UN = input(f"[{login_attempt[1]}] user_name to be removed:")
                        for user in self.users:
                            if UN == self.users[user]["user_name"]:
                                self.remove_user(UN)
                                break
                        print(f"[{login_attempt[1]}] {UN} has been removed!")
                        if UN == login_attempt[1]:
                            print(f"[{login_attempt[1]}] current logged in user has been removed, logging out...")
                            login_attempt = self.logout(login_attempt[1])

                    elif (current_input == "create_file"):
                        file_name = input(f"[{login_attempt[1]}] please enter file name: ")
                        file_content = input(f"[{login_attempt[1]}] please enter file content: ")
                        self.create_file(login_attempt[1], file_name, file_content)
                        print(f"[{login_attempt[1]}] file {file_name} has been created!")

                    elif (current_input == "view_file"):
                        file_name = input(f"[{login_attempt[1]}] please enter file name: ")
                        print(f"[{login_attempt[1]}] {self.view_file(file_name)}")

                    elif (current_input == "list_files"):
                        self.drive.list_files()

            else:
                print(f"[{UN}, {PW}] is not a valid account!")


if __name__ == '__main__':
    cloud = secure_cloud()

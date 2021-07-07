from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth


class drive:
    ROOT_ID = "FOO"

    # creates and uploades a file to google drive
    def create_file(self, file_name, file_content):
        file = self.drive.CreateFile({'title': file_name, 'parents': [{'id': self.ROOT_ID}]})
        file.SetContentString(file_content)
        file.Upload()

    # finds a files id
    def get_id(self, file_name):
        file_list = self.drive.ListFile({'q': f"'{self.ROOT_ID}' in parents and trashed=false"}).GetList()
        for file in file_list:
            if file['title'] == file_name:
                return file
        return None

    # lists all files currently in the assignment2 folder on google drive
    def list_files(self):
        file_list = self.drive.ListFile({'q': f"'{self.ROOT_ID}' in parents and trashed=false"}).GetList()
        for file in file_list:
            print(f"title: {file['title']}")

    def __init__(self):
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()  # Creates local webserver and auto handles authentication.
        self.drive = GoogleDrive(gauth)

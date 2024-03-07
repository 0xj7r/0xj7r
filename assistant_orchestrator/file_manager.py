class FileManager:
    def __init__(self, client):
        self.client = client

    def upload_file(self, file_path, purpose):
        with open(file_path, "rb") as file:
            return self.client.files.create(file=file, purpose=purpose)

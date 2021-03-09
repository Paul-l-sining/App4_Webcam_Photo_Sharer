from filestack import Client


class FileSharer():
    """
    A generator that generates a URL of the file you choose to upload
    """

    def __init__(self, filepath, apikey='ArFQU9ogfQ5uoneGAZTHqz'):
        self.filepath = filepath
        self.apikey = apikey

    def share(self):
        client = Client(self.apikey)
        new_filelink = client.upload(filepath=self.filepath)
        return new_filelink.url

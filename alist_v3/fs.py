class FileSystem:
    def __init__(self, domain: str, token: str):
        self._token = token
        self.domain = domain
        self.path = 'api/fs/'
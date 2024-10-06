from alist_v3.admin import Admin
from alist_v3.auth import Auth
from alist_v3.exceptions import AlistV3Exception
from alist_v3.fs import FileSystem
from alist_v3.public import Public


class Client:
    def __init__(self, domain: str = 'http://localhost:5244/'):
        public = Public(domain)
        try:
            is_pong = public.ping()
            if not is_pong:
                raise AlistV3Exception(f"Could not ping alist at {domain}")
        except AlistV3Exception as e:
            raise e

        self.domain = domain
        self.token = None
        self.auth = Auth(domain)
        self.public = public
        self.fs = None
        self.admin = None

    def login(self, username, password):
        """Login and initialize all authenticated modules."""
        self.token = self.auth.login(username, password)
        self.fs = FileSystem(self.domain, self.token)
        self.admin = Admin(self.domain, self.token)

    def logout(self):
        """Logout all authenticated modules."""
        self.token = None
        self.fs = None
        self.admin = None
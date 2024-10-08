from alist_v3.exceptions import AlistV3Exception
from alist_v3.models.auth_models import TokenResponse
from alist_v3.rest_adapter import RestAdapter
from hashlib import sha256

class Auth:
    def __init__(self, domain: str = 'http://localhost:5244/', ssl_verify: bool = True):
        self.domain = domain
        self._rest_adapter = RestAdapter(self.domain, ssl_verify=ssl_verify)
        self.path = 'api/auth/'
        # Why is Alist reusing salt?
        self._hash_salt = '-https://github.com/alist-org/alist'

    def login(self, username: str, password: str, is_hashed: bool = True):
        endpoint = 'login/hash' if is_hashed else 'login'
        pwd = sha256((password + self._hash_salt).encode()).hexdigest() if is_hashed else password
        data = {'username': username, 'password': pwd }
        response = self._rest_adapter.post(path=self.path, endpoint=endpoint, data=data)
        if response.data is None and 'password' in response.message:
            raise AlistV3Exception(response.message)
        try:
            token_response = TokenResponse(**response.data)
            token = token_response.token
            return token
        except (TypeError, AlistV3Exception) as e:
            raise AlistV3Exception from e
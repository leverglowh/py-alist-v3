class TokenResponse:
    def __init__(self, token):
        self.token = token

class MFATokenResponse:
    def __init__(self, qr: str, secret: str):
        self.qr = qr
        self.secret = secret

class User:
    id: int
    username: str
    password: str
    base_path: str
    role: int
    disabled: bool
    permission: int
    sso_id: str

    def __init__(self, id: int, username: str, password: str, base_path: str, role: int, disabled: bool, permission: int, sso_id: str, **kwargs) -> None:
        self.id = id
        self.username = username
        self.password = password
        self.base_path = base_path
        self.role = role
        self.disabled = disabled
        self.permission = permission
        self.sso_id = sso_id
        self.__dict__.update(kwargs)
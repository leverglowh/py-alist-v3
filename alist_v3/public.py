from alist_v3.models.settings_models import Settings
from alist_v3.rest_adapter import RestAdapter

class Public:
    def __init__(self, domain: str):
        self._path = 'api/public/'
        self._rest_adapter = RestAdapter(domain)

    def ping(self):
        return self._rest_adapter.ping()

    def get_settings(self) -> Settings:
        response = self._rest_adapter.get(self._path, 'settings')
        return Settings(**response.data)

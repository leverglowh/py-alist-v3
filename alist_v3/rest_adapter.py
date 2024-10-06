import logging
import requests
import requests.packages
from typing import Dict
from json import JSONDecodeError

from alist_v3.exceptions import AlistV3Exception
from alist_v3.models.rest_models import Result

class RestAdapter:
    def __init__(self, domain: str = 'http://localhost:5244/', token: str = '', ssl_verify: bool = True, logger: logging.Logger = None):
        """
        Constructor for RestAdapter
        :param domain: alist domain WITH trailing slash, http://localhost:5244/ when used locally with default port
        :param token: (optional) auth key for requests other than login
        :param ssl_verify: Normally set to True, but if having SSL/TLS cert validation issues, can turn off with False
        :param logger: (optional) If your app has a logger, pass it in here
        """
        self.url = domain
        self._token = token
        self._ssl_verify = ssl_verify
        self._logger = logger or logging.getLogger(__name__)
        if not ssl_verify:
            # noinspection PyUnresolvedReferences
            requests.packages.urllib3.disable_warnings()

    def ping(self) -> bool:
        try:
            self._logger.debug(msg=f"Pinging alist at {self.url}")
            response = requests.request(method='GET', url=self.url + 'ping', verify=self._ssl_verify)
            if response.status_code != 200:
                self._logger.error(f"Could not ping alist at {response.url}")
                raise AlistV3Exception("Ping failed")
            else:
                return response.text == 'pong'
        except requests.exceptions.RequestException as e:
            self._logger.error(msg=(str(e)))
            raise AlistV3Exception(f"Cannot complete ping request") from e

    def get(self, path: str, endpoint: str, ep_params: Dict = None) -> Result:
        """
        Sends get request
        :param path: the path of the request url, can be auth/fs/admin etc
        :param endpoint: the endpoint of the request
        :param ep_params: (optional) endpoint params
        :return: an alist Result object
        """
        return self._do(http_method='GET', path=path, endpoint=endpoint, ep_params=ep_params)

    def post(self, path: str, endpoint: str, ep_params: Dict = None, data: Dict = None) -> Result:
        """
        Sends post request
        :param path: the path of the request url, can be auth/fs/admin etc
        :param endpoint: the endpoint of the request
        :param ep_params: (optional) endpoint params
        :param data: (optional) data dict to be sent in the request
        :return: an alist Result object
        """
        return self._do(http_method='POST', path=path, endpoint=endpoint, ep_params=ep_params, data=data)

    def put(self, path: str, endpoint: str, ep_params: Dict = None, data: Dict = None) -> Result:
        """
        Sends put request
        :param path: the path of the request url, can be auth/fs/admin etc
        :param endpoint: the endpoint of the request
        :param ep_params: (optional) endpoint params
        :param data: (optional) data dict to be sent in the request
        :return: an alist Result object
        """
        return self._do(http_method='PUT', path=path, endpoint=endpoint, ep_params=ep_params, data=data)

    def _do(self, http_method: str, path: str, endpoint: str, ep_params: Dict = None, data: Dict = None) -> Result:
        """
        The underlying function that actually makes the request
        :param http_method: method of request, between GET, POST and PUT
        :param path: the path of the request url, can be auth/fs/admin etc
        :param endpoint: the endpoint of the request
        :param ep_params: (optional) endpoint params
        :param data: (optional) data dict to be sent in the request
        :return: an alist Result object
        """
        full_url = self.url + path + endpoint
        headers = {'Authorization': self._token}
        log_line_pre = f"method={http_method}, url={full_url}, params={ep_params}"
        log_line_post = ', '.join((log_line_pre, "success={}, status_code={}, message={}"))
        # Log HTTP params and perform an HTTP request, catching and re-raising any exceptions
        try:
            self._logger.debug(msg=log_line_pre)
            response = requests.request(method=http_method, url=full_url, verify=self._ssl_verify, headers=headers,
                                        params=ep_params, json=data)
            # Deserialize JSON output to Python object, or return failed Result on exception
            try:
                data_out = response.json()
            except (ValueError, JSONDecodeError) as e:
                self._logger.error(msg=log_line_post.format(False, None, e))
                raise AlistV3Exception("Bad JSON in response") from e

            # If status_code in 200-299 range, return success Result with data, otherwise raise exception
            is_success = 299 >= data_out['code'] >= 200  # 200 to 299 is OK
            log_line = log_line_post.format(is_success, data_out['code'], data_out['message'])
            if is_success:
                self._logger.debug(msg=log_line)
                return Result(
                    code=data_out['code'],
                    message=data_out.get('message', ''),
                    data=data_out.get('data', {})
                )
            self._logger.error(msg=log_line)
            raise AlistV3Exception(f"{data_out['code']}: {data_out['message']}")
        except requests.exceptions.RequestException as e:
            self._logger.error(msg=(str(e)))
            raise AlistV3Exception(f"Cannot complete request") from e

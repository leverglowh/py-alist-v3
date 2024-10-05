import json
from unittest import TestCase, mock
import requests
from requests import RequestException

from alist_v3.exceptions import AlistV3Exception
from alist_v3.models import Result
from alist_v3.rest_adapter import RestAdapter

class TestRestAdapter(TestCase):
    def setUp(self):
        self.rest_adapter = RestAdapter()
        self.response = requests.Response()
        self.ok_response_content = json.dumps({'code': 200, 'message': 'ok', 'data': { 'id': 1 }}).encode()
        self.ko199_response_content = json.dumps({'code': 199, 'message': 'ko199', 'data': None}).encode()
        self.ko400_response_content = json.dumps({'code': 400, 'message': 'ko400', 'data': None}).encode()

    def test__do_good_request_returns_result(self):
        self.response.status_code = 200
        self.response._content = self.ok_response_content
        with mock.patch("requests.request", return_value=self.response):
            result = self.rest_adapter._do('GET', '', '')
            self.assertIsInstance(result, Result)

    def test__do_should_raise_on_inner_code_300_up(self):
        self.response.status_code = 200
        self.response._content = self.ko400_response_content
        with mock.patch("requests.request", return_value=self.response):
            with self.assertRaises(AlistV3Exception):
                self.rest_adapter._do('GET', '', '')

    def test__do_should_raise_on_inner_code_199_down(self):
        self.response.status_code = 200
        self.response._content = self.ko199_response_content
        with mock.patch("requests.request", return_value=self.response):
            with self.assertRaises(AlistV3Exception):
                self.rest_adapter._do('GET', '', '')

    def test__do_bad_request_raises_alist_exception(self):
        with mock.patch("requests.request", side_effect=RequestException):
            with self.assertRaises(AlistV3Exception):
                self.rest_adapter._do('GET', '', '')

    def test__do_bad_json_raises_alist_exception(self):
        bad_json = '{"some bad json": '.encode()
        self.response._content = bad_json
        with mock.patch("requests.request", return_value=self.response):
            with self.assertRaises(AlistV3Exception):
                self.rest_adapter._do('GET', '', '')

    def test__do_300_or_higher_raises_alist_exception(self):
        self.response.status_code = 300
        with mock.patch("requests.request", return_value=self.response):
            with self.assertRaises(AlistV3Exception):
                self.rest_adapter._do('GET', '', '')

    def test__do_199_or_lower_raises_alist_exception(self):
        self.response.status_code = 199
        with mock.patch("requests.request", return_value=self.response):
            with self.assertRaises(AlistV3Exception):
                self.rest_adapter._do('GET', '', '')

    #region test get / post / put functions
    def test_get_method_passes_in_get(self):
        self.response.status_code = 200
        self.response._content = self.ok_response_content
        with mock.patch("requests.request", return_value=self.response) as request:
            self.rest_adapter.get('', '')
            self.assertTrue(request.method, 'GET')

    def test_post_method_passes_in_post(self):
        self.response.status_code = 200
        self.response._content = self.ok_response_content
        with mock.patch("requests.request", return_value=self.response) as request:
            self.rest_adapter.post('', '')
            self.assertTrue(request.method, 'POST')

    def test_put_method_passes_in_put(self):
        self.response.status_code = 200
        self.response._content = self.ok_response_content
        with mock.patch("requests.request", return_value=self.response) as request:
            self.rest_adapter.put('', '')
            self.assertTrue(request.method, 'PUT')
    #endregion
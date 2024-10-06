from unittest import TestCase, mock
from unittest.mock import MagicMock, patch

from alist_v3.admin import Admin
from alist_v3.auth import Auth
from alist_v3.client import Client
from alist_v3.exceptions import AlistV3Exception
from alist_v3.fs import FileSystem
from alist_v3.public import Public

class TestClientInit(TestCase):
    @patch.object(Public, 'ping', return_value=False)
    def test_no_pong_init_client_ko(self, _):
        with self.assertRaises(AlistV3Exception) as context:
            self.client = Client()
        self.assertIn('Could not ping alist at', str(context.exception))

    @patch.object(Public, 'ping', return_value=True)
    def test_pong_init_client(self, _):
        try:
            self.client = Client()
        except AlistV3Exception:
            self.fail("correct pong should not raise AlistV3Exception")

class TestClient(TestCase):
    @patch.object(Public, 'ping', return_value=True)
    def setUp(self, _):
        self.mock_auth = MagicMock(spec=Auth)
        self.mock_public = MagicMock(spec=Public)

        self.client = Client()
        self.client.auth = self.mock_auth
        self.client.public = self.mock_public

    def test_initial_client(self):
        self.assertIsNone(self.client.token)
        self.assertIsNone(self.client.fs)
        self.assertIsNone(self.client.admin)
        self.assertIsInstance(self.client.public, Public)
        self.assertIsInstance(self.client.auth, Auth)

    def test_login_ok(self):
        user = "username"
        pwd = "password"
        mock_token = "fake_token"
        self.mock_auth.login.return_value = mock_token

        self.client.login(user, pwd)
        self.mock_auth.login.assert_called_with(user, pwd)

        self.assertEqual(self.client.token, mock_token)
        self.assertIsNotNone(self.client.token)
        self.assertIsInstance(self.client.fs, FileSystem)
        self.assertIsInstance(self.client.admin, Admin)

    def test_wrong_pwd_login_ko(self):
        self.mock_auth.login.side_effect = AlistV3Exception('password is incorrect')
        with self.assertRaises(AlistV3Exception) as context:
            self.client.login('invalid', 'credentials')
        self.assertIn('password', str(context.exception))

    def test_login_fail(self):
        self.mock_auth.login.side_effect = AlistV3Exception('some other error')
        with self.assertRaises(AlistV3Exception):
            self.client.login('some', 'credentials')

    def test_logout_(self):
        self.client.logout()
        self.assertIsNone(self.client.token)
        self.assertIsNone(self.client.fs)
        self.assertIsNone(self.client.admin)

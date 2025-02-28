import unittest
from unittest.mock import patch
from my_http import HttpRequest, HttpResponse


class TestHttpRequest(unittest.TestCase):
    @patch("main.LOGER.warning")
    def test_to_bytes(self, mock_logger):
        """Тестирование преобразования HttpRequest в байты"""
        request = HttpRequest(
            method="GET",
            host="http://test.ru",
            path="/index.html",
            headers={
                "Connection": "keep-alive",
                "Content-Type": "application/json",
                "User-Agent": "python-requests/3.9"
            },
        )
        expected_bytes = b'GET /index.html HTTP/1.1\r\nHost: http://test.ru\r\nConnection: keep-alive\r\n' \
                         b'Content-Type: application/json\r\nUser-Agent: python-requests/3.9\r\n\r\n'
        self.assertEqual(request.to_bytes(), expected_bytes)
        mock_logger.assert_called_once_with("Отсутсвует логин и токен пользователя")

    def test_from_bytes(self):
        """Тестирование преобразования байтов в HttpRequest"""
        binary_data = b'POST /send_sms HTTP/1.1\r\nHost: http://localhost:4010\r\n' \
                      b'Connection: keep-alive\r\n' \
                      b'Authorization: Basic dGVzdF9sb2dpbl8xOnRlc3RfcGFzc3dvcmRfMQ==\r\n' \
                      b'User-Agent: Python/3.9\r\nContent-Type: application/json\r\n\r\n'
        request = HttpRequest.from_bytes(binary_data)
        self.assertEqual(request.method, "POST")
        self.assertEqual(request.host, "http://localhost:4010")
        self.assertEqual(request.path, "/send_sms")
        self.assertEqual(request.token, "dGVzdF9sb2dpbl8xOnRlc3RfcGFzc3dvcmRfMQ==")
        self.assertEqual(request.headers, {"Content-Type": "application/json", "User-Agent": "Python/3.9",
                                           "Connection": "keep-alive"})
        self.assertEqual(request.body, "")

    def test_from_bytes_to_bytes(self):
        """Тестирование полного цикла: to_bytes -> from_bytes"""
        original_request = HttpRequest(
            method="POST",
            host="http://localhost:4010",
            path="/send_sms",
            headers={"Content-Type": "application/json"},
            body='{"sender": "123456789", "recipient": "987654321", "message": "1"}',
            token="dGVzdF9sb2dpbl8xOnRlc3RfcGFzc3dvcmRfMQ=="
        )
        binary_data = original_request.to_bytes()
        restored_request = HttpRequest.from_bytes(binary_data)
        self.assertEqual(original_request.method, restored_request.method)
        self.assertEqual(original_request.path, restored_request.path)
        self.assertEqual(original_request.headers, restored_request.headers)
        self.assertEqual(original_request.body, restored_request.body)


class TestHttpResponse(unittest.TestCase):
    def test_to_bytes(self):
        """Тестирование преобразования HttpResponse в байты."""
        response = HttpResponse(
            status_code=200,
            status_message="OK",
            headers={'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': '*',
                     'Access-Control-Allow-Credentials': 'true', 'Access-Control-Expose-Headers': '*',
                     'Content-type': 'application/json', 'Content-Length': '42',
                     'Date': 'Fri, 28 Feb 2025 18:59:55 GMT', 'Connection': 'keep-alive', 'Keep-Alive': 'timeout=5'},
            body='{"status":"success","message_id":"123456"}',
        )
        expected_bytes = b'HTTP/1.1 200 OK\r\nAccess-Control-Allow-Origin: *\r\nAccess-Control-Allow-Headers: *\r\n' \
                         b'Access-Control-Allow-Credentials: true\r\nAccess-Control-Expose-Headers: *\r\n' \
                         b'Content-type: application/json\r\nContent-Length: 42\r\n' \
                         b'Date: Fri, 28 Feb 2025 18:59:55 GMT\r\nConnection: keep-alive\r\nKeep-Alive: timeout=5' \
                         b'\r\n\r\n{"status":"success","message_id":"123456"}'
        self.assertEqual(response.to_bytes(), expected_bytes)

    def test_from_bytes(self):
        """Тестирование преобразования байтов в HttpResponse."""
        binary_data = (
            b'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nKeep-Alive: timeout=5\r\nContent-Length: 42\r\n\r\n'
            b'{"status":"success","message_id":"123456"}'
        )
        response = HttpResponse.from_bytes(binary_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_message, "OK")
        self.assertEqual(response.headers, {"Content-Type": "application/json", "Keep-Alive": "timeout=5",
                                            "Content-Length": "42"})
        self.assertEqual(response.body, '{"status":"success","message_id":"123456"}')

    def test_from_bytes_to_bytes(self):
        """Тестирование полного цикла: to_bytes -> from_bytes."""
        original_response = HttpResponse(
            status_code=404,
            status_message="Unauthorized",
            headers={'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': '*',
                     'Access-Control-Allow-Credentials': 'true', 'Access-Control-Expose-Headers': '*',
                     'sl-violations': '[{"location":["request"],"severity":"Error","code":401,'
                                      '"message":"Invalid security scheme used"}]',
                     'Content-type': 'application/json', 'Content-Length': '31',
                     'Date': 'Fri, 28 Feb 2025 19:06:32 GMT', 'Connection': 'keep-alive', 'Keep-Alive': 'timeout=5'},
            body='{"error":"Invalid credentials"}',
        )
        binary_data = original_response.to_bytes()
        restored_response = HttpResponse.from_bytes(binary_data)
        self.assertEqual(original_response.status_code, restored_response.status_code)
        self.assertEqual(original_response.status_message, restored_response.status_message)
        self.assertEqual(original_response.headers, restored_response.headers)
        self.assertEqual(original_response.body, restored_response.body)


if __name__ == "__main__":
    unittest.main()

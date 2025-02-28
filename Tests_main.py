import unittest
from unittest.mock import patch, mock_open, MagicMock
from main import load_config, send_request, post_socket


class TestLoadConfig(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data='[section]\nkey = "value"')
    def test_load_config(self, mock_file):
        """Тестирование загрузки конфигурации из TOML файла"""
        expected_config = {"section": {"key": "value"}}
        result = load_config("cnf.toml")
        self.assertEqual(result, expected_config)
        mock_file.assert_called_once_with("cnf.toml", "r")


class TestSendRequest(unittest.TestCase):
    @patch("socket.socket")
    def test_send_request_with_port(self, mock_socket):
        """Тестирование отправки запроса с указанием порта"""
        mock_socket_instance = MagicMock()
        mock_socket.return_value.__enter__.return_value = mock_socket_instance
        mock_socket_instance.recv.return_value = b"HTTP/1.1 200 OK\r\nContent-Length: 0\r\n\r\n"

        host = "http://localhost:4010"
        message = b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n"
        response = send_request(host, message)

        mock_socket_instance.connect.assert_called_once_with(("localhost", 4010))
        mock_socket_instance.send.assert_called_once_with(message)
        mock_socket_instance.recv.assert_called_once_with(2048)
        self.assertEqual(response, b"HTTP/1.1 200 OK\r\nContent-Length: 0\r\n\r\n")

    @patch("socket.socket")
    def test_send_request_without_port(self, mock_socket):
        """Тестирование отправки запроса без указания порта"""
        mock_socket_instance = MagicMock()
        mock_socket.return_value.__enter__.return_value = mock_socket_instance
        mock_socket_instance.recv.return_value = b"HTTP/1.1 200 OK\r\nContent-Length: 0\r\n\r\n"

        host = "http://localhost"
        message = b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n"
        response = send_request(host, message)

        mock_socket_instance.connect.assert_called_once_with(("localhost", 80))
        mock_socket_instance.send.assert_called_once_with(message)
        mock_socket_instance.recv.assert_called_once_with(2048)
        self.assertEqual(response, b"HTTP/1.1 200 OK\r\nContent-Length: 0\r\n\r\n")


class TestPostSocket(unittest.TestCase):
    @patch("main.send_request")
    @patch("main.LOGER.info")
    def test_post_socket(self, mock_logger, mock_send_request):
        """Тестирование отправки сообщения через HTTP-запрос"""
        mock_send_request.return_value = b'HTTP/1.1 200 OK\r\nAccess-Control-Allow-Origin: *\r\n' \
                                         b'Access-Control-Allow-Headers: *\r\nAccess-Control-Allow-Credentials: true' \
                                         b'\r\nAccess-Control-Expose-Headers: *\r\nContent-type: application/json\r\n' \
                                         b'Content-Length: 42\r\nDate: Fri,28 Feb 2025 19:31:11 GMT\r\n' \
                                         b'Connection: keep-alive\r\nKeep-Alive: timeout=5\r\n\r\n' \
                                         b'{"status":"success","message_id":"123456"}'

        host = "http://localhost:4010"
        path = "/send"
        username = "test_login_1"
        password = "test_password_1"
        sender = "123456789"
        recipient = "987654321"
        message = "Hello_World!"

        response = post_socket(host, path, username, password, sender, recipient, message)

        # Проверка вызова send_request
        mock_send_request.assert_called_once()
        args, _ = mock_send_request.call_args
        self.assertEqual(args[0], host)

        # Проверка логгирования
        mock_logger.assert_called_once_with(
            "Ответ от сервиса: HttpResponse(status_code=200, status_message=OK, "
            "headers={'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': '*', "
            "'Access-Control-Allow-Credentials': 'true', 'Access-Control-Expose-Headers': '*', "
            "'Content-type': 'application/json', 'Content-Length': '42', 'Date': 'Fri,28 Feb 2025 19:31:11 GMT', "
            "'Connection': 'keep-alive', 'Keep-Alive': 'timeout=5'}, "
            "body={\"status\":\"success\",\"message_id\":\"123456\"})"
        )
        self.assertEqual(response, '200 OK {"status":"success","message_id":"123456"}')


if __name__ == "__main__":
    unittest.main()

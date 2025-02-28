import base64
import logging

logging.basicConfig(filename='send_sms.log', filemode="a", level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
LOGER = logging.getLogger()


class HttpRequest:
    def __init__(self, method: str, host: str, path: str, headers: dict, body: str = "",
                 username: str = "", password: str = "", token: str = ""):
        self.method = method
        self.host = host
        self.path = path
        self.headers = headers
        self.body = body
        if token:
            self.token = token
        elif not username:  # Если не указан ни токен, ни логин (пароль при этом может отсутствовать)
            LOGER.warning("Отсутсвует логин и токен пользователя")
            self.token = ""
        else:
            self.token = str(base64.encodebytes(f'{username}:{password}'.encode()).strip())[2:-1]

    def to_bytes(self) -> bytes:
        """Преобразует HTTP-запрос в последовательность байт."""
        request_line = f"{self.method} {self.path} HTTP/1.1\r\nHost: {self.host}\r\n"
        if self.token:
            request_line += f"Authorization: Basic {self.token}\r\n"
        headers = "\r\n".join(f"{key}: {value}" for key, value in self.headers.items())
        if self.body:
            headers += f"\r\nContent-Length: {len(self.body)}"
        http_request = f"{request_line}{headers}\r\n\r\n{self.body}"
        return http_request.encode("utf-8")

    @classmethod
    def from_bytes(cls, binary_data: bytes):
        """Преобразует последовательность байт в объект HttpRequest."""
        lines = binary_data.decode("utf-8").split("\r\n")
        method, path, _ = lines[0].split(" ")
        headers = {}
        body = ""
        for line in lines[1:]:
            if not line:
                break
            key, value = line.split(": ", 1)
            headers[key] = value
        token = headers.pop("Authorization").split(' ')[-1]
        host = headers.pop("Host")
        body = "\r\n".join(lines[lines.index("") + 1:])
        return cls(method, host, path, headers, body, token=token)

    def __repr__(self):
        return f"HttpRequest(method={self.method}, host={self.host}, path={self.path}, token = {self.token}, " \
               f"headers={self.headers}, body={self.body})"


class HttpResponse:
    def __init__(self, status_code: int, status_message: str, headers: dict, body: str = ""):
        self.status_code = status_code
        self.status_message = status_message
        self.headers = headers
        self.body = body

    def to_bytes(self) -> bytes:
        """Преобразует HTTP-ответ в последовательность байт."""
        status_line = f"HTTP/1.1 {self.status_code} {self.status_message}\r\n"
        headers = "\r\n".join(f"{key}: {value}" for key, value in self.headers.items())
        if self.body:
            headers += f"\r\nContent-Length: {len(self.body)}"
        http_response = f"{status_line}{headers}\r\n\r\n{self.body}"
        return http_response.encode("utf-8")

    @classmethod
    def from_bytes(cls, binary_data: bytes):
        """Преобразует последовательность байт в объект HttpResponse."""
        data = binary_data.decode("utf-8")
        lines = data.split("\r\n")
        _, status_code, status_message = lines[0].split(" ", 2)
        headers = {}
        body = ""
        for line in lines[1:]:
            if not line:
                break
            key, value = line.split(": ", 1)
            headers[key] = value
        body = "\r\n".join(lines[lines.index("") + 1:])
        return cls(int(status_code), status_message, headers, body)

    def __repr__(self):
        return f"HttpResponse(status_code={self.status_code}, status_message={self.status_message}, " \
               f"headers={self.headers}, body={self.body})"

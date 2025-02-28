import argparse
import socket
import json
import toml
from my_http import HttpRequest, HttpResponse, LOGER


def load_config(file_path: str) -> dict:
    """
    Получает конфигурацию из TOML файла
     :param file_path: Путь до файла
     :return: Словарь с настройками
    """
    with open(file_path, "r") as config_file:
        config = toml.load(config_file)
    return config


def send_request(host: str, message: bytes) -> bytes:
    """
    Отправляет запрос на указанный адрес и возвращающая полученный ответ
     :param host: Адресс формата http://localhost:4010 (если порт не указан, то используется 80)
     :param message: Отправляемый HTTP запрос
    :return: Полученный ответ
    """
    if host.split(':') != -1 and len(host.split(':')) > 2:
        host, port = host.rsplit(':', maxsplit=1)
        port = int(port)
    else:
        port = 80
    if host == "http://localhost":
        host = "localhost"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.send(message)
        return s.recv(2048)


def post_socket(host: str, path: str, username: str, password: str, sender: str, recipient: str, message: str) -> str:
    """
    Отправляет сообщение через HTTP-запрос к указанному сервису
     :param host: Хост сервиса
     :param path: Путь API
     :param username: Имя (логин) пользователя
     :param password: Пароль пользователя
     :param sender: Номер отправителя
     :param recipient: Номер получателя
     :param message: Текст сообщения
     :return: Строка состоящая из кода, статуса и тела ответа
    """
    headers = {
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "User-Agent": "python-requests/3.9"
    }
    body = json.dumps({
        "sender": sender,
        "recipient": recipient,
        "message": message,
    })
    request = HttpRequest("POST", host, path, headers, body, username, password)
    answer = HttpResponse.from_bytes(send_request(host, request.to_bytes()))
    LOGER.info(f"Ответ от сервиса: {answer}")
    return str(answer.status_code) + ' ' + str(answer.status_message) + ' ' + answer.body


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("sender_number", help="Номер отправителя СМС сообщения")
    parser.add_argument("recipient_number", help="Номер получателя СМС сообщения")
    parser.add_argument("text", help="Текст СМС сообщения")
    args = parser.parse_args()

    sender = args.sender_number
    recipient = args.recipient_number
    message = args.text

    LOGER.info(f"Номер отправителя {sender}, номер получателя {recipient}, текст сообщения: '{message}'")

    cnf = load_config("config.tolm")
    host = cnf["sms_service"]["url"]
    path = '/send_sms'
    lgn = cnf["sms_service"]["username"]
    psw = cnf["sms_service"]["password"]

    # На практике логин и пароль в лог файл не пишутся, но в рамках тестового задания - запись будет
    LOGER.info(f"Адресс хоста {host}, путь API {path}, логин {lgn}, пароль {psw}")

    print(post_socket(host, path, lgn, psw, sender, recipient, message))

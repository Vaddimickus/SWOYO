# SWOYO
SWOYO test job

Программа запускается из командной строки коммандой python .\main.py

Параметры запуска программы: 

positional arguments:

  sender_number     Номер отправителя СМС сообщения
  
  recipient_number  Номер получателя СМС сообщения
  
  text              Текст СМС сообщения
  

optional arguments:

  -h, --help        show this help message and exit

URL сервиса, login, password для входа берутся из файла config.tolm, который должен находится в одной директории с main.py.

Логи выполнения программы находятся в файле send_sms.log 

Спецификация API сервиса находится в приложенном файле sms-platform.yaml.

# SWOYO
SWOYO test job

Программа запускается из командной строки коммандой python .\main.py. В файле my_http.py Находятся классы для HTTP запроса и ответа, он должен находится в одной директории с main.py

URL сервиса, login, password для входа берутся из файла config.tolm, который должен находится в одной директории с main.py.

Логи выполнения программы находятся в файле send_sms.log 

Unit тесты для методов HTTP классов находятся в файле Test_my_http.py, для функций из файла main.py в файле Tests_main.py

Спецификация API сервиса находится в приложенном файле sms-platform.yaml, который используется для запуска mock сервиса.

Параметры запуска программы: 

positional arguments:

  sender_number     Номер отправителя СМС сообщения
  
  recipient_number  Номер получателя СМС сообщения
  
  text              Текст СМС сообщения
  

optional arguments:

  -h, --help        show this help message and exit

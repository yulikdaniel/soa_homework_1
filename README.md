**Практика 1 по СОА**

Код для каждого тестера лежит в соответствующей формату папке в папке `testers`. В ней же лежит всё остальное, что нужно этому тестеру (например, схема для протобуфа). В корне лежат все докерфайлы и docker-compose файл, собирающий их всех вместе.

Кроме контейнеров для тестеров создаётся контейнер для прокси-сервера, который пересылает запрос в нужный контейнер или на мультикаст группу всех тестеров.

Тестеры используют общую библиотеку `serializable.py`, которая определяет базовый класс сериализатора/десериализатора и все функции, необходимые для тестирования. Кроме того, они используют сервер `testers/tester_server.py`, который при получении запроса просто вызывает функцию `run_tests` у формата из своего контейнера (который он узнаёт из аргумента командной строки, с которым его запускает докер).

Вот вроде бы и всё.

Инструкции по использованию: из корня папки запустить команду:

`docker-compose pull` - подтягивает картинки всех тестеров

`docker-compose build proxyService`

Затем

`docker-compose up -d nativeTesterService jsonTesterService xmlTesterService protoTesterService avroTesterService yamlTesterService mpackTesterService proxyService`

Для запуска тестов:

`echo -n "ALL" | nc -u localhost 2000`

Вместо `ALL` можно подставить `NATIVE`, `JSON`, `XML`, `PROTO`, `AVRO`, `YAML`, `MPACK`.


Комментарий: при тестировке некоторых форматов (например, протобуфов) я перегрузил дефолтные методы для замерения времени, чтобы не учитывать время, уходящее на смену формата с питоновского словаря на протобуф, а замерять только сериализацию.

XML по какой-то причине расшифровывает числа как строки, поэтому я добавил свой скрипт, который рекурсивно конвертирует словарь обратно в правильный формат.

Для поддержки float мне пришлось дописать своё сравнение словарей с фиксированной точностью, это функция `equal` в `serializable.py`
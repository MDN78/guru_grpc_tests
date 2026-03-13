## GRPC. Клиентская часть и разработка автотестов

### Скачивание протофайлов и генерация клиентской части с pbreflect

Используем библиотеку `pbreflect` инструмент для восстановления протофайлов через reflection api, и генерации python
grpc клиентов
[pbreflect](https://github.com/ValeriyMenshikov/pbreflect)

1. Скачиваем протофайлы приложения `Niffler ` и генерация клиентской части с помощью `pbreflect`:  

```commandline
pbreflect get-protos -h localhost:8092 -o ./protos
```

2. Генерация папки для хранения стабов

```commandline
# Generate client code from proto files
pbreflect generate --proto-dir ./protos --output-dir ./internal/pb --gen-type pbreflect

```
С помощью Postman по локальному адресу `0.0.0.0:8092` можно посмотреть доступные методы

3. Подготовка файлов для тестов.

Проект `Niffler` должен быть запущен в Докере

Написали фикстуру `grpc_client` дл подключения канала

### Логирование запросов

Используем механизм grpc интерцепторов (python grpc interceptor)

[examples](https://github.com/grpc/grpc/blob/master/examples/python/interceptors/default_value/default_value_client_interceptor.py)

1. Реализуем интерцептор в папке interceptors
2. Обновили фикстуру
3. Обновили тесты - на получение всех валют и на обмен
4. Написали интерцептор на Allure и добавили его в grpc_client

### Мокирование с Wiremock: переключение между тестовым и целевым сервисом  



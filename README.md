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
Сервис чтобы wiremock мог работать с grpc
[wiremock](https://github.com/wiremock/grpc-wiremock)  
более старый образ, но работает стабильно, используем его:
[old wiremock](https://github.com/Adven27/grpc-wiremock)

Чтобы сконфигурировать мы должны замаппить запрос с ответом, что ожидаем.
В приложении Niffler уже есть заготовка: `wiremock->grpc->mappings`
И в docker-compose.mock.yml уже используем:
```dockerfile
services:
  currency.niffler.dc:
    container_name: currency.niffler.dc
    image: adven27/grpc-wiremock:latest
    volumes:
      - ./wiremock/grpc:/wiremock                     #stubs
      - ./niffler-grpc-common/src/main/proto:/proto   #proto
    ports:
      - 8888:8888                                     # wiremock port
      - 8092:8092                                     # gRPC port
    environment:
      - GRPC_SERVER_PORT=8092
    networks:
      - niffler-network
```
- скопируем yml файл и маппинги к нам в проект и отдельной фикстурой будем переключаться с реального сервиса на moc
- поправить пути в yml файле и порт
- фикстура по выбору приложения
- конфигурационный файл - pydantic settings + создать фикстуру
# Discord api
API которое частично эмулирует возможности(и добавляет некоторые другие) Discord api

**Стек**:
1. Python 3.12.7 - FastAPI, SqlAlchemy, alembic, pydantic, boto3, websockets
2. Golang 1.23.3 - net/http, database/sql, rubenv/sql-migrate, gorilla/mux
3. PostgreSQL
4. Nginx
5. Docker

# Функции

1. Поиск пользователя по username
2. Загрузка аватарки пользователю по токену(сохраняются в Yandex S3)
3. Регистрация пользователя
4. Регистрация пользователя через YandexID
5. Авторизация пользователя по email + password
6. Авторизация пользователя через YandexID(если пользователь был зарегистрирован с помощью YandexID)
7. Проверка токена через api gateway + nginx
8. Создание переписки(приватной)
9. Получение N колличества сообщений в определенной переписке(приватной)
10. Получение информации о определенной переписке(приватной)
11. Добавление сообщения в определенную переписку(приватную)
12. Получение всех переписок пользователя(приватной)
13. Авторизация через QR код(если пользователь авторизарован на телефоне)
14. Генерация токена авторизации для авторизации через QR код
15. Создание токена с информацией о юзере для авторизации через QR код
16. Авторизация с кодом подтверждения(новое устройство авторизации)

# Установка приложения

1. Соберем приложение в Docker.
```bash 
docker-compose up -d build
```
2. Сделаем миграции в микросервисе пользователей и авторизации(порядок не важен).
```bash
alembic revision --autogenerate -m "migrations name"
````
3. Применим миграции в микросервисе пользователей и авторизации(порядок не важен)
```bash
alembic upgreade head
```
4. Перезапустите микросервис приватного чата(переписки)
```bash
Тк для чата требуется таблица пользователей, а в микросервисе приватного чата миграции автоматические при запуске
```

# Документация к API

### 1. Поиск пользователя по username

```http request
GET /users/user/?username=LedxDelivery
```
### Query параметры
| Параметр   | Тип      | Описание                           |
|:-----------|:---------|:-----------------------------------|
| `username` | `string` | **Обязательно**. Имя пользователя  |

### Заголовки
| Заголовок       | Тип      | Описание                               |
|:----------------|:---------|:---------------------------------------|
| `Authorization` | `string` | **Обязательно**. jwt токен авторизации |

### Ответ
```json
{
  "id": integer,
  "username": string,
  "avatar_url": string | None
}
```
### Статус коды
| Код | Описание                |
|:----|:------------------------|
| 200 | `OK`                    |
| 401 | `Unauthorized`          |
| 404 | `NOT FOUND`             |
| 500 | `INTERNAL SERVER ERROR` |

### 2. Загрузка аватарки пользователю по токену

```http request
PATCH /users/upload-avatar/
```

### Заголовки
| Заголовок       | Тип      | Описание                               |
|:----------------|:---------|:---------------------------------------|
| `Authorization` | `string` | **Обязательно**. jwt токен авторизации |

### Тело запроса
```json
{
  "avatar_file": file
}
```
### Ответ
```json
{
  "Detail": "success"
}
```
### Статус коды
| Код | Описание                |
|:----|:------------------------|
| 200 | `OK`                    |
| 401 | `Unauthorized`          |
| 500 | `INTERNAL SERVER ERROR` |

### 3. Создание ссылки регистрации через YandexID

```http request
GET /auth/yandex_oauth_url/
```
### Ответ
```json
{
  "yandex_url": string
}
```
### Статус коды
| Код | Описание                |
|:----|:------------------------|
| 200 | `OK`                    |
| 500 | `INTERNAL SERVER ERROR` |

### 4. Регистрация пользователя - "host"/auth/register/

```http request
POST /auth/register/
```
### Заголовки
| Заголовок         | Тип      | Описание                                           |
|:------------------|:---------|:---------------------------------------------------|
| `Accept-Language` | `string` | **Не обязательно при условии**.список языко ответа |
| `X-Forwarded-For` | `string` | **Обязательно**. ip адрес клиента                  |

Accept-Language обязателен если не удастся определить страну по заголовку X-Forwarded-For 

### Тело запроса
```json
{
  "username": string,
  "email": string,
  "description": string, // не обязательно
  "status": string, // не обязательно
  "password": string
}
```
### Ответ
```json
{
  "detail": "success"
}
```
### Статус коды
| Код | Описание               |
|:----|:-----------------------|
| 200 | `OK`                   |
| 400 | `BAD REQUEST`          |
| 422 | `Unprocessable Entity` |
| 500 | `INTERNAL SERVER ERROR` |

5. Регистрация пользователя через YandexID

```http request
POST /auth/yandex_oauth_register/?oauth_token=
```
### Query параметры
| Параметр      | Тип      | Описание                                                                        |
|:--------------|:---------|:--------------------------------------------------------------------------------|
| `oauth_token` | `string` | **Обязательно** Oauth токен получаемый при авторизации через эндпоинт в 3 этапе |

### Ответ
```json
{
  "detail": "success"
}
```
### Статус коды
| Код | Описание               |
|:----|:-----------------------|
| 200 | `OK`                   |
| 400 | `BAD REQUEST`          |

### 6. Авторизация пользователя по email + password

```http request
POST /auth/login/
```
### Заголовки
| Заголовок         | Тип      | Описание                                      |
|:------------------|:---------|:----------------------------------------------|
| `X-Forwarded-For` | `string` | **Обязательно при условии**. ip адрес клиента |

X-Forwarded-For обязателен если авторизация происходит с нового устройства

### Тело запроса
```json
{
  "email": string,
  "password": string,
  "client_fingerprint": string
}
```
### Ответ
```json
{
  "token": string,
  "type": "Bearer"
}
```
ИЛИ
```json
{
  "detail": "Confirmation code send to: {string}"
}
```
### Статус коды
| Код | Описание                |
|:----|:------------------------|
| 200 | `OK`                    |
| 400 | `BAD REQUEST`           |
| 404 | `NOT FOUND`             |
| 500 | `INTERNAL SERVER ERROR` |

### 7. Проверка токена через api gateway

```http request
GET /gateway/get-token/
```
### Заголовки
| Заголовок       | Тип      | Описание                               |
|:----------------|:---------|:---------------------------------------|
| `Authorization` | `string` | **Обязательно**. jwt токен авторизации |

### Статус коды
| Код | Описание                |
|:----|:------------------------|
| 200 | `OK`                    |
| 403 | `FORBIDDEN`             |
| 500 | `INTERNAL SERVER ERROR` |

8. Создание приватного чата

```http request
POST /private/start-chat/
```
### Заголовки
| Заголовок       | Тип      | Описание                               |
|:----------------|:---------|:---------------------------------------|
| `Authorization` | `string` | **Обязательно**. jwt токен авторизации |

### Тело запроса
```json
{
  "recipient_id": integer
}
```
### Ответ
```json
{
  "chat_id": integer
}
```
### Статус коды
| Код | Описание                |
|:----|:------------------------|
| 200 | `OK`                    |
| 400 | `BAD REQUEST`           |
| 500 | `INTERNAL SERVER ERROR` |

### 9. Получение N колличества сообщений в приватном чате

```http request
GET /private/"chat_id"/messages?limit=&offset=
```
### Query параметры

| Параметр  | Тип       | Описание                                        |
|:----------|:----------|:------------------------------------------------|
| `chat_id` | `integer` | **Обязательно**. id приватного чата             |
| `limit`   | `integer` | **Обязательно**. колличество сообщений          |
| `offset`  | `integer` | **Обязательно**. срез(лучше оставить пока на 0) |

### Ответ
```json
[{
  "id": integer,
  "text": string,
  "answer": integer,
  "chat_id": integer,
  "message_owner": {
    "id": integer,
    "username": string,
    "avatar_url": string
  }
}]
```
### Статус коды
| Код | Описание                |
|:----|:------------------------|
| 200 | `OK`                    |
| 400 | `BAD REQUEST`           |
| 500 | `INTERNAL SERVER ERROR` |

### 10. Получение информации о приватном чате

```http request
GET /private/"chat_id"/info/
```
### Query параметры
| Параметр  | Тип       | Описание                                        |
|:----------|:----------|:------------------------------------------------|
| `chat_id` | `integer` | **Обязательно**. id приватного чата             |

### Ответ
```json
{
  "id": integer,
  "chat_starter": {
      "id": integer,
      "username": string,
      "avatar_url": string
    },
    "chat_recipient": {
      "id": integer,
      "username": string,
      "avatar_url": string
    }
}
```
### Статус коды
| Код | Описание                |
|:----|:------------------------|
| 200 | `OK`                    |
| 400 | `BAD REQUEST`           |
| 500 | `INTERNAL SERVER ERROR` |

### 11. Добавление сообщения в приватный чат

```http request
POST /private/add-message/"chat_id"/
```
### Query параметры
| Параметр  | Тип       | Описание                                        |
|:----------|:----------|:------------------------------------------------|
| `chat_id` | `integer` | **Обязательно**. id приватного чата             |

### Тело запроса
```json
{
  "text": string
}
```
### Ответ
```json
{
  "detail": "Success add."
}
```
### Статус коды
| Код | Описание                |
|:----|:------------------------|
| 200 | `OK`                    |
| 400 | `BAD REQUEST`           |
| 500 | `INTERNAL SERVER ERROR` |

### 12. Получение всех приватных чатов пользователя

```http request
GET /private/chat-list/
```
### Заголовки
| Заголовок       | Тип      | Описание                               |
|:----------------|:---------|:---------------------------------------|
| `Authorization` | `string` | **Обязательно**. jwt токен авторизации |

### Ответ
```json
[{
  "id": integer
}]
```
### Статус коды
| Код | Описание                |
|:----|:------------------------|
| 200 | `OK`                    |
| 400 | `BAD REQUEST`           |
| 500 | `INTERNAL SERVER ERROR` |

13. Авторизация через QR код

```http request
WEBSOCKET /auth_events/qr_auth/?client_id=&client_ip=&client_type=
```
### Query параметры
| Параметр      | Тип      | Описание                                                              |
|:--------------|:---------|:----------------------------------------------------------------------|
| `client_id`   | `string` | **Обязательно**. fingerprint устройства(является id хаба авторизации) |
| `client_ip`   | `string` | **Обязательно**. ip адрес клиета                                      |
| `client_type` | `string` | **Обязательно**. типо клиента(mb/pc)                                  |

client_id - Создается через js в браузере
client_ip - Определеятся через js в браузере
client_type - Тип клиента передается "pc" в браузере

Клиент генерирует qr код формата
```http request
WEBSOCKET /auth_events/qr_auth/?client_id=&client_ip=&client_type=mb
```
client_id и client_ip передавать те, которые используется для подключение клиента(браузера)

### Опкоды

### 1. heartbeat_ack
### Тело запроса
```json
{
  "op": "heartbeat"
}
```
### Ответ
```json
{
  "op": "heartbeat_ack"
}
```
### 2. pending_ticket
### Тело запроса
```json
{
  "op": "pending_ticket",
  "encrypted_user_payload": string
}
```
### Ответ
```json
{
  "op": "New auth device detected, send confirmation code to: {string}"
}
```
ИЛИ
```json
{
  "op": "Success auth",
  "user_payload": string
}
```
### 3. pending_ticket_confirmation
### Тело запроса
```json
{
  "op": "pending_ticket_confirmation",
  "confirmation_code": string
}
```
### Ответ
```json
{
  "op": "Success auth",
  "user_payload": string
}
```
### Статус коды
| Код  | Описание                |
|:-----|:------------------------|
| 1000 | `NORMAL CLOSURE`        |
| 1006 | `ABNORMAL CLOSURE`      |

### 14. Авторизация через auth_token полученного из qr

```http request
GET /auth/qr_auth/?client_id=
```
### Query параметры
| Параметр        | Тип      | Описание                                                              |
|:----------------|:---------|:----------------------------------------------------------------------|
| `client_id`     | `string` | **Обязательно**. fingerprint устройства                               |
| `Authorization` | `string` | **Обязательно**. токен полученный после успешной авторизации через qr |

### Ответ
```json
{
  "token": string,
  "type": "Bearer"
}
```
### Статус коды
| Код | Описание                |
|:----|:------------------------|
| 200 | `OK`                    |
| 404 | `NOT FOUND`             |
| 403 | `FORBIDDEN`             |
| 500 | `INTERNAL SERVER ERROR` |

### 15. Создание токена с информацией о юзере(для авторизации через qr)

```http request
GET /auth/encrypt_user_data/
```
### Заголовки
| Заголовок       | Тип      | Описание                               |
|:----------------|:---------|:---------------------------------------|
| `Authorization` | `string` | **Обязательно**. jwt токен авторизации |

### Ответ
```json
{
  "token": string
}
```
### Статус коды
| Код | Описание                |
|:----|:------------------------|
| 200 | `OK`                    |
| 404 | `NOT FOUND`             |
| 403 | `FORBIDDEN`             |
| 500 | `INTERNAL SERVER ERROR` |

### 16. Авторизация с кодом подтверждения

```http request
POST /auth/confirm_device_and_login/
```
### Тело запроса
```json
{
  "email": string,
  "password": string,
  "confirmation_code": string
}
```
### Ответ
```json
{
  "token": string,
  "type": "Bearer"
}
```
### Статус коды
| Код | Описание                |
|:----|:------------------------|
| 200 | `OK`                    |
| 404 | `NOT FOUND`             |
| 500 | `INTERNAL SERVER ERROR` |

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
14. Получение QR кода в S3

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
1. Поиск пользователя по username - "host"/users/user/?username=
```json
{
  "request header": "Authorization",
  "request params": {
    "username":  string
  },
  "response body": [{
      "id": int,
      "username": string,
      "avatar_url": string
    }]
  
}
```
2. Загрузка аватарки пользователю по токену - "host"/users/upload-avatar/
```json
{
  "request headers": ["Authorization", {"Content-Type": "multipart/form-data;"}],
  "request body": {
    "avatar_file": file
  },
  "response body": {"detail": "success"}
}
```
3. Создание ссылки регистрации через YandexID -"host"/auth/yandex_oauth_url/
```json
{
  "response body": {"yandex_url": string}
}
```
4. Регистрация пользователя - "host"/auth/register/
```json
{
  "request header": "Accept-Language", // не обязательно
  "request body": {
      "username": string,
      "email": string,
      "description": string, // не обязательно
      "status": string, // не обязательно
      "password": string
  },
  "response body": {"detail": "success"}
}
```
5. Регистрация пользователя через YandexID - "host"/auth/yandex_oauth_register/?oauth_token=
```json
{
  "request header": "Accept-Language", // не обязательно
  "request params": {
    "oauth_token":  string
  },
  "response body": {"detail": "success"}
}
```
6. Авторизация пользователя по email + password - "host"/auth/login/
```json
{
  "request body": {
    "email":  string,
  "password":  string
  },
  "response body": {"token": string, "type": "Bearer"}
}
```
7. Проверка токена через api gateway + nginx - "host"/gateway/get-token/
```json
{
  "request header": "Authorization"
}
```
8. Создание переписки - "host"/private/start-chat/
```json
{
  "request header": "Authorization",
  "request body": {
    "recipient_id":  int,
    "text":  string // не обязательно
  },
  "response body": {"chat_id": integer}
}
```
9. Получение N колличества сообщений в определенной переписке - "host"/private/"chat_id"/messages?limit=&offset=

```json
{
  "request header": "Authorization",
  "request path params": {
    "chat_id": int
  },
  "request params": {
    "limit": integer,
    "offset": integer
  },
  "response body": [{
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
}
```
10. Получение информации о определенной переписке - "host"/private/"chat_id"/info/

```json
{
  "request header": "Authorization",
  "request path params": {
    "chat_id": int
  },
  "response body": {
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
}
```
11. Добавление сообщения в определенную переписку - "host"/private/add-message/"chat_id"/
```json
{
  "request header": "Authorization",
  "request path params": {
    "chat_id": int
  },
  "request body": {
    "text": string,
    "message_answer_id": int // не обязательно
  },
  "response body": {
    "detail": "Success add."
    }
}
```
12. Получение всех переписок пользователя - "host"/private/chat-list/

```json
{
  "request header": "Authorization",
  "response body": [
    {
      "id":integer
    }
  ]
}
```
13. Авторизация через QR код(если пользователь авторизарован на телефоне) - ws://"host"/auth_events/qr_auth/?access_token=
    (Реализовано через websocket)
```json
{
  "request query params": {
    "access_token": string // Токен из заголовка Authorization
  },
  "request body": {
    "op": int // Ожидает получить id юзера из access_token
  },
  "response body" {
    "op": string
  }
}
```
Образно возьмем такой порядок действий:

1. Юзер отсканил через приложение QR
2. Приложение взяло url из QR и подставило туда токен
3. У юзера появляется плашка (войти или не входить)
4. Если юзер жмет **"войти"**, то приложение отправляет его Id и он получает свой auth_token(идет разрыв соединения по websocket)
5. Клиент(на пк(сайт)) совершает запрос с этим auth_token на эндпоинт авторизации по qr коду
6. Клиент получает jwt Токен
7. Если юзер жмет **"Не входить"**, то приложение разрывает соединение

(Может потом уберу auth_token и сделаю чисто через jwt токен)

14. Авторизация через auth_token - "host"/auth/qr_auth/?auth_token=
    (Реализовано через websocket)
```json
{
  "request query params": {
    "auth_token": string // токен полученый из этапа 13
  },
  "response body": {"token": string, "type": "Bearer"}
}
```
# Discord api
API которое частично эмулирует возможности(и добавляет некоторые другие) Discord api

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

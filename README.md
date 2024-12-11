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
12. Получение пользователей состоящих в переписке(приватной)

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

# Документация к API(из Postman)

```json
{
	"info": {
		"_postman_id": "35e7a968-9bc5-404c-98d8-78743b4880ae",
		"name": "Discord api",
		"description": "**Описание:**\n\nApi которое частично эмулирует дискорд\n\n**Написано на:**  \n1\\. Python 3.12.7\n\n2.Golang 1.23.3\n\n**Веб-сервер** - Nginx\n\n**Контейнеризация** - Docker + docker-compose",
		"schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
		"_exporter_id": "24868696"
	},
	"item": [
		{
			"name": "nginx",
			"item": [
				{
					"name": "users",
					"item": [
						{
							"name": "find user",
							"request": {
								"method": "GET",
								"header": [
									{
										"key": "Authorization",
										"value": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozLCJ1c2VyX2VtYWlsIjoiUEVTVElMWUB5YW5kZXgucnUiLCJyYW5kb20iOlsiMiIsIk8iLCJxIiwiISIsIjUiLCJSIiwiLSIsIl8iLCJlIiwiSSJdfQ.HkOBm6PKwMT2A-1w1XuXJuyPFrOy_Kmc_n_3iV0AKe4",
										"type": "text"
									}
								],
								"url": {
									"raw": "http://localhost:8881/users/user/?username=PESTILY",
									"protocol": "http",
									"host": [
										"localhost"
									],
									"port": "8881",
									"path": [
										"users",
										"user",
										""
									],
									"query": [
										{
											"key": "username",
											"value": "PESTILY"
										}
									]
								},
								"description": "Поиск пользователя по username"
							},
							"response": []
						},
						{
							"name": "upload avatar",
							"request": {
								"method": "PATCH",
								"header": [
									{
										"key": "Authorization",
										"value": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VyX2VtYWlsIjoibGVkeEBnbWFpbC5jb20iLCJyYW5kb20iOlsiciIsImgiLCIjIiwiQiIsImYiLCJhIiwiVCIsIk0iLCI9IiwiXG4iXX0.B6317YxsJk8Vb-1bsARpFpN9js-zLSPING_5LXg9mTQ",
										"type": "text"
									}
								],
								"body": {
									"mode": "formdata",
									"formdata": [
										{
											"key": "avatar_file",
											"type": "file",
											"src": []
										}
									]
								},
								"url": {
									"raw": "http://localhost:8881/users/upload-avatar/",
									"protocol": "http",
									"host": [
										"localhost"
									],
									"port": "8881",
									"path": [
										"users",
										"upload-avatar",
										""
									]
								},
								"description": "Эндпоинт для загрузки аватарки пользователю"
							},
							"response": []
						}
					],
					"description": "Эндпоинты в микросервисе пользователей"
				},
				{
					"name": "authorization",
					"item": [
						{
							"name": "register",
							"request": {
								"method": "POST",
								"header": [
									{
										"key": "Accept-Language",
										"value": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
										"type": "text"
									}
								],
								"body": {
									"mode": "raw",
									"raw": "{\r\n  \"username\": \"LedxDelivery\",\r\n  \"email\": \"ledx@gmail.com\",\r\n  \"description\": \"Cool desc\",\r\n  \"status\": \"golang <3\",\r\n  \"password\": \"testpassword\"\r\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": {
									"raw": "http://localhost:8881/auth/register/",
									"protocol": "http",
									"host": [
										"localhost"
									],
									"port": "8881",
									"path": [
										"auth",
										"register",
										""
									]
								},
								"description": "Регистрация пользователя в системе\n\nВ Header лучше передавать \"Accept-Language\", он нужен если не получится получить страну пользователя через сторонюю API"
							},
							"response": []
						},
						{
							"name": "current country",
							"request": {
								"method": "GET",
								"header": [
									{
										"key": "Accept-Language",
										"value": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
										"type": "text"
									}
								],
								"url": {
									"raw": "http://localhost:8881/auth/current_ip/",
									"protocol": "http",
									"host": [
										"localhost"
									],
									"port": "8881",
									"path": [
										"auth",
										"current_ip",
										""
									]
								},
								"description": "Тестовый эндпоинт для проверки страны пользователя"
							},
							"response": []
						},
						{
							"name": "login",
							"request": {
								"method": "POST",
								"header": [],
								"body": {
									"mode": "raw",
									"raw": "{\r\n  \"email\": \"ledx@gmail.com\",\r\n  \"password\": \"testpassword\"  \r\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": {
									"raw": "http://localhost:8881/auth/login/",
									"protocol": "http",
									"host": [
										"localhost"
									],
									"port": "8881",
									"path": [
										"auth",
										"login",
										""
									]
								},
								"description": "Авторизация для получения jwt токена"
							},
							"response": []
						},
						{
							"name": "get yandex  oauth url",
							"request": {
								"method": "GET",
								"header": [],
								"url": {
									"raw": "http://localhost:8881/auth/yandex_oauth_url/",
									"protocol": "http",
									"host": [
										"localhost"
									],
									"port": "8881",
									"path": [
										"auth",
										"yandex_oauth_url",
										""
									]
								},
								"description": "Генерация ссылки для авторизации через YandexID"
							},
							"response": []
						},
						{
							"name": "register by yandex oauth",
							"request": {
								"method": "POST",
								"header": [
									{
										"key": "Accept-Language",
										"value": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
										"type": "text"
									}
								],
								"url": {
									"raw": "http://localhost:8881/auth/yandex_oauth_register/?oauth_token=",
									"protocol": "http",
									"host": [
										"localhost"
									],
									"port": "8881",
									"path": [
										"auth",
										"yandex_oauth_register",
										""
									],
									"query": [
										{
											"key": "oauth_token",
											"value": ""
										}
									]
								},
								"description": "Регистрация пользователя в системе через Yandex ID\n\nВ Header лучше передавать \"Accept-Language\", он нужен если не получится получить страну пользователя через сторонюю API"
							},
							"response": []
						},
						{
							"name": "login by yandex oauth",
							"request": {
								"method": "POST",
								"header": [],
								"url": {
									"raw": "http://localhost:8881/auth/login_yandex/?oauth_token=",
									"protocol": "http",
									"host": [
										"localhost"
									],
									"port": "8881",
									"path": [
										"auth",
										"login_yandex",
										""
									],
									"query": [
										{
											"key": "oauth_token",
											"value": ""
										}
									]
								},
								"description": "Авторизация через Yandex для получения jwt токена\n\n(требует регистрации в системе через Yandex)"
							},
							"response": []
						}
					],
					"description": "Endpoint for authorization microservice"
				},
				{
					"name": "Gateway",
					"item": [
						{
							"name": "Get token",
							"request": {
								"method": "GET",
								"header": [
									{
										"key": "Authorization",
										"value": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo0LCJ1c2VyX2VtYWlsIjoibGVkeEBnbWFpbC5jb20iLCJyYW5kb20iOlsiUCIsInwiLCJKIiwibSIsInIiLCI3IiwiYiIsIjEiLCJJIiwiYiJdfQ.hBgyjKVUQwX0nV01m33sYa3Ynfrna9WF4G8eWg_lfMA",
										"type": "text"
									}
								],
								"url": {
									"raw": "http://localhost:8881/gateway/get-token/",
									"protocol": "http",
									"host": [
										"localhost"
									],
									"port": "8881",
									"path": [
										"gateway",
										"get-token",
										""
									]
								},
								"description": "Эндпоинт проверки токена\n\n(Используется в проксировании Nginx для проверки токенов на нужных эндпоинтах)"
							},
							"response": []
						}
					],
					"description": "Эндпоинты для API шлюза\n\n(Проверки токенов)"
				},
				{
					"name": "private chat",
					"item": [
						{
							"name": "Get N last messages",
							"request": {
								"method": "GET",
								"header": [
									{
										"key": "Authorization",
										"value": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo0LCJ1c2VyX2VtYWlsIjoibGVkeEBnbWFpbC5jb20iLCJyYW5kb20iOlsiaiIsIlxyIiwiWiIsIj8iLCJeIiwiUiIsIikiLCIzIiwiViIsIj0iXX0.z2lR5MKVhk-UixTencpYClHbHeffoi8ef8TVTrg4c28",
										"type": "text"
									}
								],
								"url": {
									"raw": "http://localhost:8881/private/33/messages?limit=1000&offset=0",
									"protocol": "http",
									"host": [
										"localhost"
									],
									"port": "8881",
									"path": [
										"private",
										"33",
										"messages"
									],
									"query": [
										{
											"key": "limit",
											"value": "1000"
										},
										{
											"key": "offset",
											"value": "0"
										}
									]
								},
								"description": "Эндпоинт получения последних N сообщений в нужном чате"
							},
							"response": []
						},
						{
							"name": "Get info about chat",
							"request": {
								"method": "GET",
								"header": [
									{
										"key": "Authorization",
										"value": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo0LCJ1c2VyX2VtYWlsIjoibGVkeEBnbWFpbC5jb20iLCJyYW5kb20iOlsiaiIsIlxyIiwiWiIsIj8iLCJeIiwiUiIsIikiLCIzIiwiViIsIj0iXX0.z2lR5MKVhk-UixTencpYClHbHeffoi8ef8TVTrg4c28",
										"type": "text"
									}
								],
								"url": {
									"raw": "http://localhost:8881/private/30/info/",
									"protocol": "http",
									"host": [
										"localhost"
									],
									"port": "8881",
									"path": [
										"private",
										"30",
										"info",
										""
									],
									"query": [
										{
											"key": "Authorization",
											"value": "",
											"disabled": true
										}
									]
								},
								"description": "Эндпоинт получения информации о чате"
							},
							"response": []
						},
						{
							"name": "add message in chat",
							"request": {
								"method": "POST",
								"header": [
									{
										"key": "Authorization",
										"value": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo0LCJ1c2VyX2VtYWlsIjoibGVkeEBnbWFpbC5jb20iLCJyYW5kb20iOlsiaiIsIlxyIiwiWiIsIj8iLCJeIiwiUiIsIikiLCIzIiwiViIsIj0iXX0.z2lR5MKVhk-UixTencpYClHbHeffoi8ef8TVTrg4c28",
										"type": "text"
									}
								],
								"body": {
									"mode": "raw",
									"raw": "{\r\n    \"text\": \"test6\"\r\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": {
									"raw": "http://localhost:8881/private/add-message/33/",
									"protocol": "http",
									"host": [
										"localhost"
									],
									"port": "8881",
									"path": [
										"private",
										"add-message",
										"33",
										""
									]
								},
								"description": "Эндпоинт добавления сообщения в нужный чат"
							},
							"response": []
						},
						{
							"name": "Start private chat",
							"request": {
								"method": "POST",
								"header": [
									{
										"key": "Authorization",
										"value": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo0LCJ1c2VyX2VtYWlsIjoibGVkeEBnbWFpbC5jb20iLCJyYW5kb20iOlsiaiIsIlxyIiwiWiIsIj8iLCJeIiwiUiIsIikiLCIzIiwiViIsIj0iXX0.z2lR5MKVhk-UixTencpYClHbHeffoi8ef8TVTrg4c28",
										"type": "text"
									}
								],
								"body": {
									"mode": "raw",
									"raw": "{\r\n    \"recipient_id\": 5\r\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": {
									"raw": "http://localhost:8881/private/start-chat/",
									"protocol": "http",
									"host": [
										"localhost"
									],
									"port": "8881",
									"path": [
										"private",
										"start-chat",
										""
									]
								},
								"description": "Эндпоинт создания чата с нужным пользователем\n\nВарианты запроса:\n\n``` json\nrecipient_id: 1\n\n ```\n\n``` json\nrecipient_id: 1\ntext: \"test message\"\n\n ```"
							},
							"response": []
						},
						{
							"name": "Get user chat list",
							"request": {
								"method": "GET",
								"header": [
									{
										"key": "Authorization",
										"value": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo0LCJ1c2VyX2VtYWlsIjoibGVkeEBnbWFpbC5jb20iLCJyYW5kb20iOlsiaiIsIlxyIiwiWiIsIj8iLCJeIiwiUiIsIikiLCIzIiwiViIsIj0iXX0.z2lR5MKVhk-UixTencpYClHbHeffoi8ef8TVTrg4c28",
										"type": "text"
									}
								],
								"url": {
									"raw": "http://localhost:8881/private/chat-list/",
									"protocol": "http",
									"host": [
										"localhost"
									],
									"port": "8881",
									"path": [
										"private",
										"chat-list",
										""
									]
								},
								"description": "Эндпоинт получения списка чатов текущего пользователя"
							},
							"response": []
						}
					],
					"description": "Энндпоинты для микросервиса личных сообщений"
				}
			],
			"description": "Запросы к эндпоинтам через Nginx"
		}
	]
}
```
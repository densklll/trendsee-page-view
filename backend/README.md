# Publication Feed API

Async REST API на FastAPI с JWT-авторизацией, кэшированием публикаций в Redis и хранением в PostgreSQL.

## Стек

- **FastAPI** — async web framework
- **PostgreSQL 16** — основная БД (asyncpg, параметризованные запросы)
- **Redis 7** — кэш «горячих» публикаций (TTL 10 минут)
- **Docker + docker-compose** — контейнеризация

## Структура

```
backend/
├── app/
│   ├── main.py               # Точка входа, lifespan, CORS, роутеры
│   ├── config.py             # Настройки через pydantic-settings / .env
│   ├── database.py           # Пул соединений asyncpg
│   ├── redis.py              # Redis-клиент
│   ├── auth.py               # JWT: создание и декодирование
│   ├── dependencies.py       # DI: get_db, get_cache, get_current_user
│   ├── users/
│   │   ├── router.py         # Эндпоинты /api/users
│   │   ├── schemas.py        # Pydantic-модели
│   │   └── repository.py     # SQL-запросы к таблице users
│   └── publications/
│       ├── router.py         # Эндпоинты /api/publications
│       ├── schemas.py        # Pydantic-модели
│       ├── repository.py     # SQL-запросы к таблице publications
│       └── service.py        # Бизнес-логика + Redis-кэширование
├── migrations/               # SQL-скрипты (docker-entrypoint-initdb.d)
├── Dockerfile
└── requirements.txt
```

## Запуск

```bash
docker compose up --build
```

API: `http://localhost:8000` · Swagger: `http://localhost:8000/docs`

## Эндпоинты

### Health

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/health` | Статус сервиса |

### Пользователи

| Метод | URL | Auth | Описание |
|-------|-----|------|----------|
| POST | `/api/users` | — | Создать пользователя (возвращает JWT) |
| GET | `/api/users/{id}/token` | — | Получить JWT по id |
| PATCH | `/api/users/{id}` | Bearer | Изменить имя (только свой профиль) |
| DELETE | `/api/users/{id}` | Bearer | Удалить пользователя |

### Публикации

| Метод | URL | Auth | Описание |
|-------|-----|------|----------|
| POST | `/api/publications` | Bearer | Создать публикацию |
| GET | `/api/publications/user/{user_id}` | — | Все публикации пользователя |
| GET | `/api/publications/user/{user_id}/feed` | — | Лента с пагинацией (`limit`, `offset`) |
| GET | `/api/publications/{id}` | — | Одна публикация |
| PATCH | `/api/publications/{id}` | Bearer | Изменить публикацию (только автор) |
| DELETE | `/api/publications/{id}` | Bearer | Удалить публикацию (только автор) |

Авторизованные эндпоинты ожидают заголовок:

```
Authorization: Bearer <token>
```

## Кэширование

- При создании публикация сразу попадает в Redis (TTL 600 сек).
- При чтении: есть в Redis → отдаётся мгновенно (`source: "cache"`); нет → запрос в Postgres с задержкой 2 с (`source: "database"`).
- При обновлении кэш обновляется с сохранением оставшегося TTL.
- При удалении публикации или пользователя кэш инвалидируется.

## Примеры (curl)

```bash
# Создать пользователя
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Иван"}'

# Создать публикацию
curl -X POST http://localhost:8000/api/publications \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"title": "Заголовок", "text": "Текст публикации"}'

# Получить ленту
curl "http://localhost:8000/api/publications/user/1/feed?limit=10&offset=0"
```

# TrendSee — Publication Feed (FastAPI + Vue)

[![CI](https://github.com/densklll/trendsee-page-view/actions/workflows/ci.yml/badge.svg)](https://github.com/densklll/trendsee-page-view/actions/workflows/ci.yml)

**Live demo (фронт):** [densklll.github.io/trendsee-page-view](https://densklll.github.io/trendsee-page-view/) — без бэкенда, на мок-данных.

Сервис ленты публикаций с JWT-авторизацией, Redis-кэшированием и Vue-фронтендом по дизайну Figma.

## Быстрый старт

### API + Postgres + Redis в Docker, фронт локально

```bash
docker compose up -d db redis app
```

Подожди ~10 с, проверь: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

В отдельном терминале:

```bash
cd frontend
npm install
npm run dev
```

Открой [http://localhost:5173](http://localhost:5173). Запросы на `/api` уходят на **http://127.0.0.1:8000**.

### Всё в Docker (включая UI)

```bash
docker compose --profile docker-ui up --build
```

UI: [http://localhost:5173](http://localhost:5173) · API: [http://localhost:8000](http://localhost:8000) · Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)

### Сбросить базу (схема + демо-данные заново)

```bash
docker compose down -v
docker compose up -d db redis app
```

## Локальный запуск без Docker (только БД и Redis в контейнере)

```bash
npm run dev:infra          # поднимает db + redis
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

В отдельном терминале: `cd frontend && npm run dev`.

## Структура репозитория

| Путь | Назначение |
|------|------------|
| `backend/` | FastAPI-сервис, см. [backend/README.md](backend/README.md) |
| `frontend/` | Vue 3 SPA, см. [frontend/README.md](frontend/README.md) |
| `docker-compose.yml` | Postgres, Redis, API; фронт — профиль `docker-ui` |
| `postman/` | Коллекция Postman с примерами всех запросов |

## Переменные окружения

| Переменная | По умолчанию | Описание |
|---|---|---|
| `DATABASE_URL` | `postgresql://postgres:postgres@127.0.0.1:5433/publications` | URL Postgres |
| `REDIS_URL` | `redis://127.0.0.1:6380/0` | URL Redis |
| `JWT_SECRET` | `super-secret-key-change-in-production` | Секрет для JWT |
| `VITE_FEED_USER_ID` | `1` | ID пользователя, чью ленту показывает UI |

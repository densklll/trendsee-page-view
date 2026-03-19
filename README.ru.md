<div align="center">

[🇬🇧 English](README.md) | 🇷🇺 Русский

# TrendSee — Лента публикаций

**Fullstack-сервис ленты контента: JWT-авторизация, Redis-кэш и пиксель-perfect Vue-интерфейс**

[![CI](https://github.com/densklll/trendsee-page-view/actions/workflows/ci.yml/badge.svg)](https://github.com/densklll/trendsee-page-view/actions/workflows/ci.yml)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-blue?logo=github)](https://densklll.github.io/trendsee-page-view/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.11x-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Vue 3](https://img.shields.io/badge/Vue-3-42b883?logo=vue.js&logoColor=white)](https://vuejs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178c6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7-dc382d?logo=redis&logoColor=white)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ed?logo=docker&logoColor=white)](https://docs.docker.com/compose/)

**[▶ Открыть Live Demo](https://densklll.github.io/trendsee-page-view/)**

</div>

---

## О проекте

TrendSee — сервис ленты публикаций, вдохновлённый платформами аналитики соцсетей. Бэкенд на **FastAPI** с JWT-авторизацией и Redis-кэшированием, фронтенд на **Vue 3** — реализован pixel-perfect по макету Figma.

При недоступном бэкенде фронтенд автоматически переключается на моковые данные — живое демо на GitHub Pages работает без бэкенда.

## Стек технологий

| Уровень | Технологии |
|---------|-----------|
| **Бэкенд** | Python 3.12, FastAPI, asyncpg |
| **Авторизация** | JWT (PyJWT), Bearer-токены |
| **Кэш** | Redis 7 (ответы ленты) |
| **База данных** | PostgreSQL 16 |
| **Фронтенд** | Vue 3, TypeScript, Vite, Pinia |
| **Иконки** | Phosphor Icons |
| **Dev / Deploy** | Docker Compose, GitHub Actions, GitHub Pages |

## Возможности

- **Постраничная лента** — бесконечный скролл с offset-пагинацией
- **JWT-авторизация** — токены для защищённых эндпоинтов
- **Redis-кэш** — ответы ленты кэшируются, кэш сбрасывается при новой публикации
- **Фолбэк на моки** — 30 реалистичных карточек без бэкенда
- **Pixel-perfect UI** — точное воспроизведение макета Figma: карточки, сайдбар, hero-поиск, модальное окно
- **Swagger UI** — интерактивная документация API на `/docs`
- **Postman-коллекция** — готовые запросы в папке `postman/`
- **CI/CD** — GitHub Actions: сборка Docker-образа, type-check фронта, smoke-test стека, деплой на GitHub Pages при пуше в `main`

## Быстрый старт

### Вариант 1 — Всё в Docker (рекомендуется)

```bash
git clone https://github.com/densklll/trendsee-page-view.git
cd trendsee-page-view
docker compose --profile docker-ui up --build
```

| Сервис | URL |
|--------|-----|
| Фронтенд | http://localhost:5173 |
| API | http://localhost:8000 |
| Swagger | http://localhost:8000/docs |

### Вариант 2 — Бэкенд в Docker, фронт локально

```bash
docker compose up -d db redis app
cd frontend && npm install && npm run dev
```

### Вариант 3 — Полностью локально (без Docker)

```bash
npm run dev:infra   # запускает db + redis

cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# отдельный терминал
cd frontend && npm run dev
```

### Сбросить базу данных

```bash
docker compose down -v && docker compose up -d db redis app
```

## Структура проекта

```
trendsee-page-view/
├── backend/               # FastAPI-приложение
│   ├── app/
│   │   ├── publications/  # роутер, сервис, репозиторий, схемы
│   │   ├── users/         # роутер, репозиторий, схемы
│   │   ├── auth.py        # JWT-хелперы
│   │   ├── config.py      # pydantic-settings
│   │   ├── database.py    # пул asyncpg
│   │   └── redis.py       # Redis-клиент
│   ├── migrations/        # SQL-схема и сид-данные
│   └── Dockerfile
├── frontend/              # Vue 3 SPA
│   └── src/
│       ├── components/    # VideoCard, PublicationModal, SideBar, …
│       ├── views/         # SearchResultsView, VideoDetailView
│       ├── stores/        # Pinia-стор (API + фолбэк на моки)
│       └── api/           # axios-клиент
├── postman/               # Postman-коллекция
├── docker-compose.yml
└── .github/workflows/ci.yml
```

## Переменные окружения

| Переменная | По умолчанию | Описание |
|------------|-------------|----------|
| `DATABASE_URL` | `postgresql://postgres:postgres@127.0.0.1:5433/publications` | Строка подключения к Postgres |
| `REDIS_URL` | `redis://127.0.0.1:6380/0` | Строка подключения к Redis |
| `JWT_SECRET` | `super-secret-key-change-in-production` | Секрет для подписи JWT |
| `VITE_FEED_USER_ID` | `1` | ID пользователя, чью ленту показывает UI |

## API эндпоинты

| Метод | Путь | Авторизация | Описание |
|-------|------|-------------|----------|
| `POST` | `/api/users` | — | Создать пользователя |
| `GET` | `/api/users/{id}/token` | — | Получить JWT-токен |
| `GET` | `/api/publications/user/{id}/feed` | — | Лента публикаций (с кэшем) |
| `GET` | `/api/publications/{id}` | — | Получить публикацию по ID |
| `POST` | `/api/publications` | Bearer | Создать публикацию |
| `GET` | `/health` | — | Healthcheck |

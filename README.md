<div align="center">

🇬🇧 English | [🇷🇺 Русский](README.ru.md)

# TrendSee — Publication Feed

**A full-stack content feed service with JWT auth, Redis caching, and a pixel-perfect Vue UI**

[![CI](https://github.com/densklll/trendsee-page-view/actions/workflows/ci.yml/badge.svg)](https://github.com/densklll/trendsee-page-view/actions/workflows/ci.yml)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-blue?logo=github)](https://densklll.github.io/trendsee-page-view/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.11x-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Vue 3](https://img.shields.io/badge/Vue-3-42b883?logo=vue.js&logoColor=white)](https://vuejs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178c6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7-dc382d?logo=redis&logoColor=white)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ed?logo=docker&logoColor=white)](https://docs.docker.com/compose/)

**[▶ Open Live Demo](https://densklll.github.io/trendsee-page-view/)**

</div>

---

## Overview

TrendSee is a publication feed service inspired by social media analytics platforms. It features a **FastAPI** backend with JWT authentication and Redis-cached feed endpoints, paired with a **Vue 3** single-page application built pixel-perfect from a Figma design.

The frontend falls back to rich mock data automatically when the backend is unavailable — so the live demo on GitHub Pages works out of the box.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.12, FastAPI, asyncpg |
| **Auth** | JWT (PyJWT), Bearer tokens |
| **Cache** | Redis 7 (feed responses) |
| **Database** | PostgreSQL 16 |
| **Frontend** | Vue 3, TypeScript, Vite, Pinia |
| **UI Icons** | Phosphor Icons |
| **Dev / Deploy** | Docker Compose, GitHub Actions, GitHub Pages |

## Features

- **Paginated feed** — infinite scroll with offset-based pagination
- **JWT authentication** — token-based auth for write endpoints
- **Redis caching** — feed responses are cached; cache is invalidated on new publications
- **Mock data fallback** — frontend renders 30 realistic cards when API is unreachable
- **Pixel-perfect UI** — components match the Figma layout: cards, sidebar, hero search, modal overlay
- **Swagger UI** — interactive API docs at `/docs`
- **Postman collection** — ready-to-use collection in `postman/`
- **CI/CD** — GitHub Actions builds backend image, type-checks frontend, runs stack smoke-test, and deploys to GitHub Pages on every push to `main`

## Quick Start

### Option 1 — Everything in Docker (recommended)

```bash
git clone https://github.com/densklll/trendsee-page-view.git
cd trendsee-page-view
docker compose --profile docker-ui up --build
```

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| API | http://localhost:8000 |
| Swagger | http://localhost:8000/docs |

### Option 2 — Backend in Docker, frontend locally

```bash
docker compose up -d db redis app
cd frontend && npm install && npm run dev
```

### Option 3 — Fully local (no Docker)

```bash
npm run dev:infra   # starts db + redis

cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# separate terminal
cd frontend && npm run dev
```

### Reset database

```bash
docker compose down -v && docker compose up -d db redis app
```

## Project Structure

```
trendsee-page-view/
├── backend/               # FastAPI app
│   ├── app/
│   │   ├── publications/  # feed router, service, repository, schemas
│   │   ├── users/         # user router, repository, schemas
│   │   ├── auth.py        # JWT helpers
│   │   ├── config.py      # pydantic-settings
│   │   ├── database.py    # asyncpg pool
│   │   └── redis.py       # Redis client
│   ├── migrations/        # SQL schema + seed data
│   └── Dockerfile
├── frontend/              # Vue 3 SPA
│   └── src/
│       ├── components/    # VideoCard, PublicationModal, SideBar, …
│       ├── views/         # SearchResultsView, VideoDetailView
│       ├── stores/        # Pinia store (API + mock fallback)
│       └── api/           # axios client
├── postman/               # Postman collection
├── docker-compose.yml
└── .github/workflows/ci.yml
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `postgresql://postgres:postgres@127.0.0.1:5433/publications` | Postgres connection string |
| `REDIS_URL` | `redis://127.0.0.1:6380/0` | Redis connection string |
| `JWT_SECRET` | `super-secret-key-change-in-production` | JWT signing secret |
| `VITE_FEED_USER_ID` | `1` | User ID whose feed the UI displays |

## API Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `POST` | `/api/users` | — | Create user |
| `GET` | `/api/users/{id}/token` | — | Get JWT token |
| `GET` | `/api/publications/user/{id}/feed` | — | Get paginated feed (cached) |
| `GET` | `/api/publications/{id}` | — | Get single publication |
| `POST` | `/api/publications` | Bearer | Create publication |
| `GET` | `/health` | — | Health check |

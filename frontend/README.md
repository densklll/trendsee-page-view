# TrendSee Frontend

Vue.js фронтенд для ленты публикаций, подключённый к FastAPI-бэкенду.

## Стек

- **Vue.js 3** (Composition API, `<script setup>`)
- **Vue Router** — роутинг (2 страницы)
- **Pinia** — стейт-менеджмент
- **Axios** — HTTP-клиент
- **Vite** — сборка и dev-сервер
- **TypeScript**

## Страницы

### 1. Результаты поиска (`/`)

Главная лента публикаций по макету Figma:
- **Sidebar** — навигация TrendSee (логотип, меню, тариф, пользователь)
- **Hero** — градиентный баннер с поиском
- **Сетка карточек** — каждая карточка показывает заголовок, краткий текст, дату
- **Infinite scroll** — подгрузка по 10 публикаций при скролле (порог 500px)
- **Модалка** — по клику на карточку, Vue Transition (fade + slide-up), полная информация
- **Счётчик** — «Видео: X из Y» внизу экрана

### 2. Анализ видео (`/video/:id`)

Детальная страница видео по макету Figma:
- Превью видео с бейджами
- Информация о блогере
- Статистика (просмотры, лайки, комментарии, репосты, ER)
- Теги контента
- Транскрибация, суть, структура видео

## Запуск

```bash
cd frontend
cp .env.example .env
# Задайте VITE_FEED_USER_ID — id пользователя с публикациями
npm install
npm run dev
```

Фронтенд будет доступен: `http://localhost:5173`

Прокси `/api`: по умолчанию `http://localhost:8000`, в Docker задаётся `API_PROXY_TARGET` (см. корневой `docker-compose.yml`).

## Структура

```
frontend/
├── src/
│   ├── api/
│   │   └── publications.ts    # API-клиент
│   ├── assets/
│   │   ├── images/             # Изображения из Figma
│   │   └── main.css            # Глобальные стили, CSS-переменные
│   ├── components/
│   │   ├── AppLayout.vue       # Основной layout (sidebar + main area)
│   │   ├── SideBar.vue         # Боковая навигация
│   │   ├── VideoCard.vue       # Карточка публикации
│   │   ├── PublicationModal.vue # Модальное окно с деталями
│   │   └── LoadingSpinner.vue  # Индикатор загрузки
│   ├── router/
│   │   └── index.ts            # Роутинг
│   ├── stores/
│   │   └── publications.ts     # Pinia-стор
│   ├── views/
│   │   ├── SearchResultsView.vue  # Страница 1 — лента
│   │   └── VideoDetailView.vue    # Страница 2 — анализ / деталь публикации
│   ├── App.vue
│   └── main.ts
├── index.html
├── package.json
└── vite.config.ts
```

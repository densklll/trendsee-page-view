# Миграции и начальные данные

SQL-скрипты монтируются в контейнер как `/docker-entrypoint-initdb.d` и выполняются **один раз** при **пустом** data volume (в алфавитном порядке имён файлов).

| Файл | Назначение |
|------|------------|
| `01_schema.sql` | Таблицы `users`, `publications` |
| `02_seed_videos.sql` | Демо-пользователь + 30 публикаций |
| `03_add_cover_asset.sql` | Идемпотентное добавление колонки `cover_asset` |

Пересоздать данные заново:

```bash
docker compose down -v && docker compose up -d db redis app
```

Применить вручную на работающей БД (сотрёт текущие данные):

```bash
docker compose exec -T db psql -U postgres -d publications < backend/migrations/02_seed_videos.sql
```

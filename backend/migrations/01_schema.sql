-- Схема БД (выполняется первым в /docker-entrypoint-initdb.d)
CREATE TABLE IF NOT EXISTS users (
    id         SERIAL PRIMARY KEY,
    name       VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS publications (
    id          SERIAL PRIMARY KEY,
    user_id     INTEGER      NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title       VARCHAR(500) NOT NULL,
    text        TEXT         NOT NULL,
    cover_asset VARCHAR(255),
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_publications_user_id      ON publications(user_id);
CREATE INDEX IF NOT EXISTS idx_publications_created_at   ON publications(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_publications_user_created ON publications(user_id, created_at DESC);

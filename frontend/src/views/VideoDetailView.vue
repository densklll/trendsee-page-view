<template>
  <div class="video-detail">
    <div class="video-detail__toolbar">
      <button type="button" class="video-detail__back" @click="goBack">
        <PhCaretLeft :size="16" color="#171c1f" />
        Назад к ленте
      </button>
    </div>

    <div v-if="loading" class="video-detail__state">
      <LoadingSpinner text="Загрузка публикации…" />
    </div>
    <div v-else-if="error" class="video-detail__state video-detail__state--error">
      <p>{{ error }}</p>
      <button type="button" class="video-detail__retry" @click="load">Повторить</button>
    </div>
    <div v-else-if="pub" class="video-detail__sheet">
      <div class="video-detail__layout">
        <aside class="video-detail__aside">
          <div class="video-detail__thumb">
            <img :src="thumbSrc" alt="" class="video-detail__thumb-img" />
            <div class="video-detail__thumb-badge">
              <img
                class="video-detail__reels"
                src="@/assets/images/reels-social-logo.svg"
                width="16"
                height="16"
                alt=""
              />
              <span>Reels</span>
            </div>
          </div>
          <p class="video-detail__aside-meta">
            <time :datetime="pub.created_at">{{ formatDate(pub.created_at) }}</time>
          </p>
        </aside>

        <div class="video-detail__main">
          <header class="video-detail__header">
            <span class="video-detail__eyebrow">Тема видео</span>
            <h1 class="video-detail__title">{{ pub.title }}</h1>
          </header>

          <section class="video-detail__section">
            <h2 class="video-detail__section-title">Описание</h2>
            <div class="video-detail__prose">{{ pub.text }}</div>
          </section>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { PhCaretLeft } from '@phosphor-icons/vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import type { Publication } from '@/api/publications'
import { fetchPublicationById } from '@/api/publications'
import { publicationCoverUrl } from '@/utils/publicationCover'
import { isAxiosError } from 'axios'
import { usePublicationsStore } from '@/stores/publications'

function axiosErrorDetail(e: unknown): string | null {
  if (!isAxiosError(e)) return null
  const raw = e.response?.data
  if (raw && typeof raw === 'object' && 'detail' in raw) {
    const d = (raw as { detail: unknown }).detail
    if (typeof d === 'string') return d
  }
  return null
}

function isUnreachableApi(e: unknown): boolean {
  if (!isAxiosError(e)) return false
  if (e.response) return false
  if (e.code === 'ERR_NETWORK') return true
  if ((e as Error).message === 'Network Error') return true
  return false
}

const route = useRoute()
const router = useRouter()

const pub = ref<Publication | null>(null)
const loading = ref(true)
const error = ref<string | null>(null)

const thumbSrc = computed(() =>
  pub.value ? publicationCoverUrl(pub.value.cover_asset, pub.value.id) : publicationCoverUrl(null, 0)
)

const idParam = computed(() => Number(route.params.id))

const pubStore = usePublicationsStore()

function publicationFromHistory(id: number): Publication | null {
  const s = history.state
  if (!s || typeof s !== 'object') return null
  const rec = s as Record<string, unknown>
  const p = rec.publication as Publication | undefined
  if (p && typeof p === 'object' && p.id === id) return p
  return null
}

function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  })
}

function goBack() {
  router.push({ name: 'search' })
}

async function load() {
  loading.value = true
  error.value = null
  const id = idParam.value
  if (!Number.isFinite(id) || id < 1) {
    error.value = 'Некорректный id публикации'
    loading.value = false
    return
  }
  const offline = pubStore.publicationById(id) ?? publicationFromHistory(id)

  const staleImageHint =
    'Если видите 405: пересоберите сервис app — `docker compose build app && docker compose up -d app`.'

  try {
    pub.value = await fetchPublicationById(id)
    error.value = null
  } catch (e) {
    if (offline) {
      pub.value = offline
      error.value = null
    } else {
      pub.value = null
      const status = isAxiosError(e) ? e.response?.status : undefined
      const detail = axiosErrorDetail(e)

      if (isUnreachableApi(e)) {
        error.value =
          'Запрос к API не выполнен (сеть). Поднимите стек (`docker compose up -d db redis app`) или локальный uvicorn; для `npm run dev` во frontend прокси должен смотреть на http://127.0.0.1:8000.'
      } else if (status === 405) {
        error.value = `405 на GET /api/publications/${id}: в образе app старая версия без этого маршрута. ${staleImageHint}`
      } else if (status === 404) {
        error.value = 'Публикация с таким id не найдена в БД.'
      } else if (status === 502) {
        error.value =
          '502 Bad Gateway: Vite не достучался до API. Часто app ещё стартует или не запущен — подождите 10–20 с или выполните `docker compose ps` и `docker compose logs app --tail 50`. Локальный UI без Docker: на хосте должен слушать порт 8000.'
      } else if (status != null && status >= 500) {
        error.value = detail
          ? `Ошибка сервера (${status}): ${detail}`
          : `Ошибка сервера (${status}). Смотрите логи: docker compose logs app --tail 80`
      } else if (status != null && status >= 400) {
        error.value = detail
          ? `Запрос отклонён (${status}): ${detail}`
          : `Запрос отклонён (${status}).`
      } else {
        error.value =
          'Не удалось загрузить публикацию. Откройте вкладку Network в браузере для /api/publications/… и проверьте ответ.'
      }
    }
  } finally {
    loading.value = false
  }
}

onMounted(load)
watch(idParam, () => {
  load()
})
</script>

<style scoped>
.video-detail {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding-bottom: 48px;
}

.video-detail__toolbar {
  display: flex;
  align-items: center;
}

.video-detail__back {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: #fff;
  border: 1px solid #c6ced2;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  color: #171c1f;
  cursor: pointer;
  font-family: inherit;
}

.video-detail__back:hover {
  background: #f8f9fa;
}

.video-detail__state {
  padding: 48px 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  background: #fff;
  border-radius: 16px;
}

.video-detail__state--error {
  color: #bf0031;
}

.video-detail__retry {
  padding: 10px 20px;
  background: #2b31b3;
  color: #fff;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  font-family: inherit;
}

.video-detail__sheet {
  background: #fff;
  border-radius: 16px;
  padding: 24px;
  box-sizing: border-box;
}

.video-detail__layout {
  display: flex;
  gap: 32px;
  align-items: flex-start;
  flex-wrap: wrap;
}

.video-detail__aside {
  width: 216px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.video-detail__thumb {
  position: relative;
  border-radius: 16px;
  overflow: hidden;
  aspect-ratio: 9 / 16;
  background: #e9ecef;
}

.video-detail__thumb-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.video-detail__thumb-badge {
  position: absolute;
  top: 12px;
  left: 12px;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  background: rgba(0, 0, 0, 0.45);
  backdrop-filter: blur(12px);
  border-radius: 8px;
  font-size: 12px;
  font-weight: 500;
  color: #fff;
}

.video-detail__reels {
  display: block;
}

.video-detail__aside-meta {
  margin: 0;
  font-size: 12px;
  font-weight: 500;
  color: #a0adb4;
}

.video-detail__main {
  flex: 1;
  min-width: 240px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.video-detail__header {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.video-detail__eyebrow {
  font-size: 14px;
  font-weight: 500;
  color: #4e616b;
}

.video-detail__title {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
  line-height: 1.2;
  color: #000;
}

.video-detail__section {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.video-detail__section-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #000;
}

.video-detail__prose {
  background: #f4f5f6;
  border-radius: 8px;
  padding: 16px;
  font-size: 15px;
  line-height: 1.6;
  color: #343a40;
  white-space: pre-wrap;
}

@media (max-width: 640px) {
  .video-detail__layout {
    flex-direction: column;
  }

  .video-detail__aside {
    width: 100%;
    max-width: 280px;
  }
}
</style>

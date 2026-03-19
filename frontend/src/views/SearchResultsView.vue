<template>
  <div class="search-page">
    <!-- Purple Hero / Search Area -->
    <div class="hero">
      <div class="hero__bg-overlay"></div>
      <div class="hero__content">
        <button class="hero__back">
          <PhCaretLeft :size="16" color="#fff" />
          Назад
        </button>

        <div class="hero__title-row">
          <h1 class="hero__title">Business history</h1>
          <button class="hero__add-radar">
            <PhPlus :size="16" color="#171C1F" />
            Добавить в радар
            <PhTarget :size="16" color="#171C1F" />
          </button>
          <PhInfo :size="20" color="rgba(255,255,255,0.6)" class="hero__info-icon" />
        </div>

        <div class="hero__recommend">
          <h3 class="hero__recommend-title">Рекомендуем по теме</h3>
          <div class="hero__chips">
            <span class="hero__chip" v-for="chip in chips" :key="chip">{{ chip }}</span>
          </div>
        </div>

        <div class="hero__search-area">
          <h3 class="hero__search-title">Новый поиск</h3>
          <div class="hero__search-row">
            <div class="hero__search-column hero__search-column--keyword">
              <div class="hero__search-input">
                <PhMagnifyingGlass :size="24" color="rgba(255,255,255,0.7)" />
                <input type="text" placeholder="Новый поиск" />
              </div>
              <p class="hero__search-column-hint">
                Введите ключевое слово, а мы найдем для Вас видео
              </p>
            </div>
            <div class="hero__search-column hero__search-column--type">
              <div class="hero__search-dropdown" role="button" tabindex="0">
                <img
                  class="hero__search-reels-icon"
                  src="@/assets/images/reels-social-logo.svg"
                  width="20"
                  height="20"
                  alt=""
                />
                <span class="hero__search-dropdown-label">Reels</span>
                <PhCaretDown :size="24" color="rgba(255,255,255,0.7)" />
              </div>
              <p class="hero__search-column-caption">Тип видео</p>
            </div>
            <div class="hero__search-column hero__search-column--lang">
              <div class="hero__search-lang-dropdown" role="button" tabindex="0">
                <svg class="hero__search-flag" width="24" height="16" viewBox="0 0 24 16" fill="none" aria-hidden="true">
                  <rect width="24" height="16" rx="2" fill="#F0F0F0" />
                  <rect width="24" height="5.33" fill="#fff" />
                  <rect y="5.33" width="24" height="5.34" fill="#0039A6" />
                  <rect y="10.67" width="24" height="5.33" fill="#CE2028" />
                </svg>
                <span class="hero__search-dropdown-label">Русский</span>
                <PhCaretDown :size="24" color="rgba(255,255,255,0.7)" />
              </div>
              <p class="hero__search-column-caption">Язык видео</p>
            </div>
            <div class="hero__search-column hero__search-column--action">
              <button type="button" class="hero__search-btn">Найти</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Результаты: белая подложка на сером фоне страницы (Figma Main / Frame 2131329209 + Content) -->
    <div class="search-page__results-panel">
      <div class="info-section">
        <div class="info-section__title-bar">
          <div class="info-section__title-left">
            <PhMagnifyingGlass :size="24" color="#2B31B3" />
            <h2 class="info-section__title">Business history</h2>
            <button type="button" class="info-section__add-radar">
              <PhPlus :size="16" color="#171c1f" />
              Добавить в радар
              <PhTarget :size="16" color="#171c1f" />
            </button>
            <PhInfo :size="16" color="#A0ADB4" />
          </div>
          <span class="info-section__count">Загружено: {{ store.items.length }} видео</span>
        </div>

        <div class="info-section__banner" v-if="showBanner">
          <span>Ролики собираются напрямую из поиска соц. сети. Все видео из выдачи – актуальны и продвигаются прямо сейчас.</span>
          <button type="button" class="info-section__banner-close" aria-label="Закрыть" @click="showBanner = false">
            <PhX :size="20" color="#2B31B3" />
          </button>
        </div>

        <div class="info-section__filters">
          <button type="button" class="filter-btn filter-btn--outline">
            За все время
            <PhCaretDown :size="16" color="#4e616b" />
          </button>
          <button type="button" class="filter-btn filter-btn--outline">
            По лайкам
            <PhCaretDown :size="16" color="#4e616b" />
          </button>
        </div>
      </div>

      <!-- Card grid -->
      <div class="content-area__grid">
        <VideoCard
          v-for="(pub, idx) in store.items"
          :key="pub.id"
          :publication="pub"
          :card-index="idx"
          @select="openModal"
        />
      </div>
    </div>

    <LoadingSpinner v-if="store.loading" text="Загрузка публикаций…" />

    <!-- Find more button -->
    <button class="find-more-btn" @click="store.loadMore()">
      <PhLightning :size="20" color="#fff" weight="fill" />
      Найти еще ролики
    </button>

    <!-- Counter badge — полукруг синий (скруглённые концы) + серый трек, крутится -->
    <div class="counter-badge" v-if="store.total > 0">
      <div class="counter-badge__loader" aria-hidden="true">
        <svg class="counter-badge__loader-svg" width="24" height="24" viewBox="0 0 24 24">
          <circle
            cx="12"
            cy="12"
            :r="counterLoaderR"
            fill="none"
            stroke="#e8eaeb"
            :stroke-width="counterLoaderStroke"
          />
          <circle
            cx="12"
            cy="12"
            :r="counterLoaderR"
            fill="none"
            stroke="#2b31b3"
            :stroke-width="counterLoaderStroke"
            stroke-linecap="round"
            :stroke-dasharray="counterLoaderDashArray"
            transform="rotate(-90 12 12)"
          />
        </svg>
      </div>
      <span class="counter-badge__label">Видео: {{ store.items.length }} из {{ store.total }}</span>
    </div>

    <PublicationModal :publication="selectedPub" @close="selectedPub = null" />
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'
import {
  PhLightning,
  PhCaretLeft,
  PhCaretDown,
  PhPlus,
  PhTarget,
  PhInfo,
  PhMagnifyingGlass,
  PhX,
} from '@phosphor-icons/vue'
import VideoCard from '@/components/VideoCard.vue'
import PublicationModal from '@/components/PublicationModal.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import { usePublicationsStore } from '@/stores/publications'
import type { Publication } from '@/api/publications'

const store = usePublicationsStore()
const selectedPub = ref<Publication | null>(null)
const showBanner = ref(true)

const counterLoaderR = 8
const counterLoaderStroke = 3
const counterLoaderCirc = 2 * Math.PI * counterLoaderR
const counterLoaderDashArray = `${counterLoaderCirc / 2} ${counterLoaderCirc}`

const chips = ['Базы данных', 'ИИ', 'Чат-боты', 'Программирование', 'Айти', 'Макбук', 'Кофе']

function openModal(pub: Publication) { selectedPub.value = pub }

function handleScroll() {
  const el = document.querySelector('.app-layout__main')
  if (!el) return
  if (el.scrollHeight - el.scrollTop - el.clientHeight < 500 && !store.loading && store.hasMore) {
    store.loadMore()
  }
}

onMounted(() => {
  store.loadMore()
  const el = document.querySelector('.app-layout__main')
  if (el) el.addEventListener('scroll', handleScroll, { passive: true })
  window.addEventListener('scroll', handleScroll, { passive: true })
})
onUnmounted(() => {
  const el = document.querySelector('.app-layout__main')
  if (el) el.removeEventListener('scroll', handleScroll)
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
.search-page { display: flex; flex-direction: column; gap: 16px; width: 100%; padding-bottom: 80px; }

/* Панель результатов: белая карточка на --c-bg (#f4f5f6), как в макете */
.search-page__results-panel {
  background: #fff;
  border-radius: 16px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 100%;
}

/* ===== Hero ===== */
.hero { background: #6F41DE; border-radius: 16px; padding: 24px; position: relative; overflow: hidden; }
.hero__bg-overlay { position: absolute; inset: 0; background-image: url('@/assets/images/hero_bg.jpg'); background-size: cover; background-position: center; opacity: 0.32; }
.hero__content { position: relative; z-index: 1; display: flex; flex-direction: column; gap: 16px; }
.hero__back { display: flex; align-items: center; gap: 8px; padding: 8px 12px; font-size: 12px; font-weight: 600; color: #fff; background: none; border: none; cursor: pointer; width: fit-content; border-radius: 8px; letter-spacing: 0.4px; font-family: inherit; }
.hero__back:hover { background: rgba(255,255,255,0.1); }
.hero__title-row { display: flex; align-items: center; gap: 10px; }
.hero__title { font-size: 24px; font-weight: 700; color: #fff; margin: 0; }
.hero__add-radar { display: flex; align-items: center; gap: 4px; padding: 12px; background: #f4f5f6; border-radius: 12px; font-size: 12px; font-weight: 600; color: #171c1f; border: none; cursor: pointer; font-family: inherit; letter-spacing: 0.4px; line-height: 16px; }
.hero__add-radar:hover { background: #e8eaec; }
.hero__info-icon { cursor: pointer; flex-shrink: 0; }
.hero__recommend { display: flex; flex-direction: column; gap: 12px; }
.hero__recommend-title { font-size: 16px; font-weight: 700; color: #fff; margin: 0; }
.hero__chips { display: flex; flex-wrap: wrap; gap: 8px; }
.hero__chip { display: inline-flex; align-items: center; padding: 8px 12px; background: #fff; border: 1px solid #DEE2E6; border-radius: 12px; font-size: 14px; font-weight: 400; color: #212529; cursor: pointer; }
.hero__chip:hover { background: #f0f0f0; }

/* Search area — структура как Figma node 1:3880: колонки gap 12px, подпись под своим контролом gap 6px */
.hero__search-area { display: flex; flex-direction: column; gap: 10px; }
.hero__search-title { font-size: 16px; font-weight: 700; color: #fff; margin: 0; letter-spacing: 0.15px; }
.hero__search-row { display: flex; align-items: flex-start; flex-wrap: wrap; gap: 12px; }
.hero__search-column { display: flex; flex-direction: column; align-items: stretch; gap: 6px; isolation: isolate; }
.hero__search-column--keyword { flex: 1 1 280px; max-width: 400px; min-width: 0; }
.hero__search-column--type { flex: 0 0 166px; width: 166px; }
.hero__search-column--lang { flex: 0 0 194px; width: 194px; }
.hero__search-column--action { flex: 0 0 133px; width: 133px; }
.hero__search-input { display: flex; align-items: center; gap: 12px; padding: 0 16px; height: 48px; box-sizing: border-box; background: rgba(255,255,255,0.2); border: 1px solid #fff; border-radius: 12px; backdrop-filter: blur(12px); z-index: 2; }
.hero__search-input input { flex: 1; background: none; border: none; outline: none; color: #fff; font-size: 16px; font-weight: 400; font-family: inherit; letter-spacing: 0.15px; min-width: 0; }
.hero__search-input input::placeholder { color: rgba(255,255,255,0.5); }
.hero__search-column-hint { margin: 0; padding: 0 4px; font-size: 14px; line-height: 21px; font-weight: 400; letter-spacing: 0.25px; color: rgba(255,255,255,0.7); z-index: 1; }
.hero__search-column-caption { margin: 0; padding: 0 4px; font-size: 14px; line-height: 20px; font-weight: 400; color: rgba(255,255,255,0.7); z-index: 1; }
.hero__search-reels-icon { flex-shrink: 0; display: block; width: 20px; height: 20px; object-fit: contain; }
.hero__search-dropdown-label { flex: 1; min-width: 0; font-size: 16px; font-weight: 400; line-height: 24px; letter-spacing: 0.15px; color: rgba(255,255,255,0.5); }
.hero__search-dropdown,
.hero__search-lang-dropdown { display: flex; align-items: center; gap: 10px; padding: 12px 16px; min-height: 48px; box-sizing: border-box; background: rgba(255,255,255,0.2); border: 1px solid #fff; border-radius: 12px; backdrop-filter: blur(12px); cursor: pointer; white-space: nowrap; z-index: 2; }
.hero__search-lang-dropdown .hero__search-dropdown-label { flex: 0 1 auto; width: 94px; }
.hero__search-flag { flex-shrink: 0; display: block; border-radius: 2px; }
.hero__search-btn { width: 100%; min-height: 48px; box-sizing: border-box; padding: 12px; background: #f4f5f6; color: #171c1f; border: none; border-radius: 16px; font-size: 16px; font-weight: 600; line-height: 24px; letter-spacing: 0.3px; cursor: pointer; font-family: inherit; white-space: nowrap; }
.hero__search-btn:hover { background: #e8eaec; }

/* ===== Info Section (Figma Frame 2131329209: gap 16px) ===== */
.info-section { display: flex; flex-direction: column; gap: 16px; }
.info-section__title-bar { display: flex; align-items: center; gap: 16px; justify-content: space-between; }
.info-section__title-left { display: flex; align-items: center; gap: 16px; flex: 1; min-width: 0; flex-wrap: wrap; }
.info-section__title { font-size: 20px; font-weight: 600; color: #000; margin: 0; line-height: 24px; letter-spacing: 0.15px; }
.info-section__add-radar { display: flex; align-items: center; gap: 4px; padding: 12px; background: #f4f5f6; border: none; border-radius: 12px; font-size: 12px; font-weight: 600; color: #171c1f; cursor: pointer; font-family: inherit; letter-spacing: 0.4px; line-height: 16px; }
.info-section__add-radar:hover { background: #e8eaec; }
.info-section__count { font-size: 16px; font-weight: 400; line-height: 24px; color: #4e616b; letter-spacing: 0.5px; white-space: nowrap; flex-shrink: 0; }
/* Баннер — Figma Frame 1:3892: Blue Spark/200 + текст brand-medium #2B31B3 */
.info-section__banner {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 16px;
  background: #d5d6f8;
  border-radius: 16px;
  font-size: 14px;
  font-weight: 400;
  line-height: 21px;
  letter-spacing: 0.25px;
  color: #2b31b3;
}
.info-section__banner span { flex: 1; min-width: 0; }
.info-section__banner-close {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  cursor: pointer;
  flex-shrink: 0;
  border-radius: 6px;
  color: #2b31b3;
}
.info-section__banner-close:hover { background: rgba(43, 49, 179, 0.08); }
.info-section__filters { display: flex; align-items: center; gap: 16px; flex-wrap: wrap; }

/* Button Outline — Figma 1:3898: фон белый, обводка #c6ced2, padding 12px, radius 12, высота 40 */
.filter-btn { display: inline-flex; align-items: center; justify-content: center; gap: 4px; min-height: 40px; padding: 12px; box-sizing: border-box; border-radius: 12px; font-size: 12px; font-weight: 600; color: #000; letter-spacing: 0.4px; line-height: 16px; cursor: pointer; font-family: inherit; transition: background 0.15s, border-color 0.15s; }
.filter-btn--outline { background: #fff; border: 1px solid #c6ced2; }
.filter-btn--outline:hover { background: #f8f9fa; border-color: #b5bfc4; }

/* ===== Grid — Figma List 1:3900: шаг 8px (236−228), межрядно 8px; мин. ширина ячейки = карточка 228px */
.content-area__grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(228px, 1fr));
  column-gap: 8px;
  row-gap: 8px;
  width: 100%;
}

/* ===== Bottom buttons ===== */
.find-more-btn { position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%); display: flex; align-items: center; gap: 8px; padding: 12px 24px; background: #2B31B3; color: #fff; border-radius: 16px; font-size: 16px; font-weight: 600; border: none; cursor: pointer; font-family: inherit; z-index: 50; box-shadow: 0 8px 32px rgba(0,0,0,0.2); white-space: nowrap; }
.find-more-btn:hover { background: #2228a0; }

.counter-badge { position: fixed; bottom: 24px; right: 24px; background: rgba(0,0,0,0.6); backdrop-filter: blur(12px); color: #fff; border-radius: 1000px; padding: 16px 24px; display: flex; align-items: center; gap: 10px; z-index: 50; }
.counter-badge__loader {
  flex-shrink: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.counter-badge__loader-svg {
  display: block;
  animation: counter-badge-loader-spin 1s linear infinite;
}

@keyframes counter-badge-loader-spin {
  to {
    transform: rotate(360deg);
  }
}
.counter-badge__label { font-size: 16px; font-weight: 500; line-height: 24px; letter-spacing: 0.5px; color: #fff; }
</style>

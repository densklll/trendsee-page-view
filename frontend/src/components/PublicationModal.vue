<template>
  <Teleport to="body">
    <Transition name="fade">
      <div v-if="publication" class="modal-overlay" @click.self="$emit('close')">
        <Transition name="slide-up">
          <div v-if="publication" class="modal" @click.stop>
            <div class="modal__layout">
              <!-- LEFT COLUMN: Video + Metadata -->
              <div class="modal__left">
                <div class="modal__video">
                  <img :src="thumbSrc" alt="" class="modal__video-img" />
                  <div class="modal__video-badges">
                    <span class="modal__badge">
                      <img class="modal__reels-icon" src="@/assets/images/reels-social-logo.svg" width="16" height="16" alt="" />
                      <span>Reels</span>
                    </span>
                    <span class="modal__badge">
                      <PhFireSimple :size="16" color="#fff" weight="fill" />
                      <span>X10</span>
                    </span>
                  </div>
                  <button type="button" class="modal__video-play" aria-label="Play">
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M5 3l8 5-8 5V3z" fill="#3a4951"/></svg>
                  </button>
                </div>

                <div class="modal__date-row">
                  <time class="modal__date" :datetime="publication.created_at">
                    {{ formatPubDate(publication.created_at) }}
                  </time>
                  <button type="button" class="modal__date-share" aria-label="Поделиться">
                    <PhArrowSquareOut :size="20" color="#343A40" />
                  </button>
                </div>

                <div class="modal__pub-meta">
                  <span class="modal__pub-meta-row">
                    <span class="modal__pub-meta-label">Автор (user_id)</span>
                    <span class="modal__pub-meta-value">{{ publication.user_id }}</span>
                  </span>
                  <span class="modal__pub-meta-row">
                    <span class="modal__pub-meta-label">Обновлено</span>
                    <span class="modal__pub-meta-value">{{ formatPubDate(publication.updated_at) }}</span>
                  </span>
                </div>

                <div class="modal__blogger">
                  <img :src="avatarSrc" alt="" class="modal__blogger-avatar" />
                  <div class="modal__blogger-info">
                    <span class="modal__blogger-name">@blogerich</span>
                    <span class="modal__blogger-followers">384.5K</span>
                  </div>
                  <div class="modal__blogger-icon" aria-hidden="true">
                    <span class="modal__spy-icon">
                      <PhDetective :size="24" color="#333CD3" />
                    </span>
                    <span class="modal__plus-badge">
                      <PhPlus :size="8" color="#333CD3" weight="bold" />
                    </span>
                  </div>
                </div>

                <div class="modal__description">
                  <div class="modal__description-text" :class="{ 'modal__description-text--expanded': descExpanded }">{{ publication.text }}</div>
                  <button type="button" class="modal__description-more" @click="descExpanded = !descExpanded">
                    {{ descExpanded ? 'Скрыть' : 'Ещё' }}
                  </button>
                </div>

                <div class="modal__stats-list">
                  <div class="modal__stat-row" v-for="stat in stats" :key="stat.label">
                    <div class="modal__stat-left">
                      <img
                        v-if="stat.figmaIconSrc"
                        :src="stat.figmaIconSrc"
                        alt=""
                        class="modal__stat-figma-icon"
                        width="16"
                        height="16"
                      />
                      <component
                        v-else-if="stat.icon"
                        :is="stat.icon"
                        :size="16"
                        :color="stat.color"
                        weight="regular"
                      />
                      <span class="modal__stat-label">{{ stat.label }}</span>
                    </div>
                    <span class="modal__stat-value">{{ stat.value }}</span>
                  </div>
                </div>
              </div>

              <!-- RIGHT COLUMN: Analysis Details -->
              <div class="modal__right">
                <!-- Video Info Container (Figma gap 16px) -->
                <div class="modal__video-info">
                  <!-- Header row -->
                  <div class="modal__header">
                    <div class="modal__header-text">
                      <div class="modal__title-group">
                        <span class="modal__topic">Тема видео</span>
                        <h1 class="modal__title">{{ publication.title }}</h1>
                      </div>
                      <div class="modal__meta">
                        <span class="modal__music-chip">
                          <img :src="iconMusic" alt="" class="modal__music-icon" width="16" height="16" />
                          <span>{{ trackLine.track }}</span>
                        </span>
                        <span class="modal__language">
                          <span class="modal__language-label">Язык:</span>
                          <span class="modal__language-value">
                            <span class="modal__flag">{{ trackLine.flag }}</span>
                            <span>{{ trackLine.lang }}</span>
                          </span>
                        </span>
                      </div>
                    </div>
                    <button class="modal__close" @click="$emit('close')">
                      <PhX :size="16" color="#3a4951" />
                    </button>
                  </div>

                  <!-- Tags -->
                  <div class="modal__tags">
                    <span v-for="(tag, ti) in tags" :key="`t-${publication.id}-${ti}`" class="modal__tag" :style="{ background: tag.bg, color: tag.color }">
                      {{ tag.text }}
                    </span>
                  </div>
                </div>

                <div class="modal__hooks">
                <!-- Транскрибация -->
                <div class="modal__section modal__section--transcription">
                  <div class="modal__section-header">
                    <h3 class="modal__section-title">Транскрибация</h3>
                    <div class="modal__section-actions modal__section-actions--transcription">
                      <span class="modal__translated-btn">
                        <PhTranslate :size="16" color="#2B31B3" weight="regular" class="modal__translated-btn-icon" />
                        <span class="modal__translated-btn-text">Переведено</span>
                      </span>
                      <button type="button" class="modal__copy-btn modal__copy-btn--transcription" title="Копировать">
                        <PhCopy :size="16" color="#2B31B3" weight="regular" />
                      </button>
                    </div>
                  </div>
                  <div class="modal__section-content modal__section-content--transcription">
                    <div class="modal__transcription-text">
                      <p class="modal__transcription-main">{{ publication.text }}</p>
                    </div>
                    <button type="button" class="modal__transcription-more">
                      <PhCaretDown :size="16" color="#171C1F" weight="regular" class="modal__transcription-more-icon" />
                      <span class="modal__transcription-more-label">Ещё</span>
                    </button>
                  </div>
                </div>

                <!-- Адаптировать (Figma: 220×, pad 16px, type 18 semibold, иконка 24 из макета) -->
                <button type="button" class="modal__adapt-btn">
                  <img :src="iconAdaptFigma" alt="" class="modal__adapt-icon" width="24" height="24" />
                  Адаптировать
                </button>

                <!-- Суть -->
                <div class="modal__section">
                  <h3 class="modal__section-title">Суть</h3>
                  <div class="modal__section-content modal__section-content--essence">
                    <p>{{ essenceParagraph }}</p>
                  </div>
                </div>

                <!-- Структура (Figma I1:3916;43096:69948) -->
                <div class="modal__section modal__section--structure">
                  <div class="modal__structure-head">
                    <h3 class="modal__section-title modal__structure-heading">Структура</h3>
                  </div>
                  <div class="modal__structure-steps">
                    <div
                      v-for="(step, i) in structureSteps"
                      :key="step.time"
                      class="modal__structure-step"
                    >
                      <div class="modal__structure-meta">
                        <div class="modal__structure-time-row">
                          <img
                            :src="structureClockSrc"
                            alt=""
                            class="modal__structure-clock"
                            width="16"
                            height="16"
                          />
                          <span class="modal__structure-time-label">{{ step.time }}</span>
                        </div>
                        <div class="modal__structure-rail" aria-hidden="true">
                          <span
                            class="modal__structure-rail-seg modal__structure-rail-seg--top"
                            :class="{ 'modal__structure-rail-seg--invisible': i === 0 }"
                          />
                          <img
                            :src="step.dotSrc"
                            alt=""
                            class="modal__structure-dot"
                            width="16"
                            height="16"
                          />
                          <span
                            class="modal__structure-rail-seg modal__structure-rail-seg--bottom"
                            :class="{ 'modal__structure-rail-seg--invisible': i === structureSteps.length - 1 }"
                          />
                        </div>
                      </div>
                      <div class="modal__structure-copy">
                        <p class="modal__structure-step-title">{{ step.title }}</p>
                        <p class="modal__structure-step-desc">{{ step.desc }}</p>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Хуки: один контейнер как Figma I1:3916;43096:69988–69989 -->
                <div class="modal__hooks-wrap">
                  <div class="modal__hooks-list">
                    <div v-for="hook in hooksList" :key="hook.title" class="modal__hooks-item">
                      <div class="modal__hooks-item-head">
                        <h3 class="modal__hooks-item-title">{{ hook.title }}</h3>
                        <button type="button" class="modal__hooks-copy" title="Копировать">
                          <PhCopy :size="16" color="#4e616b" weight="regular" />
                        </button>
                      </div>
                      <p class="modal__hooks-item-text">{{ hook.text }}</p>
                    </div>
                  </div>
                </div>

                <!-- Рабочие приёмы (Figma I1:3916;43096:70007–70011) -->
                <div class="modal__analysis-block">
                  <div class="modal__analysis-block-head">
                    <h3 class="modal__analysis-block-title">Рабочие приемы</h3>
                    <button type="button" class="modal__analysis-copy" title="Копировать">
                      <img :src="iconCopySecondaryFigma" alt="" width="16" height="16" class="modal__analysis-copy-icon" />
                    </button>
                  </div>
                  <div class="modal__techniques-list">
                    <div v-for="group in techniques" :key="group.number" class="modal__technique-group">
                      <ol class="modal__technique-ol" :start="group.number">
                        <li class="modal__technique-ol-item">{{ group.title }}</li>
                      </ol>
                      <div class="modal__technique-entries">
                        <div
                          v-for="(entry, i) in group.entries"
                          :key="i"
                          class="modal__technique-entry"
                        >
                          <p class="modal__technique-line">Приём: {{ entry.technique }}</p>
                          <p class="modal__technique-line">Почему сработало: {{ entry.reason }}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Воронка / Маркетинг (Figma I1:3916;43096:70035–70039) -->
                <div class="modal__analysis-block">
                  <div class="modal__analysis-block-head">
                    <h3 class="modal__analysis-block-title">Воронка / Маркетинг</h3>
                    <button type="button" class="modal__analysis-copy" title="Копировать">
                      <img :src="iconCopySecondaryFigma" alt="" width="16" height="16" class="modal__analysis-copy-icon" />
                    </button>
                  </div>
                  <div class="modal__marketing-steps">
                    <div v-for="item in marketing" :key="item.label" class="modal__marketing-step">
                      <p class="modal__marketing-step-title">{{ item.label }}</p>
                      <div class="modal__marketing-step-body">
                        <p class="modal__marketing-line">Почему сработало: {{ item.reason }}</p>
                      </div>
                    </div>
                  </div>
                </div>
                </div>
              </div>
            </div>
          </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import type { Component } from 'vue'
import {
  PhFireSimple,
  PhHeart,
  PhArrowSquareOut,
  PhX,
  PhCopy,
  PhCaretDown,
  PhTranslate,
  PhEye,
  PhChatCircle,
  PhPaperPlaneTilt,
  PhPlus,
  PhDetective,
} from '@phosphor-icons/vue'
import type { Publication } from '@/api/publications'
import { publicationCoverUrl } from '@/utils/publicationCover'
import avatarImg from '@/assets/images/avatar.png'
import iconErFigma from '@/assets/images/icon-er-figma.svg'
import iconAdaptFigma from '@/assets/images/icon-adapt-figma.svg'
import iconMusic from '@/assets/images/icon-music.svg'
import structureClockFigma from '@/assets/images/structure-clock-figma.svg'
import structureDot1Figma from '@/assets/images/structure-dot-1-figma.png'
import structureDot2Figma from '@/assets/images/structure-dot-2-figma.svg'
import structureDot3Figma from '@/assets/images/structure-dot-3-figma.svg'
import iconCopySecondaryFigma from '@/assets/images/icon-copy-secondary-figma.svg'

type ModalStatRow =
  | { label: string; value: string; color: string; icon: Component; figmaIconSrc?: undefined }
  | { label: string; value: string; figmaIconSrc: string; icon?: undefined; color?: undefined }

const props = defineProps<{ publication: Publication | null }>()
defineEmits<{ close: [] }>()

const descExpanded = ref(false)

watch(() => props.publication, () => { descExpanded.value = false })

const TRACKS = [
  { track: 'Zivert – Credo', lang: 'Русский', flag: '🇷🇺' },
  { track: 'Miyagi & Эндшпиль – I Got Love', lang: 'Русский', flag: '🇷🇺' },
  { track: 'Tyga – Pop It Off', lang: 'Английский', flag: '🇬🇧' },
  { track: 'The Weeknd – Blinding Lights', lang: 'Английский', flag: '🇬🇧' },
  { track: 'Скриптонит – Положение', lang: 'Русский', flag: '🇷🇺' },
  { track: 'Dua Lipa – Levitating', lang: 'Английский', flag: '🇬🇧' },
]

const trackLine = computed(() => {
  const p = props.publication
  const i = p ? (p.id - 1 + p.user_id) % TRACKS.length : 0
  return TRACKS[i]
})

const hooksList = computed(() => {
  const p = props.publication
  if (!p) return []
  const chunks = p.text
    .split(/\n\s*\n/)
    .map((s) => s.trim())
    .filter(Boolean)
  const lines = chunks.length
    ? chunks
    : p.text.split('\n').map((s) => s.trim()).filter(Boolean)
  const titles = ['Открытие', 'Развитие', 'Финал / CTA']
  return lines.slice(0, 3).map((text, i) => ({
    title: titles[i] || 'Фрагмент',
    text: text.length > 320 ? text.slice(0, 317).trim() + '…' : text,
  }))
})

const essenceParagraph = computed(() => {
  const t = props.publication?.text?.trim() ?? ''
  if (!t) return '—'
  const withoutHashtags = t.split(/\n\s*#/)[0].trim()
  const block = withoutHashtags.split(/\n\s*\n/)[0] ?? withoutHashtags
  return block.length > 400 ? block.slice(0, 397).trim() + '…' : block
})

const thumbSrc = computed(() =>
  props.publication
    ? publicationCoverUrl(props.publication.cover_asset, props.publication.id)
    : publicationCoverUrl(null, 0)
)
const avatarSrc = avatarImg
const structureClockSrc = structureClockFigma

const stats: ModalStatRow[] = [
  { label: 'Просмотры', value: '1,2 млн', color: '#333CD3', icon: PhEye },
  { label: 'Лайки', value: '1,2 млн', color: '#FF4E7B', icon: PhHeart },
  { label: 'Комментарии', value: '1,2 млн', color: '#37C500', icon: PhChatCircle },
  { label: 'Репосты', value: '1,2 млн', color: '#E96C00', icon: PhPaperPlaneTilt },
  { label: 'ER', value: '1,2 млн', figmaIconSrc: iconErFigma },
]

const TAG_STYLES = [
  { text: 'Туториал', bg: '#D5D6F8', color: '#2B31B3' },
  { text: 'Энергичное видео', bg: '#E1F7D8', color: '#1E6D00' },
  { text: 'Изи монтаж', bg: '#FFF0CB', color: '#9E3F00' },
  { text: 'Трендовый звук', bg: '#FFECF1', color: '#BF0031' },
  { text: 'Лид магнит', bg: '#FFF0CB', color: '#9E3F00' },
  { text: 'Красота и здоровье', bg: '#D5D6F8', color: '#2B31B3' },
  { text: 'Карьера', bg: '#E1F7D8', color: '#1E6D00' },
  { text: 'Монтаж', bg: '#D5D6F8', color: '#2B31B3' },
]

const tags = computed(() => {
  const id = props.publication?.id ?? 0
  const n = TAG_STYLES.length
  return [0, 1, 2, 3, 4, 5].map((k) => TAG_STYLES[(id + k) % n])
})

const structureSteps = [
  {
    time: '0–3 сек',
    title: 'Шок-сравнение',
    desc: 'Визуальный (Девушка с предметом) + Текст на экране: "Это спасет вашу зиму"',
    dotSrc: structureDot1Figma,
  },
  {
    time: '3–15 сек',
    title: 'Сюжет',
    desc: '[Герой] показывает проблему -> Резкая смена кадра -> Решение',
    dotSrc: structureDot2Figma,
  },
  {
    time: '15–120 сек',
    title: 'Финал / CTA',
    desc: 'Призыв: «Пиши слово «ССЫЛКА» в комменты»',
    dotSrc: structureDot3Figma,
  },
]

const techniques = [
  {
    number: 2,
    title: 'Суть видео',
    entries: [
      {
        technique: '«кому подходит / кому нет» двумя блоками.',
        reason:
          'это формат «диагноз → лечение → решение». Люди сохраняют не эмоции, а инструкцию. И это «обзор», а не философия',
      },
    ],
  },
  {
    number: 3,
    title: 'Монтаж',
    entries: [
      {
        technique:
          'смена планов каждые 1–2 секунды: лицо → продукт крупно → рука (демо) → снова лицо.',
        reason: 'вертикалки смотрят на автопилоте. Частая смена планов держит внимание даже без звука',
      },
      {
        technique:
          'все доказательства — через B-roll вставки на 0.3–0.8 сек (катышки, блеск, этикетка, нанесение.',
        reason: 'речь в кадре быстро утомляет. B-roll делает ощущение «я реально тестировал».',
      },
    ],
  },
  {
    number: 4,
    title: 'Реплики',
    entries: [
      {
        technique: '«триггер доверия» одной фразой: «Я не продаю этот SPF, мне пох, скажу как есть.»',
        reason: 'снимает защиту «мне впаривают».',
      },
      {
        technique: '«вилка выбора» в середине: «Если кожа жирная — делай так. Если сухая — так.»',
        reason: 'персонализация без долгого объяснения = удержание.',
      },
    ],
  },
]

const marketingReasonFigma =
  'зритель узнаёт свой баг мгновенно. Это не «мнение», а физический факт в кадре, мозг цепляется.'

const marketing = [
  { label: 'CTA голос/визуал', reason: marketingReasonFigma },
  { label: 'Тригер', reason: marketingReasonFigma },
  { label: 'Куда ведет', reason: marketingReasonFigma },
  { label: 'Лид-магнит', reason: marketingReasonFigma },
]

function formatPubDate(iso: string): string {
  return new Date(iso).toLocaleDateString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  })
}

watch(
  () => props.publication,
  (val) => {
    if (val) {
      document.body.style.overflow = 'hidden'
    } else {
      document.body.style.overflow = ''
    }
  },
)
</script>

<style scoped>
/* ===== Overlay =====
   Панель прижата вправо и по вертикали на весь экран (без щелей), ~3/4 ширины вьюпорта. */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: stretch;
  justify-content: flex-end;
  z-index: 1000;
  padding: 0;
  box-sizing: border-box;
}

/* ===== Modal Container ===== */
.modal {
  background: #fff;
  width: 75vw;
  flex-shrink: 0;
  align-self: stretch;
  max-height: none;
  height: auto;
  overflow-y: auto;
  overscroll-behavior: none;
  border-radius: 24px 0 0 24px;
  box-shadow: -8px 0 40px rgba(0, 0, 0, 0.12);
  box-sizing: border-box;
}

.modal__layout {
  display: flex;
  gap: 32px;
  padding: 24px;
  min-height: 100%;
}

/* ===== LEFT COLUMN ===== */
.modal__left {
  width: 216px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.modal__video {
  position: relative;
  border-radius: 16px;
  overflow: hidden;
  aspect-ratio: 9 / 16;
  background: #e9ecef;
}

.modal__video-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.modal__video-badges {
  position: absolute;
  top: 12px;
  left: 12px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.modal__badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(16px);
  border-radius: 8px;
  font-size: 12px;
  font-weight: 500;
  color: #fff;
}

.modal__badge span {
  padding-right: 2px;
}

.modal__reels-icon {
  display: block;
  flex-shrink: 0;
  object-fit: contain;
}

.modal__video-play {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 48px;
  height: 48px;
  background: #F8F9FA;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border: none;
}

.modal__date-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 4px 0;
}

.modal__date {
  font-size: 12px;
  font-weight: 500;
  color: #A0ADB4;
  line-height: 1.208em;
  letter-spacing: 0.4px;
}

.modal__date-share {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  padding: 0;
  border: none;
  background: none;
  cursor: pointer;
  flex-shrink: 0;
}

.modal__date-share:hover {
  opacity: 0.75;
}

.modal__pub-meta {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.modal__pub-meta-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  padding: 6px 10px;
  background: #f4f5f6;
  border-radius: 8px;
}

.modal__pub-meta-label {
  font-size: 11px;
  font-weight: 500;
  color: #a0adb4;
  letter-spacing: 0.4px;
}

.modal__pub-meta-value {
  font-size: 12px;
  font-weight: 600;
  color: #343a40;
}

.modal__blogger {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 0;
}

.modal__blogger-avatar {
  width: 40px;
  height: 40px;
  border-radius: 128px;
  object-fit: cover;
  border: 2px solid #fff;
  flex-shrink: 0;
}

.modal__blogger-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
}

.modal__blogger-name {
  font-size: 14px;
  font-weight: 600;
  color: #2B31B3;
  line-height: 1.5em;
}

.modal__blogger-followers {
  font-size: 12px;
  font-weight: 500;
  color: #4E616B;
  line-height: 1.333em;
  letter-spacing: 0.4px;
}

/* Как на главной (VideoCard): детектив 24×24, плюс 12×12, без белого круга */
.modal__blogger-icon {
  position: relative;
  padding: 4px;
  flex-shrink: 0;
  width: 32px;
  height: 32px;
  box-sizing: border-box;
  overflow: visible;
}

.modal__spy-icon {
  position: relative;
  z-index: 1;
  display: flex;
  width: 24px;
  height: 24px;
  align-items: center;
  justify-content: center;
}

.modal__plus-badge {
  position: absolute;
  left: -3px;
  top: 22px;
  z-index: 0;
  width: 12px;
  height: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
}

.modal__description {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.modal__description-text {
  font-size: 12px;
  font-weight: 500;
  color: #343a40;
  line-height: 14.5px;
  letter-spacing: 0.4px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.modal__description-text--expanded {
  display: block;
  overflow: visible;
  white-space: pre-wrap;
  word-break: break-word;
}

.modal__description-more {
  font-size: 12px;
  font-weight: 600;
  color: #171c1f;
  line-height: 16px;
  letter-spacing: 0.4px;
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
  width: fit-content;
  font-family: inherit;
}

.modal__more-btn {
  font-size: 12px;
  font-weight: 600;
  color: #171C1F;
  background: none;
  border: none;
  cursor: pointer;
  width: fit-content;
  padding: 0;
}

.modal__stats-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.modal__stat-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  background: #F4F5F6;
  border-radius: 12px;
  padding: 8px 12px;
}

.modal__stat-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.modal__stat-figma-icon {
  display: block;
  flex-shrink: 0;
  width: 16px;
  height: 16px;
  object-fit: contain;
}

.modal__stat-label {
  font-size: 12px;
  font-weight: 500;
  color: #343A40;
}

.modal__stat-value {
  font-size: 14px;
  font-weight: 500;
  color: #393C4C;
}

/* ===== RIGHT COLUMN ===== */
.modal__right {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 24px;
  min-width: 0;
}

/* Figma Hooks Container (I1:3916;43096:69930): space-400 = 32px между блоками под тегами */
.modal__hooks {
  display: flex;
  flex-direction: column;
  gap: 32px;
  min-width: 0;
}

.modal__header {
  display: flex;
  gap: 10px;
}

.modal__video-info {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.modal__header-text {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.modal__title-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.modal__topic {
  font-size: 14px;
  font-weight: 500;
  color: #4E616B;
}

.modal__title {
  font-size: 24px;
  font-weight: 700;
  color: #000;
  line-height: 1.208em;
  margin: 0;
}

.modal__meta {
  display: flex;
  gap: 16px;
  align-items: center;
  flex-wrap: wrap;
}

.modal__music-chip {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background: #F1F3F5;
  border-radius: 24px;
  padding: 4px 12px 4px 8px;
  font-size: 12px;
  font-weight: 500;
  color: #343A40;
  letter-spacing: 0.4px;
  line-height: 16px;
}

.modal__music-icon {
  display: block;
  flex-shrink: 0;
  width: 16px;
  height: 16px;
  object-fit: contain;
}

.modal__language {
  display: inline-flex;
  align-items: center;
  gap: 12px;
}

.modal__language-label {
  font-size: 14px;
  font-weight: 400;
  color: #4E616B;
  line-height: 21px;
  letter-spacing: 0.25px;
}

.modal__language-value {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 400;
  color: #4E616B;
  line-height: 21px;
  letter-spacing: 0.25px;
}

.modal__flag {
  font-size: 16px;
  line-height: 1;
}

.modal__close {
  width: 32px;
  height: 32px;
  background: #F4F5F6;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  cursor: pointer;
  border: none;
}

.modal__close:hover {
  background: #e8eaec;
}

/* Tags */
.modal__tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.modal__tag {
  display: inline-flex;
  align-items: center;
  padding: 4px 12px;
  border-radius: 1000px;
  font-size: 14px;
  font-weight: 500;
  line-height: 1.5em;
}

/* Sections */
.modal__section {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.modal__section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.modal__section--transcription .modal__section-header {
  gap: 10px;
}

.modal__section-title {
  font-size: 16px;
  font-weight: 600;
  color: #000;
  margin: 0;
}

.modal__section-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* Figma Transcription Label Container (I1:3916;43096:69932): gap 10px; secondary buttons #f4f5f6, radius 12px, pad 8px */
.modal__section-actions--transcription {
  gap: 10px;
}

.modal__translated-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8px;
  background: #f4f5f6;
  border-radius: 12px;
  box-sizing: border-box;
}

.modal__translated-btn-icon {
  flex-shrink: 0;
  display: flex;
}

.modal__translated-btn-text {
  padding: 0 4px;
  font-size: 12px;
  font-weight: 600;
  line-height: 16px;
  letter-spacing: 0.4px;
  color: #2b31b3;
}

.modal__copy-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #F4F5F6;
  border-radius: 8px;
  cursor: pointer;
  border: none;
  transition: background 0.15s;
}

.modal__copy-btn--transcription {
  width: auto;
  height: auto;
  min-width: 0;
  padding: 8px;
  border-radius: 12px;
}

.modal__copy-btn:hover {
  background: #e0e2e4;
}

.modal__section-content {
  background: #F4F5F6;
  border-radius: 8px;
  padding: 16px;
}

/* Figma Transcription Content Container: radius 6, col items-end, gap 12, pt 16 pb 8 px 16 */
.modal__section-content--transcription {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 12px;
  padding: 16px 16px 8px;
  border-radius: 6px;
}

.modal__section-content--essence {
  border-radius: 6px;
}

.modal__transcription-text {
  width: 100%;
  align-self: stretch;
}

.modal__section-content p {
  font-size: 14px;
  font-weight: 400;
  color: #4E616B;
  line-height: 1.6;
  margin: 0 0 8px;
}

.modal__transcription-text p {
  line-height: 21px;
  letter-spacing: 0.25px;
  margin: 0 0 8px;
}

.modal__transcription-main {
  white-space: pre-wrap;
  margin: 0 !important;
}

.modal__transcription-text p:last-child {
  margin-bottom: 0;
}

.modal__section-content p:last-child {
  margin-bottom: 0;
}

/* Figma Button Link «Ещё»: pad 8, radius 12, caret 16 + label */
.modal__transcription-more {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  padding: 8px;
  border: none;
  border-radius: 12px;
  background: transparent;
  cursor: pointer;
  font-family: inherit;
}

.modal__transcription-more:hover {
  background: rgba(0, 0, 0, 0.04);
}

.modal__transcription-more-icon {
  display: flex;
  flex-shrink: 0;
}

.modal__transcription-more-label {
  padding: 0 4px;
  font-size: 12px;
  font-weight: 600;
  line-height: 16px;
  letter-spacing: 0.4px;
  color: #171c1f;
}

/* Adapt button */
.modal__adapt-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  align-self: flex-start;
  gap: 8px;
  width: 220px;
  max-width: 100%;
  box-sizing: border-box;
  padding: 16px;
  background: #2B31B3;
  color: #fff;
  border-radius: 12px;
  font-size: 18px;
  font-weight: 600;
  line-height: 24px;
  letter-spacing: 0.25px;
  border: none;
  cursor: pointer;
  font-family: inherit;
  transition: background 0.15s;
}

.modal__adapt-icon {
  display: block;
  flex-shrink: 0;
  width: 24px;
  height: 24px;
  object-fit: contain;
}

.modal__adapt-btn:hover {
  background: #2228a0;
}

/* Структура — Figma I1:3916;43096:69948–69951 */
.modal__section--structure {
  gap: 8px;
}

.modal__structure-head {
  display: flex;
  align-items: center;
  padding: 4px 0;
  width: 100%;
}

.modal__structure-heading {
  flex: 1;
}

.modal__structure-steps {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.modal__structure-step {
  display: flex;
  gap: 8px;
  align-items: flex-start;
  width: 100%;
}

.modal__structure-meta {
  display: flex;
  gap: 8px;
  align-items: flex-start;
  align-self: stretch;
  flex-shrink: 0;
}

.modal__structure-time-row {
  display: flex;
  flex-direction: row;
  gap: 4px;
  align-items: center;
  justify-content: flex-end;
  width: 96px;
  flex-shrink: 0;
  padding: 10px 0;
  box-sizing: border-box;
}

.modal__structure-clock {
  display: block;
  flex-shrink: 0;
  width: 16px;
  height: 16px;
  object-fit: contain;
}

.modal__structure-time-label {
  font-size: 12px;
  font-weight: 500;
  line-height: 14.5px;
  letter-spacing: 0.4px;
  color: #4e616b;
  white-space: nowrap;
}

.modal__structure-rail {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 24px;
  padding: 0 4px;
  box-sizing: border-box;
  align-self: stretch;
  flex-shrink: 0;
}

.modal__structure-rail-seg {
  width: 1px;
  background: #aeb1f2;
  flex-shrink: 0;
}

.modal__structure-rail-seg--top {
  height: 11px;
}

.modal__structure-rail-seg--bottom {
  flex: 1;
  min-height: 12px;
}

.modal__structure-rail-seg--invisible {
  opacity: 0;
}

.modal__structure-rail-seg--bottom.modal__structure-rail-seg--invisible {
  flex: 0 0 0;
  min-height: 0;
  height: 0;
}

.modal__structure-dot {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
  display: block;
  object-fit: contain;
}

.modal__structure-copy {
  flex: 1;
  min-width: 0;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 8px 0 12px;
  box-sizing: border-box;
}

.modal__structure-step-title {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
  line-height: 21px;
  letter-spacing: 0.1px;
  color: #000;
}

.modal__structure-step-desc {
  margin: 0;
  font-size: 14px;
  font-weight: 400;
  line-height: 21px;
  letter-spacing: 0.25px;
  color: #4e616b;
}

/* Блок хуков — Figma Hooks List Container 69989 */
.modal__hooks-wrap {
  width: 100%;
}

.modal__hooks-list {
  background: #f4f5f6;
  border-radius: 6px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 24px;
  box-sizing: border-box;
}

.modal__hooks-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 100%;
}

.modal__hooks-item-head {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  min-width: 0;
}

.modal__hooks-item-title {
  flex: 1 1 0;
  min-width: 0;
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  line-height: 24px;
  letter-spacing: 0.15px;
  color: #000;
}

.modal__hooks-copy {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 8px;
  background: #f4f5f6;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  font: inherit;
}

.modal__hooks-copy:hover {
  background: #e8eaec;
}

.modal__hooks-item-text {
  margin: 0;
  width: 100%;
  font-size: 14px;
  font-weight: 400;
  line-height: 21px;
  letter-spacing: 0.25px;
  color: #4e616b;
}

/* Рабочие приёмы / Воронка — общая сетка как Figma 70007, 70035 */
.modal__analysis-block {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  gap: 8px;
  min-width: 0;
  width: 100%;
}

.modal__analysis-block-head {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
}

.modal__analysis-block-title {
  flex: 1 1 0;
  min-width: 0;
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  line-height: 24px;
  letter-spacing: 0.15px;
  color: #000;
}

.modal__analysis-copy {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 8px;
  border: none;
  border-radius: 12px;
  background: #f4f5f6;
  cursor: pointer;
  font: inherit;
}

.modal__analysis-copy:hover {
  background: #e8eaec;
}

.modal__analysis-copy-icon {
  display: block;
  width: 16px;
  height: 16px;
  object-fit: contain;
}

/* Techniques List Container: bg secondary, radius 75 (6px), pad 16, gap 24 */
.modal__techniques-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding: 16px;
  background: #f4f5f6;
  border-radius: 6px;
  box-sizing: border-box;
}

.modal__technique-group {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  gap: 8px;
  min-width: 0;
}

/* Явно включаем цифры: в main.css у всех ol стоит list-style: none */
.modal__technique-ol {
  margin: 0;
  padding: 0 0 0 24px;
  list-style: decimal outside;
  font-size: 16px;
  font-weight: 600;
  line-height: 24px;
  letter-spacing: 0.15px;
  color: #000;
}

.modal__technique-ol-item {
  padding-left: 4px;
}

.modal__technique-ol-item::marker {
  font-weight: 600;
}

.modal__technique-entries {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.modal__technique-entry {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.modal__technique-line {
  margin: 0;
  font-size: 14px;
  font-weight: 400;
  line-height: 21px;
  letter-spacing: 0.25px;
  color: #4e616b;
}

/* Marketing Steps Container — те же токены, что Techniques List */
.modal__marketing-steps {
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding: 16px;
  background: #f4f5f6;
  border-radius: 6px;
  box-sizing: border-box;
}

.modal__marketing-step {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  gap: 8px;
  min-width: 0;
}

.modal__marketing-step-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  line-height: 24px;
  letter-spacing: 0.15px;
  color: #000;
}

.modal__marketing-step-body {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.modal__marketing-line {
  margin: 0;
  font-size: 14px;
  font-weight: 400;
  line-height: 21px;
  letter-spacing: 0.25px;
  color: #4e616b;
}

/* ===== Transitions ===== */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
.slide-up-enter-from {
  opacity: 0;
  transform: translateX(30px);
}
.slide-up-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style>

<template>
  <article
    class="card"
    role="button"
    tabindex="0"
    @click="openModal"
    @keydown.enter.prevent="openModal"
  >
    <div class="card__thumb">
      <img :src="thumbSrc" alt="" class="card__thumb-img" />
      <div class="card__thumb-overlay">
        <div class="card__header">
          <div class="card__badges">
            <!-- Category label for first 3 cards -->
            <span v-if="categoryLabel" class="card__category-badge" :style="{ background: categoryLabel.bg }">
              <component :is="categoryLabel.icon" :size="16" color="#fff" weight="fill" />
              <span>{{ categoryLabel.text }}</span>
            </span>
            <span class="card__badge">
              <img class="card__reels-icon" src="@/assets/images/reels-social-logo.svg" width="16" height="16" alt="" />
              <span>Reels</span>
            </span>
            <span class="card__badge">
              <PhFireSimple :size="16" color="#fff" weight="fill" />
              <span>X10</span>
            </span>
          </div>
          <div class="card__actions-top">
            <button class="card__action-btn card__action-btn--heart" :class="{ 'card__action-btn--liked': isFavorite, 'card__action-btn--liking': heartAnimating }" @click.stop="toggleFavorite">
              <PhHeart :size="20" :color="isFavorite ? '#FF4E7B' : '#fff'" :weight="isFavorite ? 'fill' : 'regular'" />
            </button>
            <button type="button" class="card__action-btn" @click.stop="goDetail">
              <PhArrowSquareOut :size="20" color="#fff" />
            </button>
          </div>
        </div>
      </div>
      <div class="card__stats">
        <div class="card__stat">
          <PhEye :size="20" color="#fff" />
          <span>105k</span>
        </div>
        <div class="card__stat">
          <PhHeart :size="20" color="#fff" />
          <span>85k</span>
        </div>
        <div class="card__stat">
          <PhChatCircle :size="20" color="#fff" />
          <span>15k</span>
        </div>
        <div class="card__stat">
          <PhPaperPlaneTilt :size="18" color="#fff" />
          <span>485</span>
        </div>
      </div>
    </div>
    <div class="card__body">
      <div class="card__blogger">
        <img :src="avatarSrc" alt="" class="card__blogger-avatar" />
        <div class="card__blogger-info">
          <span class="card__blogger-name">@blogerich</span>
          <span class="card__blogger-followers">{{ followerText }}</span>
        </div>
        <div class="card__blogger-icon">
          <!-- Figma Bloger Card I1:3869;1120:27248: шпион 24×24, плюс 12×12 absolute left:-3px top:22px -->
          <span class="card__spy-icon">
            <PhDetective :size="24" color="#333CD3" />
          </span>
          <span class="card__plus-badge" aria-hidden="true">
            <PhPlus :size="8" color="#333CD3" weight="bold" />
          </span>
        </div>
      </div>
      <div class="card__description">
        <span>{{ publication.title }}</span>
      </div>
      <div class="card__date">
        <span>{{ formatDate(publication.created_at) }}</span>
      </div>
      <button type="button" class="card__btn-primary" @click.stop="openModal">
        Анализ
      </button>
    </div>
  </article>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import {
  PhHeart,
  PhArrowSquareOut,
  PhEye,
  PhChatCircle,
  PhPaperPlaneTilt,
  PhFireSimple,
  PhPlus,
  PhDetective,
  PhTrophy,
} from '@phosphor-icons/vue'
import type { Publication } from '@/api/publications'
import { publicationCoverUrl } from '@/utils/publicationCover'
import avatarImg from '@/assets/images/avatar.png'

const props = defineProps<{ publication: Publication; cardIndex: number }>()
const emit = defineEmits<{ select: [pub: Publication] }>()

const router = useRouter()

function openModal() {
  emit('select', props.publication)
}

function goDetail() {
  router.push(
    {
      name: 'video-detail',
      params: { id: String(props.publication.id) },
      state: { publication: props.publication },
    } as unknown as Parameters<typeof router.push>[0]
  )
}

const isFavorite = ref(false)
const heartAnimating = ref(false)

function toggleFavorite() {
  if (heartAnimating.value) return
  const willLike = !isFavorite.value
  if (willLike) {
    heartAnimating.value = true
    setTimeout(() => {
      isFavorite.value = true
      heartAnimating.value = false
    }, 600)
  } else {
    isFavorite.value = false
  }
}

const thumbSrc = computed(() =>
  publicationCoverUrl(props.publication.cover_asset, props.cardIndex)
)
const avatarSrc = avatarImg

// Alternate follower text
const followerText = computed(() =>
  props.cardIndex % 3 === 0 ? '10.5K Подписчиков' : '384.5K'
)

// Category labels for first 3 cards
const categoryLabels = [
  { text: 'Просмотры', bg: '#914CFF', icon: PhTrophy },
  { text: 'Лайки', bg: '#FF4E7B', icon: PhTrophy },
  { text: 'Комментарии', bg: '#37C500', icon: PhTrophy },
]
const categoryLabel = computed(() =>
  props.cardIndex < 3 ? categoryLabels[props.cardIndex] : null
)

function formatDate(iso: string): string {
  const d = new Date(iso)
  return d.toLocaleDateString('ru-RU', { day: '2-digit', month: '2-digit', year: 'numeric' })
}
</script>

<style scoped>
.card { width: 100%; min-width: 0; height: 100%; background: var(--c-white); border-radius: 16px; overflow: hidden; display: flex; flex-direction: column; gap: 4px; padding: 4px 4px 8px; box-sizing: border-box; }
.card__thumb { position: relative; width: 100%; height: 346px; overflow: hidden; border-radius: 16px; flex-shrink: 0; }
.card__thumb-img { width: 100%; height: 100%; object-fit: cover; display: block; }
.card__thumb-overlay { position: absolute; inset: 0; padding: 12px; display: flex; flex-direction: column; }
.card__header { display: flex; justify-content: space-between; align-items: flex-start; }
.card__badges { display: flex; flex-direction: column; gap: 6px; align-items: flex-start; }

.card__category-badge { display: inline-flex; align-items: center; gap: 6px; padding: 6px 10px; border-radius: 8px; font-size: 12px; font-weight: 600; color: #fff; }

.card__badge { display: inline-flex; align-items: center; gap: 4px; padding: 4px 6px; background: rgba(0,0,0,0.4); backdrop-filter: blur(16px); border-radius: 8px; font-size: 12px; font-weight: 500; color: #fff; }
.card__badge span { padding-right: 2px; }
.card__reels-icon { display: block; flex-shrink: 0; object-fit: contain; }

.card__actions-top { display: flex; flex-direction: column; gap: 8px; }
.card__action-btn { width: 32px; height: 32px; background: rgba(0,0,0,0.4); backdrop-filter: blur(16px); border-radius: 8px; display: flex; align-items: center; justify-content: center; cursor: pointer; border: none; padding: 0; transition: background 0.15s, transform 0.2s; }
.card__action-btn:hover { background: rgba(0,0,0,0.6); }
.card__action-btn--liked { background: rgba(255,255,255,0.9); }
.card__action-btn--liking { animation: heartSpin 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) forwards; background: rgba(255,255,255,0.9); }

@keyframes heartSpin {
  0%   { transform: scale(1) rotate(0deg); }
  40%  { transform: scale(0.85) rotate(720deg); }
  65%  { transform: scale(0.7) rotate(720deg); }
  85%  { transform: scale(1.15) rotate(720deg); }
  100% { transform: scale(1) rotate(720deg); }
}

.card__stats { position: absolute; bottom: 12px; left: 4px; right: 4px; display: flex; justify-content: space-around; background: rgba(0,0,0,0.3); backdrop-filter: blur(8px); border-radius: 12px; padding: 8px 4px; }
.card__stat { display: flex; flex-direction: column; align-items: center; gap: 4px; color: #fff; font-size: 12px; font-weight: 500; flex: 1; }

.card__body { padding: 0 4px; display: flex; flex-direction: column; gap: 4px; flex: 1; min-height: 0; }
.card__blogger { display: flex; align-items: center; gap: 8px; padding: 4px 0; }
.card__blogger-avatar { width: 40px; height: 40px; border-radius: 128px; object-fit: cover; border: 2px solid #fff; flex-shrink: 0; }
.card__blogger-info { display: flex; flex-direction: column; gap: 4px; flex: 1; min-width: 0; }
.card__blogger-name { font-size: 14px; font-weight: 600; line-height: 1.5em; color: #2B31B3; }
.card__blogger-followers { font-size: 12px; font-weight: 500; line-height: 1.333em; color: #4E616B; }
.card__blogger-icon {
  position: relative;
  padding: 4px;
  flex-shrink: 0;
  width: 32px;
  height: 32px;
  box-sizing: border-box;
  overflow: visible;
}
.card__spy-icon {
  position: relative;
  z-index: 1;
  display: flex;
  width: 24px;
  height: 24px;
  align-items: center;
  justify-content: center;
}
/* Как в Figma: плюс внизу слева, не перекрывает очки; без белого круга в макете */
.card__plus-badge {
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

.card__description { font-size: 12px; font-weight: 500; line-height: 1.208em; color: #4E616B; height: 44px; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; }
.card__date { font-size: 12px; font-weight: 500; color: #A0ADB4; }
.card__btn-primary { display: flex; align-items: center; justify-content: center; padding: 12px; background: #2B31B3; color: #fff; border-radius: 12px; font-size: 12px; font-weight: 600; width: 100%; cursor: pointer; border: none; font-family: inherit; transition: background 0.15s; flex-shrink: 0; }
.card__btn-primary:hover { background: #2228a0; }
</style>

<template>
  <aside class="sidebar" :class="{ 'sidebar--collapsed': collapsed }">
    <div class="sidebar__strip">
    <div class="sidebar__header" :class="{ 'sidebar__header--collapsed': collapsed }">
      <div class="sidebar__logo">
        <svg class="sidebar__logo-icon" width="30" height="23" viewBox="0 0 30 23" fill="none" aria-hidden="true">
          <circle cx="15" cy="11.5" r="10" stroke="#1B1A25" stroke-width="2.5"/>
          <circle cx="15" cy="11.5" r="4" fill="#1B1A25"/>
          <path d="M2 11.5C2 11.5 7 3 15 3s13 8.5 13 8.5S23 20 15 20 2 11.5 2 11.5z" stroke="#1B1A25" stroke-width="2.5" fill="none"/>
        </svg>
        <span class="sidebar__logo-text">trendsee</span>
      </div>
      <span class="sidebar__logo-badge">Beta</span>
      <button type="button" class="sidebar__collapse-btn" :aria-expanded="!collapsed" :aria-label="collapsed ? 'Развернуть меню' : 'Свернуть меню'" @click="collapsed = !collapsed">
        <PhArrowSquareLeft class="sidebar__collapse-icon" :size="16" color="var(--c-text-tertiary)" :class="{ 'sidebar__collapse-icon--flipped': collapsed }" />
      </button>
    </div>

    <div class="sidebar__body">
      <div class="sidebar__scroll-shell">
        <div class="sidebar__scroll-area">
          <nav class="sidebar__nav">
          <div class="sidebar__section sidebar__section--search">
            <div class="sidebar__section-header">Поиск контента</div>
            <ul class="sidebar__list">
              <li v-for="item in searchItems" :key="item.label" class="sidebar__item" :class="{ 'sidebar__item--active': item.active }">
                <span class="sidebar__item-icon">
                  <component :is="item.icon" :size="24" weight="thin" :color="item.iconColor" />
                </span>
                <span class="sidebar__item-label">{{ item.label }}</span>
                <span v-if="item.badge" class="sidebar__item-badge">{{ item.badge }}</span>
              </li>
            </ul>
          </div>

          <div class="sidebar__section sidebar__section--social">
            <div class="sidebar__section-header">Работа с соцсетями</div>
            <ul class="sidebar__list">
              <li v-for="item in socialItems" :key="item.label" class="sidebar__item">
                <span class="sidebar__item-icon">
                  <component :is="item.icon" :size="24" weight="thin" :color="item.iconColor" />
                </span>
                <span class="sidebar__item-label">{{ item.label }}</span>
              </li>
            </ul>
          </div>

          <div class="sidebar__section sidebar__section--tools">
            <div class="sidebar__section-header">Инструменты</div>
            <ul class="sidebar__list">
              <li v-for="item in toolItems" :key="item.label" class="sidebar__item">
                <span class="sidebar__item-icon">
                  <component :is="item.icon" :size="24" weight="thin" :color="item.iconColor" />
                </span>
                <span class="sidebar__item-label">{{ item.label }}</span>
                <span v-if="item.soon" class="sidebar__item-soon">Скоро</span>
              </li>
            </ul>
          </div>

          <div class="sidebar__section sidebar__section--ideas">
            <div class="sidebar__section-header">Идеи</div>
            <ul class="sidebar__list">
              <li v-for="item in ideasItems" :key="item.label" class="sidebar__item">
                <span class="sidebar__item-icon">
                  <component :is="item.icon" :size="24" weight="thin" :color="item.iconColor" />
                </span>
                <span class="sidebar__item-label">{{ item.label }}</span>
                <span v-if="item.soon" class="sidebar__item-soon">Скоро</span>
              </li>
            </ul>
          </div>

          <div class="sidebar__section sidebar__section--more">
            <div class="sidebar__section-header">Еще</div>
            <ul class="sidebar__list">
              <li v-for="item in moreItems" :key="item.label" class="sidebar__item">
                <span class="sidebar__item-icon">
                  <component :is="item.icon" :size="24" weight="thin" :color="item.iconColor" />
                </span>
                <span class="sidebar__item-label">{{ item.label }}</span>
                <span v-if="item.soon" class="sidebar__item-soon">Скоро</span>
              </li>
            </ul>
          </div>
          </nav>
        </div>
        <div class="sidebar__scroll-fade" aria-hidden="true" />
      </div>

      <div class="sidebar__bottom">
      <div class="sidebar__tokens-card" :class="{ 'sidebar__tokens-card--creative-open': creativeExpanded }">
        <div class="sidebar__tokens-top">
          <div class="sidebar__tokens-row">
            <PhFire :size="20" color="#FF4E7B" weight="fill" />
            <span class="sidebar__tokens-label">Токены</span>
            <span class="sidebar__tokens-value">1 245 / 4 497</span>
          </div>
          <div class="sidebar__tokens-bar">
            <div class="sidebar__tokens-fill"></div>
          </div>
        </div>
        <div class="sidebar__tokens-footer">
          <div class="sidebar__tokens-footer-stack" :class="{ 'sidebar__tokens-footer-stack--open': creativeExpanded }">
            <div class="sidebar__tokens-footer-pane sidebar__tokens-footer-pane--creative">
              <button
                type="button"
                class="sidebar__creative"
                aria-expanded="false"
                @click="creativeExpanded = true"
              >
                <span class="sidebar__creative-label">Creative +</span>
                <PhCaretRight class="sidebar__creative-icon" :size="20" color="var(--c-text-tertiary)" weight="regular" />
              </button>
            </div>
            <div class="sidebar__tokens-footer-pane sidebar__tokens-footer-pane--trial">
              <button
                type="button"
                class="sidebar__trial-head"
                aria-expanded="true"
                aria-label="Свернуть"
                @click="creativeExpanded = false"
              >
                <span class="sidebar__trial-label">Пробная версия</span>
              </button>
              <button type="button" class="sidebar__upgrade-btn">Улучшить подписку</button>
            </div>
          </div>
        </div>
      </div>

      <div class="sidebar__user">
        <div class="sidebar__user-avatar">
          <img :src="avatarSrc" alt="" class="sidebar__user-avatar-img" />
        </div>
        <div class="sidebar__user-info">
          <span class="sidebar__user-name">Александра</span>
          <span class="sidebar__user-phone">+7 (999) 999-99-99</span>
        </div>
        <button type="button" class="sidebar__user-exit" aria-label="Выйти">
          <PhSignOut :size="20" color="var(--c-text-secondary)" />
        </button>
      </div>

      <div class="sidebar__lang">
        <svg width="24" height="16" viewBox="0 0 24 16" fill="none">
          <rect width="24" height="16" rx="2" fill="#F0F0F0"/>
          <rect y="10.67" width="24" height="5.33" rx="0 0 2 2" fill="#CE2028"/>
          <rect width="24" height="5.33" rx="2 2 0 0" fill="#fff"/>
          <rect y="5.33" width="24" height="5.34" fill="#0039A6"/>
        </svg>
        <span class="sidebar__lang-code">RU</span>
        <PhCaretDown :size="16" color="var(--c-text-tertiary)" />
      </div>
    </div>
    </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import {
  PhHouse,
  PhVideo,
  PhDetective,
  PhTarget,
  PhShareNetwork,
  PhRobot,
  PhMagicWand,
  PhCards,
  PhLinkSimple,
  PhNotepad,
  PhArrowSquareLeft,
  PhSignOut,
  PhCaretDown,
  PhCaretRight,
  PhFire,
  PhCalendarCheck,
  PhHeart,
  PhClockCounterClockwise,
  PhBookmarkSimple,
  PhGraduationCap,
  PhUsersThree,
  PhLightbulb,
  PhHeadset,
} from '@phosphor-icons/vue'
import avatarImg from '@/assets/images/avatar.png'

const avatarSrc = avatarImg
const collapsed = ref(false)
const creativeExpanded = ref(false)

const fig = {
  goldenStone400: '#E99B00',
  brandPrimary600: '#2B31B3',
  electricIndigo600: '#914CFF',
  electricIndigo700: '#7016FF',
  brandDanger600: '#ED003D',
  snappyViolet500: '#FF3DBA',
  deepSea700: '#5E5B7D',
  seaSight500: '#009CCF',
  luckyOrange400: '#FF8E2C',
  psychedelicPurple600: '#C900EC',
  iconSecondary: '#667A85',
} as const

const searchItems = [
  { label: 'Главная', icon: PhHouse, iconColor: fig.goldenStone400, active: true },
  { label: 'Видео', icon: PhVideo, iconColor: fig.brandPrimary600 },
  { label: 'Шпионаж', icon: PhDetective, iconColor: fig.electricIndigo600 },
  { label: 'Контент радар', icon: PhTarget, iconColor: fig.brandDanger600, badge: '712' },
]

const socialItems = [
  { label: 'Кросс-постинг', icon: PhShareNetwork, iconColor: fig.snappyViolet500 },
  { label: 'Чат боты', icon: PhRobot, iconColor: fig.deepSea700 },
]

const toolItems = [
  { label: 'ИИ-сценарий', icon: PhMagicWand, iconColor: fig.seaSight500 },
  { label: 'Карусели', icon: PhCards, iconColor: fig.luckyOrange400 },
  { label: 'Анализ видео', icon: PhLinkSimple, iconColor: fig.electricIndigo700 },
  { label: 'Анализ профиля', icon: PhLinkSimple, iconColor: fig.psychedelicPurple600 },
  { label: 'Черновик', icon: PhNotepad, iconColor: fig.iconSecondary, soon: true },
  { label: 'Контент план', icon: PhCalendarCheck, iconColor: fig.deepSea700, soon: true },
]

const ideasItems = [
  { label: 'Избранные', icon: PhHeart, iconColor: fig.brandDanger600, soon: true },
  { label: 'История', icon: PhClockCounterClockwise, iconColor: fig.brandPrimary600, soon: true },
  { label: 'Закладки', icon: PhBookmarkSimple, iconColor: fig.deepSea700, soon: true },
]

const moreItems = [
  { label: 'Обучение', icon: PhGraduationCap, iconColor: fig.seaSight500, soon: true },
  { label: 'Рефералы', icon: PhUsersThree, iconColor: fig.electricIndigo600, soon: true },
  { label: 'Предложить идею', icon: PhLightbulb, iconColor: fig.goldenStone400, soon: true },
  { label: 'Поддержка', icon: PhHeadset, iconColor: fig.deepSea700 },
]
</script>

<style scoped>
.sidebar {
  position: relative;
  box-sizing: border-box;
  width: 274px;
  height: 100%;
  min-height: 0;
  background: #F4F5F6;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  align-self: stretch;
  transition: width 0.48s cubic-bezier(0.32, 0.72, 0, 1);
  padding: 12px 16px 16px;
  gap: 8px;
  overflow: hidden;
}
.sidebar__strip {
  width: 242px;
  min-width: 242px;
  flex: 1 1 0%;
  min-height: 0;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
}
.sidebar--collapsed { width: 72px; padding-left: 16px; padding-right: 16px; }
.sidebar--collapsed .sidebar__item { justify-content: center; padding: 8px; }
.sidebar--collapsed .sidebar__nav { gap: 10px; }
.sidebar--collapsed .sidebar__section { gap: 2px; }

.sidebar--collapsed .sidebar__item-label,
.sidebar--collapsed .sidebar__item-badge,
.sidebar--collapsed .sidebar__item-soon {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip-path: inset(50%);
  white-space: nowrap;
  border-width: 0;
}

.sidebar--collapsed .sidebar__logo-text,
.sidebar--collapsed .sidebar__logo-badge {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip-path: inset(50%);
  white-space: nowrap;
  border-width: 0;
}

.sidebar__header {
  display: flex;
  align-items: center;
  gap: 6px;
  min-height: 28px;
  flex-shrink: 0;
  padding: 4px 28px 0 0;
}
.sidebar__header--collapsed {
  justify-content: center;
  padding-left: 0;
  padding-right: 28px;
}
.sidebar__logo {
  position: relative;
  display: flex;
  align-items: center;
  gap: 6px;
  flex: 1;
  min-width: 0;
}
.sidebar__header--collapsed .sidebar__logo {
  flex: 0 0 auto;
  justify-content: center;
}
.sidebar__logo-icon { flex-shrink: 0; width: 30px; height: 23px; display: block; }
.sidebar__logo-text { font-family: var(--font-logo); font-weight: 600; font-size: 23px; color: #1B1A25; line-height: 1.2; letter-spacing: -0.47px; }
.sidebar__logo-badge {
  font-size: 12px;
  font-weight: 700;
  color: #4E616B;
  background: #E6E8EA;
  border-radius: 1000px;
  padding: 4px 8px;
  line-height: 14.5px;
  letter-spacing: 0.4px;
}
.sidebar__collapse-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  cursor: pointer;
  flex-shrink: 0;
  padding: 0;
  margin: 0;
}
.sidebar__collapse-btn:hover { opacity: 0.85; }
.sidebar__collapse-icon { display: block; transition: transform 0.48s cubic-bezier(0.32, 0.72, 0, 1); }
.sidebar__collapse-icon--flipped { transform: rotate(180deg); }

.sidebar__body {
  flex: 1 1 0%;
  min-height: 0;
  display: flex;
  flex-direction: column;
  gap: 0;
  overflow: hidden;
}

.sidebar__scroll-shell {
  flex: 1 1 0%;
  min-height: 0;
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  border-bottom-left-radius: 12px;
  border-bottom-right-radius: 12px;
}

.sidebar__scroll-area {
  flex: 1 1 0%;
  min-height: 0;
  overflow-x: hidden;
  overflow-y: auto;
  padding: 0;
  scrollbar-width: thin;
  scrollbar-color: rgb(163 177 184 / 0.55) transparent;
}

.sidebar__scroll-area::-webkit-scrollbar {
  width: 4px;
}

.sidebar__scroll-area::-webkit-scrollbar-track {
  background: transparent;
}

.sidebar__scroll-area::-webkit-scrollbar-thumb {
  background: rgb(163 177 184 / 0.55);
  border-radius: 100px;
}

.sidebar__scroll-area::-webkit-scrollbar-thumb:hover {
  background: rgb(131 147 156 / 0.75);
}

.sidebar__scroll-fade {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 48px;
  pointer-events: none;
  z-index: 2;
  border-bottom-left-radius: 12px;
  border-bottom-right-radius: 12px;
  background: linear-gradient(
    to bottom,
    rgb(244 245 246 / 0) 0%,
    rgb(244 245 246 / 0) 42%,
    rgb(244 245 246 / 0.07) 58%,
    rgb(244 245 246 / 0.18) 68%,
    rgb(244 245 246 / 0.38) 78%,
    rgb(244 245 246 / 0.62) 88%,
    rgb(244 245 246 / 0.88) 96%,
    var(--c-bg) 100%
  );
}

.sidebar__nav {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding-top: 8px;
  padding-bottom: 16px;
  transition: gap 0.38s cubic-bezier(0.32, 0.72, 0, 1);
}
.sidebar__section {
  display: flex;
  flex-direction: column;
  gap: 4px;
  transition: gap 0.38s cubic-bezier(0.32, 0.72, 0, 1);
}
.sidebar__section-header {
  font-size: 14px;
  font-weight: 600;
  color: #83939C;
  line-height: 21px;
  letter-spacing: 0.1px;
  padding: 4px 0;
  max-height: 48px;
  opacity: 1;
  overflow: hidden;
  transition:
    max-height 0.46s cubic-bezier(0.32, 0.72, 0, 1),
    opacity 0.38s ease,
    margin 0.38s ease,
    padding 0.38s ease;
}
.sidebar--collapsed .sidebar__section-header {
  max-height: 0;
  opacity: 0;
  margin: 0;
  padding-top: 0;
  padding-bottom: 0;
}
.sidebar__list { display: flex; flex-direction: column; gap: 0; }
.sidebar__item {
  position: relative;
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 8px;
  border-radius: 12px;
  cursor: pointer;
  transition: background 0.15s;
}
.sidebar__section--social .sidebar__item,
.sidebar__section--tools .sidebar__item,
.sidebar__section--ideas .sidebar__item,
.sidebar__section--more .sidebar__item { border-radius: 8px; }
.sidebar__item:hover { background: rgba(0,0,0,0.04); }
.sidebar__item--active { background: #fff; }
.sidebar__item--active:hover { background: #fff; }
.sidebar__item-icon { width: 24px; height: 24px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.sidebar__item-label { flex: 1; font-size: 16px; font-weight: 500; color: #4E616B; line-height: 24px; letter-spacing: 0.5px; }
.sidebar__item-badge {
  font-size: 12px;
  font-weight: 700;
  color: #2B31B3;
  background: #D5D6F8;
  border-radius: 1000px;
  padding: 4px 8px;
  min-width: 24px;
  text-align: center;
  line-height: 14.5px;
  letter-spacing: 0.4px;
}
.sidebar__item-soon {
  font-size: 12px;
  font-weight: 700;
  color: #4E616B;
  background: #E6E8EA;
  border-radius: 1000px;
  padding: 4px 8px;
  line-height: 14.5px;
  letter-spacing: 0.4px;
}

.sidebar__bottom {
  flex-shrink: 0;
  background: #F4F5F6;
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 0;
  max-height: 560px;
  opacity: 1;
  overflow: hidden;
  visibility: visible;
  transition:
    max-height 0.48s cubic-bezier(0.32, 0.72, 0, 1),
    opacity 0.38s ease,
    visibility 0s linear;
}
.sidebar--collapsed .sidebar__bottom {
  max-height: 0;
  opacity: 0;
  visibility: hidden;
  pointer-events: none;
  gap: 0;
  transition:
    max-height 0.48s cubic-bezier(0.32, 0.72, 0, 1),
    opacity 0.28s ease,
    visibility 0s linear 0.35s;
}

.sidebar__tokens-card {
  position: relative;
  z-index: 1;
  margin-top: -1px;
  background: #fff;
  border-radius: 12px;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  box-shadow: 0 2px 10px rgba(27, 26, 37, 0.05);
}
.sidebar__tokens-card--creative-open {
  padding-bottom: 16px;
  border-radius: 12px;
}
.sidebar__tokens-top {
  display: flex;
  flex-direction: column;
  gap: 12px;
  transition: transform 0.32s cubic-bezier(0.22, 1, 0.36, 1);
}
.sidebar__tokens-card--creative-open .sidebar__tokens-top { transform: translateY(-6px); }
.sidebar__tokens-row { display: flex; align-items: center; gap: 4px; }
.sidebar__tokens-label {
  font-size: 14px;
  font-weight: 700;
  font-style: italic;
  color: #000;
  line-height: 21px;
  letter-spacing: 0.25px;
}
.sidebar__tokens-value {
  font-size: 14px;
  font-weight: 400;
  color: #000;
  margin-left: auto;
  line-height: 21px;
  letter-spacing: 0.25px;
}
.sidebar__tokens-bar { height: 8px; background: #E6E8EA; border-radius: 200px; overflow: hidden; }
.sidebar__tokens-fill { height: 100%; width: 28%; background: #2B31B3; border-radius: 100px; }

.sidebar__tokens-footer { min-height: 0; }

.sidebar__tokens-footer-stack {
  position: relative;
  width: 100%;
}

.sidebar__tokens-footer-pane--creative,
.sidebar__tokens-footer-pane--trial {
  width: 100%;
}

.sidebar__tokens-footer-pane--creative {
  transition:
    opacity 0.1s cubic-bezier(0.4, 0, 1, 1),
    transform 0.1s cubic-bezier(0.4, 0, 1, 1);
}

.sidebar__tokens-footer-pane--trial {
  display: flex;
  flex-direction: column;
  gap: 12px;
  transition:
    opacity 0.26s cubic-bezier(0.4, 0, 0.2, 1),
    transform 0.32s cubic-bezier(0.22, 1, 0.36, 1);
}

.sidebar__tokens-footer-stack:not(.sidebar__tokens-footer-stack--open) .sidebar__tokens-footer-pane--creative {
  position: relative;
  z-index: 1;
  opacity: 1;
  transform: translateY(0);
  pointer-events: auto;
}

.sidebar__tokens-footer-stack:not(.sidebar__tokens-footer-stack--open) .sidebar__tokens-footer-pane--trial {
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  z-index: 0;
  opacity: 0;
  transform: translateY(12px);
  pointer-events: none;
}

.sidebar__tokens-footer-stack--open .sidebar__tokens-footer-pane--creative {
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  z-index: 0;
  opacity: 0;
  transform: translateY(-8px);
  pointer-events: none;
}

.sidebar__tokens-footer-stack--open .sidebar__tokens-footer-pane--trial {
  position: relative;
  z-index: 1;
  opacity: 1;
  transform: translateY(0);
  pointer-events: auto;
}

.sidebar__creative {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  width: 100%;
  padding: 0;
  margin: 0;
  border: none;
  background: none;
  cursor: pointer;
  font: inherit;
  text-align: left;
}
.sidebar__creative:hover .sidebar__creative-label { color: #667a85; }
.sidebar__creative-label { font-size: 14px; font-weight: 500; color: #83939C; line-height: 21px; letter-spacing: 0.25px; }
.sidebar__creative-icon { display: block; flex-shrink: 0; }

.sidebar__trial-head {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  width: 100%;
  padding: 0;
  margin: 0;
  border: none;
  background: none;
  cursor: pointer;
  font: inherit;
  text-align: left;
}
.sidebar__trial-head:hover .sidebar__trial-label { color: var(--c-text-tertiary-hover); }
.sidebar__trial-label {
  font-size: 14px;
  font-weight: 500;
  color: var(--c-text-tertiary);
  line-height: 21px;
  letter-spacing: 0.25px;
}

.sidebar__upgrade-btn {
  width: 100%;
  box-sizing: border-box;
  padding: 12px;
  min-height: 40px;
  border-radius: var(--radius-lg);
  background: var(--c-bg);
  color: var(--c-primary);
  font-size: 12px;
  font-weight: 600;
  line-height: 16px;
  letter-spacing: 0.4px;
  border: none;
  cursor: pointer;
  text-align: center;
  font-family: var(--font-main);
  transition: background 0.15s ease;
}
.sidebar__upgrade-btn:hover { background: var(--c-btn-secondary-bg-hover); }
.sidebar__upgrade-btn:active { background: var(--c-btn-secondary-bg-active); }

.sidebar__user {
  display: flex;
  align-items: center;
  gap: 8px;
  min-height: 48px;
  padding: 8px 4px;
  border-radius: 12px;
  background: #F4F5F6;
}
.sidebar__user-avatar { width: 32px; height: 32px; border-radius: 128px; overflow: hidden; flex-shrink: 0; }
.sidebar__user-avatar-img { width: 100%; height: 100%; object-fit: cover; }
.sidebar__user-info { display: flex; flex-direction: column; gap: 4px; flex: 1; min-width: 0; }
.sidebar__user-name { font-size: 14px; font-weight: 500; color: #4E616B; line-height: 21px; letter-spacing: 0.25px; }
.sidebar__user-phone { font-size: 12px; font-weight: 500; color: #A0ADB4; line-height: 14.5px; letter-spacing: 0.4px; }
.sidebar__user-exit {
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  cursor: pointer;
  flex-shrink: 0;
  padding: 0;
}
.sidebar__user-exit:hover { opacity: 0.85; }

.sidebar__lang {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  cursor: pointer;
  border-radius: 12px;
}
.sidebar__lang:hover { background: rgba(0,0,0,0.04); }
.sidebar__lang-code { font-size: 12px; font-weight: 500; color: var(--c-text-tertiary); line-height: 14.5px; letter-spacing: 0.4px; }
</style>

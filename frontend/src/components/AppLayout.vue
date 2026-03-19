<template>
  <div class="app-layout">
    <SideBar />
    <main class="app-layout__main">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
import SideBar from '@/components/SideBar.vue'
</script>

<style scoped>
.app-layout {
  display: flex;
  height: 100%;
  min-height: 0;
  background: var(--c-bg);
}

.app-layout__main {
  flex: 1;
  min-width: 0;
  min-height: 0;
  overflow-y: auto;
  overscroll-behavior: none;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}
</style>

<template>
  <div class="spinner-container">
    <div class="spinner"></div>
    <span v-if="text" class="spinner-text">{{ text }}</span>
  </div>
</template>

<script setup lang="ts">
defineProps<{ text?: string }>()
</script>

<style scoped>
.spinner-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 24px;
}

.spinner {
  width: 24px;
  height: 24px;
  border: 3px solid var(--c-primary-bg);
  border-top-color: var(--c-primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.spinner-text {
  font-size: 14px;
  font-weight: 500;
  color: var(--c-text-muted);
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>

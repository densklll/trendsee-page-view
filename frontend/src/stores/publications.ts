import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Publication } from '@/api/publications'
import { MOCK_PUBLICATIONS } from '@/data/mockFeed'

const defaultUserId = Number(import.meta.env.VITE_FEED_USER_ID) || 1

export const usePublicationsStore = defineStore('publications', () => {
  const items = ref<Publication[]>([])
  const total = ref(0)
  const loading = ref(false)
  const offset = ref(0)
  const limit = 10
  const userId = ref(defaultUserId)
  const feedComplete = ref(false)
  const hasMore = computed(() => !feedComplete.value && items.value.length < total.value)
  const useMock = ref(false)

  function publicationById(id: number): Publication | undefined {
    return items.value.find((p) => p.id === id)
  }

  async function loadMore() {
    if (loading.value || feedComplete.value) return

    loading.value = true
    try {
      const { fetchPublications } = await import('@/api/publications')
      const resp = await fetchPublications(userId.value, limit, offset.value)
      items.value.push(...resp.items)
      total.value = resp.total
      offset.value += resp.items.length
      if (resp.items.length === 0 || items.value.length >= resp.total) {
        feedComplete.value = true
      }
    } catch {
      if (!useMock.value) {
        useMock.value = true
        items.value = []
        total.value = MOCK_PUBLICATIONS.length
        offset.value = 0
        feedComplete.value = false
      }
      const nextBatch = MOCK_PUBLICATIONS.slice(offset.value, offset.value + limit)
      items.value.push(...nextBatch)
      offset.value += nextBatch.length
      if (offset.value >= MOCK_PUBLICATIONS.length) {
        feedComplete.value = true
      }
    } finally {
      loading.value = false
    }
  }

  function reset() {
    items.value = []
    total.value = 0
    offset.value = 0
    useMock.value = false
    feedComplete.value = false
  }

  return { items, total, loading, hasMore, userId, useMock, loadMore, reset, publicationById }
})

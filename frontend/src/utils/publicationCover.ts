import cardThumbGirl from '@/assets/images/card_thumb_girl.png'
import cardThumbTops from '@/assets/images/card_thumb_tops.png'
import cardThumbMan from '@/assets/images/card_thumb_man.png'
import cardThumbText from '@/assets/images/card_thumb_text.png'
import cardThumb1 from '@/assets/images/card_thumb_1.png'
import cardThumb2 from '@/assets/images/card_thumb_2.png'
import cardThumb3 from '@/assets/images/card_thumb_3.png'
import cardThumb4 from '@/assets/images/card_thumb_4.png'
import cardContainer from '@/assets/images/card_container.png'
import videoThumb from '@/assets/images/video_thumb.jpg'
import videoCard from '@/assets/images/video_card.png'
import searchResultsPage from '@/assets/images/search_results_page.png'
import videoDetailPage from '@/assets/images/video_detail_page.png'

const BY_FILENAME: Record<string, string> = {
  'card_thumb_girl.png': cardThumbGirl,
  'card_thumb_tops.png': cardThumbTops,
  'card_thumb_man.png': cardThumbMan,
  'card_thumb_text.png': cardThumbText,
  'card_thumb_1.png': cardThumb1,
  'card_thumb_2.png': cardThumb2,
  'card_thumb_3.png': cardThumb3,
  'card_thumb_4.png': cardThumb4,
  'card_container.png': cardContainer,
  'video_thumb.jpg': videoThumb,
  'video_card.png': videoCard,
  'search_results_page.png': searchResultsPage,
  'video_detail_page.png': videoDetailPage,
}

const FALLBACK_ORDER = [
  cardThumbGirl,
  cardThumbMan,
  cardThumbTops,
  cardThumbText,
]

/** Обложка карточки: из API (`cover_asset`) или ротация по индексу */
export function publicationCoverUrl(
  coverAsset: string | null | undefined,
  cardIndex: number
): string {
  if (coverAsset && BY_FILENAME[coverAsset]) {
    return BY_FILENAME[coverAsset]
  }
  return FALLBACK_ORDER[Math.abs(cardIndex) % FALLBACK_ORDER.length]
}

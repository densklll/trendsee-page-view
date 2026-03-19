import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
})

export interface Publication {
  id: number
  user_id: number
  title: string
  text: string
  cover_asset?: string | null
  created_at: string
  updated_at: string
  source: string
}

export interface PaginatedResponse {
  items: Publication[]
  total: number
  limit: number
  offset: number
}

export async function fetchPublications(
  userId: number,
  limit = 10,
  offset = 0
): Promise<PaginatedResponse> {
  const { data } = await api.get<PaginatedResponse>(
    `/publications/user/${userId}/feed`,
    { params: { limit, offset } }
  )
  return data
}

export async function fetchPublicationById(id: number): Promise<Publication> {
  const { data } = await api.get<Publication>(`/publications/${id}`)
  return data
}

export async function createUser(name: string) {
  const { data } = await api.post('/users', { name })
  return data
}

export async function getToken(userId: number) {
  const { data } = await api.get(`/users/${userId}/token`)
  return data.token as string
}

export async function createPublication(
  token: string,
  title: string,
  text: string
) {
  const { data } = await api.post(
    '/publications',
    { title, text },
    { headers: { Authorization: `Bearer ${token}` } }
  )
  return data
}

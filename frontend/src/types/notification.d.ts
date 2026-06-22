import type { NotificationType, UserRole } from '@/constants/enums'

export interface Notification {
  id: number
  title: string
  content: string
  type: NotificationType
  role?: UserRole
  created_at: string
  is_read: boolean
}

export interface NotificationPage {
  total: number
  page: number
  size: number
  items: Notification[]
}

export interface UnreadCount {
  count: number
}

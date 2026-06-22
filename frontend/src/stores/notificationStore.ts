import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Notification, NotificationPage, UnreadCount } from '@/types/notification'
import request from '@/utils/request'

export const useNotificationStore = defineStore('notification', () => {
  const notifications = ref<Notification[]>([])
  const total = ref(0)
  const unreadCount = ref(0)
  const page = ref(1)
  const size = ref(20)

  async function fetchNotifications(p?: number, s?: number) {
    if (p) page.value = p
    if (s) size.value = s
    const data = await request.get<unknown, NotificationPage>('/notifications', {
      params: { page: page.value, size: size.value }
    })
    notifications.value = data.items
    total.value = data.total
  }

  async function fetchUnreadCount() {
    const data = await request.get<unknown, UnreadCount>('/notifications/unread-count')
    unreadCount.value = data.count
  }

  async function markRead(notificationIds: number[]) {
    await request.post('/notifications/mark-read', { notification_ids: notificationIds })
    notifications.value.forEach((n) => {
      if (notificationIds.includes(n.id)) n.is_read = true
    })
    unreadCount.value = Math.max(0, unreadCount.value - notificationIds.length)
  }

  async function markAllRead() {
    await request.post('/notifications/mark-all-read')
    notifications.value.forEach((n) => (n.is_read = true))
    unreadCount.value = 0
  }

  return {
    notifications,
    total,
    unreadCount,
    page,
    size,
    fetchNotifications,
    fetchUnreadCount,
    markRead,
    markAllRead
  }
})

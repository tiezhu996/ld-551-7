<template>
  <el-popover
    ref="popoverRef"
    placement="bottom-end"
    :width="420"
    trigger="click"
    popper-class="notification-popover"
  >
    <template #reference>
      <el-badge :value="store.unreadCount" :hidden="store.unreadCount === 0" :max="99" class="notification-bell">
        <el-button text circle @click="handleOpen">
          <el-icon :size="20"><Bell /></el-icon>
        </el-button>
      </el-badge>
    </template>
    <div class="notification-panel">
      <div class="panel-header">
        <span class="panel-title">消息通知</span>
        <el-button
          v-if="store.unreadCount > 0"
          type="primary"
          link
          @click="handleMarkAllRead"
        >
          全部已读
        </el-button>
      </div>
      <div class="notification-list" v-loading="loading">
        <el-empty v-if="!loading && store.notifications.length === 0" description="暂无消息" />
        <div
          v-for="item in store.notifications"
          :key="item.id"
          class="notification-item"
          :class="{ unread: !item.is_read }"
          @click="handleItemClick(item)"
        >
          <div class="item-header">
            <el-tag size="small" :type="tagType(item.type)">
              {{ notificationTypeLabel[item.type] }}
            </el-tag>
            <span class="item-time">{{ formatTime(item.created_at) }}</span>
          </div>
          <div class="item-title">{{ item.title }}</div>
          <div class="item-content">{{ item.content }}</div>
        </div>
      </div>
      <div v-if="store.total > store.notifications.length" class="panel-footer">
        <el-button type="primary" link @click="handleLoadMore">加载更多</el-button>
      </div>
    </div>
  </el-popover>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { Bell } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { NotificationType, notificationTypeLabel } from '@/constants/enums'
import { useNotificationStore } from '@/stores/notificationStore'
import type { Notification } from '@/types/notification'
import { formatDateTime } from '@/utils/format'

const store = useNotificationStore()
const loading = ref(false)

function tagType(type: NotificationType): string {
  switch (type) {
    case NotificationType.SYSTEM:
      return 'info'
    case NotificationType.COURSE:
      return 'success'
    case NotificationType.ORDER:
      return 'warning'
    case NotificationType.ANNOUNCEMENT:
      return 'danger'
    default:
      return 'info'
  }
}

function formatTime(time: string) {
  return formatDateTime(time)
}

async function handleOpen() {
  if (store.notifications.length === 0) {
    await store.fetchNotifications()
  }
}

async function handleItemClick(item: Notification) {
  if (!item.is_read) {
    await store.markRead([item.id])
  }
}

async function handleMarkAllRead() {
  try {
    await store.markAllRead()
    ElMessage.success('已全部标记为已读')
  } catch {
    // 错误已在 request 拦截器中处理
  }
}

async function handleLoadMore() {
  loading.value = true
  try {
    await store.fetchNotifications(store.page + 1)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  if (store.unreadCount === 0) {
    store.fetchUnreadCount()
  }
})
</script>

<style scoped>
.notification-bell {
  cursor: pointer;
}

.notification-panel {
  max-height: 480px;
  display: flex;
  flex-direction: column;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 12px;
  border-bottom: 1px solid #e5e7eb;
}

.panel-title {
  font-weight: 700;
  font-size: 16px;
}

.notification-list {
  flex: 1;
  overflow-y: auto;
  margin: 8px -16px 0;
  padding: 0 16px;
  max-height: 360px;
}

.notification-item {
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}

.notification-item + .notification-item {
  margin-top: 4px;
}

.notification-item:hover {
  background: #f3f4f6;
}

.notification-item.unread {
  background: #f0fdf4;
}

.notification-item.unread:hover {
  background: #dcfce7;
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.item-time {
  font-size: 12px;
  color: #6b7280;
}

.item-title {
  font-weight: 600;
  font-size: 14px;
  margin-bottom: 4px;
}

.item-content {
  font-size: 13px;
  color: #4b5563;
  line-height: 1.5;
}

.panel-footer {
  padding-top: 12px;
  border-top: 1px solid #e5e7eb;
  text-align: center;
}
</style>

<style>
.notification-popover {
  padding: 16px !important;
}
</style>

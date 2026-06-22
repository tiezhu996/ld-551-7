export enum CourseStatus {
  DRAFT = 'DRAFT',
  PUBLISHED = 'PUBLISHED',
  ARCHIVED = 'ARCHIVED'
}

export enum CourseLevel {
  BEGINNER = 'BEGINNER',
  INTERMEDIATE = 'INTERMEDIATE',
  ADVANCED = 'ADVANCED'
}

export enum LessonType {
  VIDEO = 'VIDEO',
  TEXT = 'TEXT',
  QUIZ = 'QUIZ'
}

export enum OrderStatus {
  PENDING = 'PENDING',
  PAID = 'PAID',
  REFUNDED = 'REFUNDED',
  CANCELLED = 'CANCELLED'
}

export enum UserRole {
  STUDENT = 'STUDENT',
  INSTRUCTOR = 'INSTRUCTOR',
  ADMIN = 'ADMIN'
}

export enum NotificationType {
  SYSTEM = 'SYSTEM',
  COURSE = 'COURSE',
  ORDER = 'ORDER',
  ANNOUNCEMENT = 'ANNOUNCEMENT'
}

export const notificationTypeLabel: Record<NotificationType, string> = {
  [NotificationType.SYSTEM]: '系统',
  [NotificationType.COURSE]: '课程',
  [NotificationType.ORDER]: '订单',
  [NotificationType.ANNOUNCEMENT]: '公告'
}

export const courseLevelLabel: Record<CourseLevel, string> = {
  [CourseLevel.BEGINNER]: '入门',
  [CourseLevel.INTERMEDIATE]: '进阶',
  [CourseLevel.ADVANCED]: '高级'
}

export const courseStatusLabel: Record<CourseStatus, string> = {
  [CourseStatus.DRAFT]: '草稿',
  [CourseStatus.PUBLISHED]: '已上架',
  [CourseStatus.ARCHIVED]: '已归档'
}

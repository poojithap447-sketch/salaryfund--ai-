import axiosClient from './axiosClient'

export const notificationService = {
  getNotifications: (params) => axiosClient.get('/notifications', { params }).then((r) => r.data),
  markAsRead: (id) => axiosClient.patch(`/notifications/${id}/read`).then((r) => r.data),
  markAllRead: () => axiosClient.patch('/notifications/read-all').then((r) => r.data),
}

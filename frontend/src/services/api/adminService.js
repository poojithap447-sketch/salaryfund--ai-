import axiosClient from './axiosClient'

export const adminService = {
  getSummary: () => axiosClient.get('/admin/summary').then((r) => r.data),
  getCompanies: (params) => axiosClient.get('/admin/companies', { params }).then((r) => r.data),
  getUsers: (params) => axiosClient.get('/admin/users', { params }).then((r) => r.data),
  getAuditLogs: (params) => axiosClient.get('/admin/audit-logs', { params }).then((r) => r.data),
  getSystemHealth: () => axiosClient.get('/admin/system-health').then((r) => r.data),
  getTransactions: (params) => axiosClient.get('/admin/transactions', { params }).then((r) => r.data),
}

import axiosClient from './axiosClient'

export const reportService = {
  getReports: (params) => axiosClient.get('/reports', { params }).then((r) => r.data),
  generateReport: (payload) => axiosClient.post('/reports/generate', payload).then((r) => r.data),
  downloadReport: (id) => axiosClient.get(`/reports/${id}/download`, { responseType: 'blob' }).then((r) => r.data),
}

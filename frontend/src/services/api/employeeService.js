import axiosClient from './axiosClient'

export const employeeService = {
  getSummary: () => axiosClient.get('/employees/me/summary').then((r) => r.data),
  getProfile: () => axiosClient.get('/employees/me').then((r) => r.data),
  updateProfile: (payload) => axiosClient.patch('/employees/me', payload).then((r) => r.data),
  getSalaryTrend: (params) => axiosClient.get('/employees/me/salary-trend', { params }).then((r) => r.data),
  getCareerScore: () => axiosClient.get('/employees/me/career-score').then((r) => r.data),
  getFinancialWellness: () => axiosClient.get('/employees/me/financial-wellness').then((r) => r.data),
  getDocuments: () => axiosClient.get('/employees/me/documents').then((r) => r.data),
  uploadDocument: (formData) =>
    axiosClient.post('/employees/me/documents', formData, { headers: { 'Content-Type': 'multipart/form-data' } }).then((r) => r.data),
}

import axiosClient from './axiosClient'

export const employerService = {
  getSummary: () => axiosClient.get('/employers/me/summary').then((r) => r.data),
  getEmployees: (params) => axiosClient.get('/employers/me/employees', { params }).then((r) => r.data),
  getDepartments: () => axiosClient.get('/employers/me/departments').then((r) => r.data),
  getDepartmentAnalytics: () => axiosClient.get('/employers/me/departments/analytics').then((r) => r.data),
  getWellnessAnalytics: () => axiosClient.get('/employers/me/financial-wellness/analytics').then((r) => r.data),
  approveLoan: (loanId, payload) => axiosClient.post(`/employers/me/loans/${loanId}/approve`, payload).then((r) => r.data),
  rejectLoan: (loanId, payload) => axiosClient.post(`/employers/me/loans/${loanId}/reject`, payload).then((r) => r.data),
}

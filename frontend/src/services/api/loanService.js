import axiosClient from './axiosClient'

export const loanService = {
  getLoans: (params) => axiosClient.get('/loans', { params }).then((r) => r.data),
  getLoanById: (id) => axiosClient.get(`/loans/${id}`).then((r) => r.data),
  checkEligibility: (payload) => axiosClient.post('/loans/eligibility', payload).then((r) => r.data),
  applyLoan: (payload) => axiosClient.post('/loans/apply', payload).then((r) => r.data),
  uploadLoanDocuments: (loanId, formData) =>
    axiosClient.post(`/loans/${loanId}/documents`, formData, { headers: { 'Content-Type': 'multipart/form-data' } }).then((r) => r.data),
  getRepaymentSchedule: (loanId) => axiosClient.get(`/loans/${loanId}/schedule`).then((r) => r.data),
  cancelLoan: (loanId) => axiosClient.post(`/loans/${loanId}/cancel`).then((r) => r.data),
}

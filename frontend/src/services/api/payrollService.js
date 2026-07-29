import axiosClient from './axiosClient'

export const payrollService = {
  getMyPayroll: (params) => axiosClient.get('/payroll/me', { params }).then((r) => r.data),
  getPayrollStatus: () => axiosClient.get('/payroll/status').then((r) => r.data),
  getPayslips: (params) => axiosClient.get('/payroll/payslips', { params }).then((r) => r.data),
  syncPayroll: () => axiosClient.post('/payroll/sync').then((r) => r.data),
}

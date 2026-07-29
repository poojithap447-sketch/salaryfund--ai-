import axiosClient from './axiosClient'

export const analyticsService = {
  getOverview: (params) => axiosClient.get('/analytics/overview', { params }).then((r) => r.data),
  getLoanAnalytics: (params) => axiosClient.get('/analytics/loans', { params }).then((r) => r.data),
  getRiskAnalytics: (params) => axiosClient.get('/analytics/risk', { params }).then((r) => r.data),
  getRevenueAnalytics: (params) => axiosClient.get('/analytics/revenue', { params }).then((r) => r.data),
}

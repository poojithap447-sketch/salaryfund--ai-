import axiosClient from './axiosClient'

export const lenderService = {
  getSummary: () => axiosClient.get('/lenders/me/summary').then((r) => r.data),
  getPortfolio: (params) => axiosClient.get('/lenders/me/portfolio', { params }).then((r) => r.data),
  getInterestRates: () => axiosClient.get('/lenders/me/interest-rates').then((r) => r.data),
  updateInterestRates: (payload) => axiosClient.put('/lenders/me/interest-rates', payload).then((r) => r.data),
  getDefaultRisk: () => axiosClient.get('/lenders/me/default-risk').then((r) => r.data),
}

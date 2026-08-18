import axiosClient from './axiosClient'

export const authService = {
  login: (payload) => axiosClient.post('/auth/login', payload).then((r) => r.data),
  firstTimeLogin: (payload) => axiosClient.post('/auth/first-time-login', payload).then((r) => r.data),
  register: (payload) => axiosClient.post('/auth/register', payload).then((r) => r.data),
  requestOtp: (payload) => axiosClient.post('/auth/otp/request', payload).then((r) => r.data),
  verifyOtp: (payload) => axiosClient.post('/auth/otp/verify', payload).then((r) => r.data),
  resendOtp: (payload) => axiosClient.post('/auth/otp/request', payload).then((r) => r.data),
  forgotPassword: (payload) => axiosClient.post('/auth/password-reset/request', payload).then((r) => r.data),
  resetPassword: (payload) => axiosClient.post('/auth/password-reset/confirm', payload).then((r) => r.data),
  refresh: (payload) => axiosClient.post('/auth/token/refresh', payload).then((r) => r.data),
  logout: () => axiosClient.post('/auth/logout').then((r) => r.data),
  me: () => axiosClient.get('/auth/me').then((r) => r.data),
}

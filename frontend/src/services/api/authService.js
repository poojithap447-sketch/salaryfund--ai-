import axiosClient from './axiosClient'

export const authService = {
  login: (payload) => axiosClient.post('/authentication/login', payload).then((r) => r.data),
  register: (payload) => axiosClient.post('/authentication/register', payload).then((r) => r.data),
  verifyOtp: (payload) => axiosClient.post('/authentication/verify-otp', payload).then((r) => r.data),
  resendOtp: (payload) => axiosClient.post('/authentication/resend-otp', payload).then((r) => r.data),
  forgotPassword: (payload) => axiosClient.post('/authentication/forgot-password', payload).then((r) => r.data),
  resetPassword: (payload) => axiosClient.post('/authentication/reset-password', payload).then((r) => r.data),
  refresh: (payload) => axiosClient.post('/authentication/refresh', payload).then((r) => r.data),
  logout: () => axiosClient.post('/authentication/logout').then((r) => r.data),
  me: () => axiosClient.get('/authentication/me').then((r) => r.data),
}

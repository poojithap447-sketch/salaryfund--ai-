import { lazy } from 'react'

export const Landing = lazy(() => import('@/pages/Landing/Landing'))
export const About = lazy(() => import('@/pages/Landing/About'))

export const Login = lazy(() => import('@/pages/Authentication/Login'))
export const Register = lazy(() => import('@/pages/Authentication/Register'))
export const ForgotPassword = lazy(() => import('@/pages/Authentication/ForgotPassword'))
export const ResetPassword = lazy(() => import('@/pages/Authentication/ResetPassword'))
export const OtpVerification = lazy(() => import('@/pages/Authentication/OtpVerification'))

export const EmployeeDashboard = lazy(() => import('@/pages/Dashboard/Employee/EmployeeDashboard'))
export const EmployerDashboard = lazy(() => import('@/pages/Dashboard/Employer/EmployerDashboard'))
export const AdminDashboard = lazy(() => import('@/pages/Dashboard/Admin/AdminDashboard'))
export const LenderDashboard = lazy(() => import('@/pages/Dashboard/Lender/LenderDashboard'))

export const LoanApplication = lazy(() => import('@/pages/Loans/LoanApplication'))
export const LoanEligibility = lazy(() => import('@/pages/Loans/LoanEligibility'))
export const LoanTracking = lazy(() => import('@/pages/Loans/LoanTracking'))
export const LoanDetails = lazy(() => import('@/pages/Loans/LoanDetails'))
export const EmiCalculator = lazy(() => import('@/pages/Loans/EmiCalculator'))

export const CareerScorePage = lazy(() => import('@/pages/CareerScore/CareerScorePage'))
export const FinancialWellnessPage = lazy(() => import('@/pages/FinancialWellness/FinancialWellnessPage'))
export const Notifications = lazy(() => import('@/pages/Notifications/Notifications'))
export const Reports = lazy(() => import('@/pages/Reports/Reports'))
export const Analytics = lazy(() => import('@/pages/Analytics/Analytics'))
export const Settings = lazy(() => import('@/pages/Settings/Settings'))
export const Profile = lazy(() => import('@/pages/Profile/Profile'))
export const Support = lazy(() => import('@/pages/Support/Support'))
export const Payroll = lazy(() => import('@/pages/Payroll/Payroll'))
export const EmployeesPage = lazy(() => import('@/pages/Employees/EmployeesPage'))
export const LenderPortfolioPage = lazy(() => import('@/pages/Lender/LenderPortfolioPage'))

export const NotFound = lazy(() => import('@/pages/NotFound'))

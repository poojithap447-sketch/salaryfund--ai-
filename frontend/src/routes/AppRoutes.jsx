import { Suspense } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import DashboardLayout from '@/components/layout/DashboardLayout'
import AuthLayout from '@/components/layout/AuthLayout'
import PageLoader from '@/components/common/PageLoader'
import ProtectedRoute from './ProtectedRoute'
import { ROUTES, ROLES } from '@/constants'
import {
  Landing,
  About,
  Pricing,
  Login,
  Register,
  ForgotPassword,
  ResetPassword,
  OtpVerification,
  EmployeeDashboard,
  EmployerDashboard,
  AdminDashboard,
  LenderDashboard,
  LoanApplication,
  LoanEligibility,
  LoanTracking,
  LoanDetails,
  EmiCalculator,
  CareerScorePage,
  FinancialWellnessPage,
  Notifications,
  Reports,
  Analytics,
  Settings,
  Profile,
  Support,
  Payroll,
  NotFound,
} from './lazyPages'

export default function AppRoutes() {
  return (
    <Suspense fallback={<PageLoader />}>
      <Routes>
        {/* Public marketing pages */}
        <Route path={ROUTES.HOME} element={<Landing />} />
        <Route path={ROUTES.ABOUT} element={<About />} />
        <Route path={ROUTES.PRICING} element={<Pricing />} />

        {/* Auth pages */}
        <Route element={<AuthLayout />}>
          <Route path={ROUTES.LOGIN} element={<Login />} />
          <Route path={ROUTES.REGISTER} element={<Register />} />
          <Route path={ROUTES.FORGOT_PASSWORD} element={<ForgotPassword />} />
          <Route path="/reset-password" element={<ResetPassword />} />
          <Route path={ROUTES.OTP} element={<OtpVerification />} />
        </Route>

        {/* Protected dashboard shell */}
        <Route element={<ProtectedRoute />}>
          <Route element={<DashboardLayout />}>
            <Route path={ROUTES.EMPLOYEE_DASHBOARD} element={<EmployeeDashboard />} />
            <Route path={ROUTES.EMPLOYER_DASHBOARD} element={<EmployerDashboard />} />
            <Route path={ROUTES.HR_DASHBOARD} element={<EmployerDashboard />} />
            <Route path={ROUTES.FINANCE_DASHBOARD} element={<EmployerDashboard />} />
            <Route path={ROUTES.ADMIN_DASHBOARD} element={<AdminDashboard />} />
            <Route path={ROUTES.LENDER_DASHBOARD} element={<LenderDashboard />} />

            <Route path={ROUTES.LOAN_APPLICATION} element={<LoanApplication />} />
            <Route path={ROUTES.LOAN_ELIGIBILITY} element={<LoanEligibility />} />
            <Route path={ROUTES.LOAN_TRACKING} element={<LoanTracking />} />
            <Route path={ROUTES.LOAN_DETAILS} element={<LoanDetails />} />
            <Route path={ROUTES.EMI_CALCULATOR} element={<EmiCalculator />} />

            <Route path="/career-score" element={<CareerScorePage />} />
            <Route path="/financial-wellness" element={<FinancialWellnessPage />} />
            <Route path={ROUTES.NOTIFICATIONS} element={<Notifications />} />
            <Route path={ROUTES.REPORTS} element={<Reports />} />
            <Route path={ROUTES.ANALYTICS} element={<Analytics />} />
            <Route path={ROUTES.SETTINGS} element={<Settings />} />
            <Route path={ROUTES.PROFILE} element={<Profile />} />
            <Route path={ROUTES.SUPPORT} element={<Support />} />
            <Route path="/payroll" element={<Payroll />} />
            <Route path="/employees" element={<EmployerDashboard />} />
          </Route>
        </Route>

        <Route path="*" element={<NotFound />} />
      </Routes>
    </Suspense>
  )
}

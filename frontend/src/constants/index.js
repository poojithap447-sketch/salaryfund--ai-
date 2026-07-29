export const ROLES = {
  EMPLOYEE: 'employee',
  EMPLOYER: 'employer',
  HR: 'hr',
  FINANCE: 'finance',
  LENDER: 'lender',
  ADMIN: 'admin',
}

export const ROUTES = {
  HOME: '/',
  ABOUT: '/about',
  PRICING: '/pricing',
  LOGIN: '/login',
  REGISTER: '/register',
  FORGOT_PASSWORD: '/forgot-password',
  OTP: '/otp-verification',

  EMPLOYEE_DASHBOARD: '/dashboard/employee',
  EMPLOYER_DASHBOARD: '/dashboard/employer',
  HR_DASHBOARD: '/dashboard/hr',
  FINANCE_DASHBOARD: '/dashboard/finance',
  LENDER_DASHBOARD: '/dashboard/lender',
  ADMIN_DASHBOARD: '/dashboard/admin',

  LOAN_APPLICATION: '/loans/apply',
  LOAN_ELIGIBILITY: '/loans/eligibility',
  LOAN_TRACKING: '/loans/tracking',
  LOAN_DETAILS: '/loans/:id',
  EMI_CALCULATOR: '/loans/emi-calculator',

  NOTIFICATIONS: '/notifications',
  REPORTS: '/reports',
  ANALYTICS: '/analytics',
  SETTINGS: '/settings',
  PROFILE: '/profile',
  SUPPORT: '/support',
}

export const QUERY_KEYS = {
  EMPLOYEE_SUMMARY: 'employee-summary',
  EMPLOYER_SUMMARY: 'employer-summary',
  ADMIN_SUMMARY: 'admin-summary',
  LENDER_SUMMARY: 'lender-summary',
  LOANS: 'loans',
  LOAN_DETAIL: 'loan-detail',
  PAYROLL: 'payroll',
  NOTIFICATIONS: 'notifications',
  CAREER_SCORE: 'career-score',
  FINANCIAL_WELLNESS: 'financial-wellness',
  REPORTS: 'reports',
  ANALYTICS: 'analytics',
}

export const LOAN_TYPES = [
  { value: 'salary_advance', label: 'Salary Advance' },
  { value: 'personal_loan', label: 'Personal Loan' },
  { value: 'emergency_loan', label: 'Emergency Loan' },
  { value: 'education_loan', label: 'Education Loan' },
]

export const LOAN_STATUS = {
  PENDING: 'pending',
  APPROVED: 'approved',
  REJECTED: 'rejected',
  DISBURSED: 'disbursed',
  ACTIVE: 'active',
  CLOSED: 'closed',
}

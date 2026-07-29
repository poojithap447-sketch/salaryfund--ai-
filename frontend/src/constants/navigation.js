import {
  LayoutDashboard,
  Wallet,
  Landmark,
  Users,
  Building2,
  BarChart3,
  FileText,
  Settings,
  Bell,
  CreditCard,
  ShieldCheck,
  PiggyBank,
  Gauge,
} from 'lucide-react'
import { ROLES, ROUTES } from './index'

export const NAV_CONFIG = {
  [ROLES.EMPLOYEE]: [
    { label: 'Overview', icon: LayoutDashboard, path: ROUTES.EMPLOYEE_DASHBOARD },
    { label: 'Loans', icon: Wallet, path: ROUTES.LOAN_TRACKING },
    { label: 'Apply for Loan', icon: CreditCard, path: ROUTES.LOAN_APPLICATION },
    { label: 'EMI Calculator', icon: Gauge, path: ROUTES.EMI_CALCULATOR },
    { label: 'Career Score', icon: ShieldCheck, path: '/career-score' },
    { label: 'Financial Wellness', icon: PiggyBank, path: '/financial-wellness' },
    { label: 'Notifications', icon: Bell, path: ROUTES.NOTIFICATIONS },
    { label: 'Settings', icon: Settings, path: ROUTES.SETTINGS },
  ],
  [ROLES.EMPLOYER]: [
    { label: 'Overview', icon: LayoutDashboard, path: ROUTES.EMPLOYER_DASHBOARD },
    { label: 'Employees', icon: Users, path: '/employees' },
    { label: 'Loans', icon: Wallet, path: ROUTES.LOAN_TRACKING },
    { label: 'Payroll', icon: Landmark, path: '/payroll' },
    { label: 'Analytics', icon: BarChart3, path: ROUTES.ANALYTICS },
    { label: 'Reports', icon: FileText, path: ROUTES.REPORTS },
    { label: 'Settings', icon: Settings, path: ROUTES.SETTINGS },
  ],
  [ROLES.ADMIN]: [
    { label: 'Overview', icon: LayoutDashboard, path: ROUTES.ADMIN_DASHBOARD },
    { label: 'Companies', icon: Building2, path: '/admin/companies' },
    { label: 'Users', icon: Users, path: '/admin/users' },
    { label: 'Loans', icon: Wallet, path: ROUTES.LOAN_TRACKING },
    { label: 'Analytics', icon: BarChart3, path: ROUTES.ANALYTICS },
    { label: 'Audit Logs', icon: ShieldCheck, path: '/admin/audit-logs' },
    { label: 'Settings', icon: Settings, path: ROUTES.SETTINGS },
  ],
  [ROLES.LENDER]: [
    { label: 'Overview', icon: LayoutDashboard, path: ROUTES.LENDER_DASHBOARD },
    { label: 'Portfolio', icon: Wallet, path: '/lender/portfolio' },
    { label: 'Interest Rates', icon: Landmark, path: '/lender/interest-rates' },
    { label: 'Risk Analytics', icon: BarChart3, path: ROUTES.ANALYTICS },
    { label: 'Settings', icon: Settings, path: ROUTES.SETTINGS },
  ],
}

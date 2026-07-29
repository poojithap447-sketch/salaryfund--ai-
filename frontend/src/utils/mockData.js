// Demo fixtures used as graceful fallback when VITE_API_BASE_URL isn't reachable yet.
// Every hook tries the real endpoint first (see src/hooks) — this only fires on network failure,
// so the UI is fully explorable standalone and swaps to live data the moment the backend is up.

export const mockEmployeeSummary = {
  name: 'Ananya Rao',
  designation: 'Senior Product Designer',
  employer: 'Nimbus Retail Pvt Ltd',
  currentSalary: 128000,
  availableLoan: 64000,
  loanBalance: 22400,
  remainingEmi: 4,
  nextEmiDate: '2026-08-05',
  careerCreditScore: 742,
  financialWellnessScore: 78,
}

export const salaryTrend = [
  { month: 'Feb', salary: 118000 },
  { month: 'Mar', salary: 118000 },
  { month: 'Apr', salary: 122000 },
  { month: 'May', salary: 122000 },
  { month: 'Jun', salary: 128000 },
  { month: 'Jul', salary: 128000 },
]

export const emiTrend = [
  { month: 'Feb', paid: 5600 },
  { month: 'Mar', paid: 5600 },
  { month: 'Apr', paid: 5600 },
  { month: 'May', paid: 5600 },
  { month: 'Jun', paid: 5600 },
  { month: 'Jul', paid: 5600 },
]

export const repaymentTrend = [
  { month: 'Feb', onTime: 100 },
  { month: 'Mar', onTime: 100 },
  { month: 'Apr', onTime: 92 },
  { month: 'May', onTime: 100 },
  { month: 'Jun', onTime: 100 },
  { month: 'Jul', onTime: 100 },
]

export const loanHistory = [
  { id: 'LN-2291', type: 'Salary Advance', amount: 40000, status: 'closed', date: '2025-12-02' },
  { id: 'LN-2354', type: 'Emergency Loan', amount: 22400, status: 'active', date: '2026-05-18' },
  { id: 'LN-2402', type: 'Personal Loan', amount: 64000, status: 'pending', date: '2026-07-21' },
]

export const recentNotifications = [
  { id: 'n1', title: 'EMI due in 3 days', body: '₹5,600 will be auto-debited on Aug 5.', read: false, time: '2h ago' },
  { id: 'n2', title: 'Career Credit Score updated', body: 'Your score improved by 12 points this month.', read: false, time: '1d ago' },
  { id: 'n3', title: 'Loan LN-2354 disbursed', body: '₹22,400 credited to your linked account.', read: true, time: '3d ago' },
]

export const employerSummary = {
  companyName: 'Nimbus Retail Pvt Ltd',
  totalEmployees: 1284,
  activeLoans: 312,
  pendingApproval: 18,
  payrollStatus: 'synced',
  defaultRiskRate: 2.1,
  totalDisbursed: 18400000,
}

export const departmentAnalytics = [
  { department: 'Engineering', employees: 340, avgWellness: 81, activeLoans: 62 },
  { department: 'Sales', employees: 410, avgWellness: 68, activeLoans: 121 },
  { department: 'Operations', employees: 280, avgWellness: 74, activeLoans: 84 },
  { department: 'Support', employees: 160, avgWellness: 71, activeLoans: 33 },
  { department: 'Finance', employees: 94, avgWellness: 85, activeLoans: 12 },
]

export const loanTypeSplit = [
  { name: 'Salary Advance', value: 44 },
  { name: 'Emergency Loan', value: 26 },
  { name: 'Personal Loan', value: 21 },
  { name: 'Education Loan', value: 9 },
]

export const adminSummary = {
  revenue: 8420000,
  companies: 64,
  users: 128400,
  activeLoans: 9218,
  documentsProcessed: 41200,
  systemUptime: 99.98,
}

export const revenueTrend = [
  { month: 'Feb', revenue: 620000 },
  { month: 'Mar', revenue: 690000 },
  { month: 'Apr', revenue: 710000 },
  { month: 'May', revenue: 780000 },
  { month: 'Jun', revenue: 812000 },
  { month: 'Jul', revenue: 842000 },
]

export const auditLogs = [
  { id: 'A-9910', actor: 'system', action: 'AI model retrained (eligibility_v4)', time: '10 min ago', level: 'info' },
  { id: 'A-9909', actor: 'admin@nimbus.io', action: 'Approved lender onboarding: Kastle Capital', time: '48 min ago', level: 'success' },
  { id: 'A-9908', actor: 'fraud-engine', action: 'Flagged duplicate PAN on application LN-2402', time: '1h ago', level: 'warning' },
  { id: 'A-9907', actor: 'admin@nimbus.io', action: 'Rate limit threshold updated', time: '3h ago', level: 'info' },
]

export const lenderSummary = {
  lenderName: 'Kastle Capital',
  portfolioValue: 42800000,
  activeLoans: 1840,
  avgInterestRate: 13.4,
  defaultRate: 1.8,
  npaRatio: 0.9,
}

export const riskDistribution = [
  { risk: 'Low', count: 1240 },
  { risk: 'Medium', count: 480 },
  { risk: 'High', count: 120 },
]

export const financialWellness = {
  score: 78,
  debtToIncome: 24,
  savingsRatio: 18,
  emiBurden: 12,
  loanUtilization: 34,
  emergencyReserve: 62,
  recommendations: [
    'Increase emergency reserve to 3 months of salary to improve resilience.',
    'Your EMI burden is healthy — consider automating savings transfers on payday.',
    'Loan utilization is moderate; avoid stacking a new salary advance this cycle.',
  ],
}

export const careerScoreHistory = [
  { month: 'Feb', score: 698 },
  { month: 'Mar', score: 705 },
  { month: 'Apr', score: 712 },
  { month: 'May', score: 724 },
  { month: 'Jun', score: 730 },
  { month: 'Jul', score: 742 },
]

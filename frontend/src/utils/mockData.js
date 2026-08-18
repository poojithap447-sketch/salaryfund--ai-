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
  { id: '1', action: 'Employer Onboarded', actor: 'Admin (System)', time: '10 mins ago', level: 'info' },
  { id: '2', action: 'Risk Model Retrained', actor: 'AI Engine', time: '1 hour ago', level: 'success' },
  { id: '3', action: 'High Risk Alert Triggered', actor: 'Fraud Engine', time: '3 hours ago', level: 'danger' },
  { id: '4', action: 'API Key Rotated', actor: 'Capital Alliance NBFC', time: '5 hours ago', level: 'warning' },
]

export const mockEmployeesList = [
  {
    id: 'emp-1',
    employee_code: 'cci26',
    full_name: 'Rahul Sharma',
    email: 'rahul.sharma@company.com',
    department: 'Engineering',
    designation: 'Senior Software Engineer',
    monthly_net_salary: 85000,
    active_loans: 1,
    status: 'Active',
    joined_date: '2023-04-12',
  },
  {
    id: 'emp-2',
    employee_code: 'cci27',
    full_name: 'Ananya Rao',
    email: 'ananya.rao@company.com',
    department: 'Product',
    designation: 'Product Manager',
    monthly_net_salary: 92000,
    active_loans: 0,
    status: 'Active',
    joined_date: '2023-08-01',
  },
  {
    id: 'emp-3',
    employee_code: 'cci28',
    full_name: 'Vikramaditya Patel',
    email: 'vikram.p@company.com',
    department: 'Sales',
    designation: 'Account Executive',
    monthly_net_salary: 68000,
    active_loans: 2,
    status: 'Active',
    joined_date: '2024-01-15',
  },
  {
    id: 'emp-4',
    employee_code: 'cci29',
    full_name: 'Priya Sundaram',
    email: 'priya.s@company.com',
    department: 'Finance',
    designation: 'Financial Analyst',
    monthly_net_salary: 74000,
    active_loans: 0,
    status: 'Pending First Login',
    joined_date: '2026-02-10',
  },
  {
    id: 'emp-5',
    employee_code: 'cci30',
    full_name: 'Karan Malhotra',
    email: 'karan.m@company.com',
    department: 'Operations',
    designation: 'Operations Lead',
    monthly_net_salary: 78000,
    active_loans: 1,
    status: 'Active',
    joined_date: '2022-11-20',
  },
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

export const mockLenderPortfolio = [
  {
    id: 'LN-9812',
    borrower_name: 'Rahul Sharma',
    employee_code: 'cci26',
    employer_name: 'Nimbus Enterprise',
    principal_amount: 55000,
    interest_rate: 12.5,
    tenure_months: 6,
    monthly_emi: 9490,
    career_score: 742,
    risk_tier: 'Low',
    disbursement_date: '2026-02-01',
    status: 'Disbursed',
  },
  {
    id: 'LN-9815',
    borrower_name: 'Ananya Rao',
    employee_code: 'cci27',
    employer_name: 'Nimbus Enterprise',
    principal_amount: 80000,
    interest_rate: 13.0,
    tenure_months: 12,
    monthly_emi: 7140,
    career_score: 780,
    risk_tier: 'Low',
    disbursement_date: '2026-02-12',
    status: 'Underwriting Approved',
  },
  {
    id: 'LN-9819',
    borrower_name: 'Vikramaditya Patel',
    employee_code: 'cci28',
    employer_name: 'Nimbus Enterprise',
    principal_amount: 35000,
    interest_rate: 14.2,
    tenure_months: 3,
    monthly_emi: 11940,
    career_score: 650,
    risk_tier: 'Medium',
    disbursement_date: '2026-02-15',
    status: 'Disbursed',
  },
  {
    id: 'LN-9822',
    borrower_name: 'Priya Sundaram',
    employee_code: 'cci29',
    employer_name: 'Nimbus Enterprise',
    principal_amount: 100000,
    interest_rate: 12.0,
    tenure_months: 12,
    monthly_emi: 8880,
    career_score: 810,
    risk_tier: 'Low',
    disbursement_date: '2026-02-16',
    status: 'Pending NBFC Approval',
  },
  {
    id: 'LN-9826',
    borrower_name: 'Karan Malhotra',
    employee_code: 'cci30',
    employer_name: 'Nimbus Enterprise',
    principal_amount: 45000,
    interest_rate: 15.5,
    tenure_months: 6,
    monthly_emi: 7850,
    career_score: 610,
    risk_tier: 'High',
    disbursement_date: '2026-02-17',
    status: 'Pending NBFC Approval',
  },
]


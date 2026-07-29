import { Users, Wallet, Clock, ShieldAlert } from 'lucide-react'
import PageHeader from '@/components/common/PageHeader'
import StatCard from '@/components/common/StatCard'
import { StatCardSkeleton, ChartSkeleton } from '@/components/common/Skeletons'
import DistributionBarChart from '@/components/charts/DistributionBarChart'
import SplitPieChart from '@/components/charts/SplitPieChart'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { useEmployerSummary, useDepartmentAnalytics, useLoanTypeSplit } from '@/hooks/useEmployerData'
import { formatCurrency, formatPercent } from '@/utils/format'

export default function EmployerDashboard() {
  const { data: summary, isLoading } = useEmployerSummary()
  const { data: departments, isLoading: deptLoading } = useDepartmentAnalytics()
  const { data: loanSplit } = useLoanTypeSplit()

  return (
    <div>
      <PageHeader title={summary?.companyName || 'Employer overview'} description="Team-wide loan, payroll, and wellness signals." />

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {isLoading ? (
          Array.from({ length: 4 }).map((_, i) => <StatCardSkeleton key={i} />)
        ) : (
          <>
            <StatCard label="Total employees" value={summary.totalEmployees.toLocaleString('en-IN')} icon={Users} accent="primary" />
            <StatCard label="Active loans" value={summary.activeLoans} icon={Wallet} accent="accent" trend={6} trendLabel="vs last month" />
            <StatCard label="Pending approval" value={summary.pendingApproval} icon={Clock} accent="warning" />
            <StatCard label="Default risk" value={formatPercent(summary.defaultRiskRate)} icon={ShieldAlert} accent="success" trend={-3} trendLabel="vs last quarter" />
          </>
        )}
      </div>

      <div className="mt-5 grid grid-cols-1 gap-5 lg:grid-cols-3">
        <div className="lg:col-span-2">
          {deptLoading ? (
            <ChartSkeleton height={300} />
          ) : (
            <DistributionBarChart
              title="Department analytics"
              description="Active loans by department"
              data={departments}
              dataKey="activeLoans"
              xKey="department"
            />
          )}
        </div>
        <SplitPieChart title="Loan type mix" description="Share of total disbursed loans" data={loanSplit || []} />
      </div>

      <Card className="mt-5">
        <CardHeader>
          <CardTitle>Financial wellness by department</CardTitle>
          <CardDescription>Average employee wellness score (0–100)</CardDescription>
        </CardHeader>
        <CardContent className="space-y-3">
          {(departments || []).map((d) => (
            <div key={d.department} className="flex items-center justify-between rounded-xl bg-secondary/30 px-4 py-3">
              <div>
                <p className="text-sm font-medium">{d.department}</p>
                <p className="text-xs text-muted-foreground">{d.employees} employees</p>
              </div>
              <Badge variant={d.avgWellness >= 75 ? 'success' : d.avgWellness >= 60 ? 'warning' : 'danger'}>
                {d.avgWellness} / 100
              </Badge>
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  )
}

import { Building2, FileText, ShieldAlert, TrendingUp, Users, Wallet } from 'lucide-react'
import PageHeader from '@/components/common/PageHeader'
import StatCard from '@/components/common/StatCard'
import { StatCardSkeleton, ChartSkeleton } from '@/components/common/Skeletons'
import TrendAreaChart from '@/components/charts/TrendAreaChart'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { useAdminSummary, useRevenueTrend, useAuditLogs } from '@/hooks/useAdminData'
import { formatCompactNumber, formatCurrency, formatPercent } from '@/utils/format'

const LEVEL_VARIANT = { info: 'secondary', success: 'success', warning: 'warning', danger: 'danger' }

export default function AdminDashboard() {
  const { data: summary, isLoading } = useAdminSummary()
  const { data: revenue, isLoading: revenueLoading } = useRevenueTrend()
  const { data: logs, isLoading: logsLoading } = useAuditLogs()

  return (
    <div>
      <PageHeader title="Platform overview" description="Revenue, system health, and activity across all tenants." />

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {isLoading ? (
          Array.from({ length: 4 }).map((_, i) => <StatCardSkeleton key={i} />)
        ) : (
          <>
            <StatCard label="Revenue (MTD)" value={formatCurrency(summary.revenue)} icon={TrendingUp} accent="primary" trend={9} trendLabel="vs last month" />
            <StatCard label="Companies" value={summary.companies} icon={Building2} accent="accent" />
            <StatCard label="Total users" value={formatCompactNumber(summary.users)} icon={Users} accent="success" />
            <StatCard label="System uptime" value={formatPercent(summary.systemUptime, 2)} icon={ShieldAlert} accent="warning" />
          </>
        )}
      </div>

      <div className="mt-5 grid grid-cols-1 gap-5 lg:grid-cols-3">
        <div className="lg:col-span-2">
          {revenueLoading ? (
            <ChartSkeleton />
          ) : (
            <TrendAreaChart title="Revenue trend" description="Last 6 months" data={revenue} dataKey="revenue" valueFormatter={formatCurrency} />
          )}
        </div>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Wallet className="h-4 w-4 text-primary" /> Active loans
            </CardTitle>
            <CardDescription>Across all companies</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="font-display text-4xl font-semibold">{summary?.activeLoans?.toLocaleString('en-IN')}</p>
            <p className="mt-2 text-sm text-muted-foreground">
              <FileText className="mr-1 inline h-3.5 w-3.5" />
              {summary?.documentsProcessed?.toLocaleString('en-IN')} documents processed
            </p>
          </CardContent>
        </Card>
      </div>

      <Card className="mt-5">
        <CardHeader>
          <CardTitle>Audit logs</CardTitle>
          <CardDescription>Recent system and administrative activity</CardDescription>
        </CardHeader>
        <CardContent className="space-y-2">
          {logsLoading
            ? Array.from({ length: 4 }).map((_, i) => <div key={i} className="skeleton h-12 w-full rounded-lg" />)
            : logs.map((log) => (
                <div key={log.id} className="flex items-center justify-between gap-3 rounded-xl bg-secondary/30 px-4 py-3">
                  <div className="min-w-0">
                    <p className="truncate text-sm font-medium">{log.action}</p>
                    <p className="text-xs text-muted-foreground">{log.actor} · {log.time}</p>
                  </div>
                  <Badge variant={LEVEL_VARIANT[log.level] || 'secondary'} className="shrink-0 capitalize">
                    {log.level}
                  </Badge>
                </div>
              ))}
        </CardContent>
      </Card>
    </div>
  )
}

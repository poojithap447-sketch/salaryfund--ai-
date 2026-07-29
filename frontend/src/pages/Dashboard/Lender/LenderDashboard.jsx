import { Landmark, Percent, ShieldAlert, Wallet } from 'lucide-react'
import PageHeader from '@/components/common/PageHeader'
import StatCard from '@/components/common/StatCard'
import { StatCardSkeleton, ChartSkeleton } from '@/components/common/Skeletons'
import DistributionBarChart from '@/components/charts/DistributionBarChart'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { useLenderSummary, useRiskDistribution } from '@/hooks/useLenderData'
import { formatCurrency, formatPercent } from '@/utils/format'

export default function LenderDashboard() {
  const { data: summary, isLoading } = useLenderSummary()
  const { data: risk, isLoading: riskLoading } = useRiskDistribution()

  return (
    <div>
      <PageHeader title={summary?.lenderName || 'Lender overview'} description="Portfolio performance and risk exposure." />

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {isLoading ? (
          Array.from({ length: 4 }).map((_, i) => <StatCardSkeleton key={i} />)
        ) : (
          <>
            <StatCard label="Portfolio value" value={formatCurrency(summary.portfolioValue)} icon={Landmark} accent="primary" />
            <StatCard label="Active loans" value={summary.activeLoans} icon={Wallet} accent="accent" />
            <StatCard label="Avg. interest rate" value={formatPercent(summary.avgInterestRate)} icon={Percent} accent="success" />
            <StatCard label="NPA ratio" value={formatPercent(summary.npaRatio)} icon={ShieldAlert} accent="warning" trend={-0.4} trendLabel="vs last quarter" />
          </>
        )}
      </div>

      <div className="mt-5 grid grid-cols-1 gap-5 lg:grid-cols-3">
        <div className="lg:col-span-2">
          {riskLoading ? (
            <ChartSkeleton />
          ) : (
            <DistributionBarChart title="Risk distribution" description="Active loans by risk tier" data={risk} dataKey="count" xKey="risk" />
          )}
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Default rate</CardTitle>
            <CardDescription>Trailing 90 days</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="font-display text-4xl font-semibold text-success">{formatPercent(summary?.defaultRate)}</p>
            <p className="mt-2 text-sm text-muted-foreground">Well within your configured threshold of 3.0%</p>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

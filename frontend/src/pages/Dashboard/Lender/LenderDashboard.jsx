import { Landmark, Percent, ShieldAlert, Wallet } from 'lucide-react'
import PageHeader from '@/components/common/PageHeader'
import StatCard from '@/components/common/StatCard'
import { StatCardSkeleton, ChartSkeleton } from '@/components/common/Skeletons'
import DistributionBarChart from '@/components/charts/DistributionBarChart'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { useLenderSummary, useRiskDistribution } from '@/hooks/useLenderData'
import { formatCurrency, formatPercent } from '@/utils/format'
import { lenderSummary as defaultLenderSummary, riskDistribution as defaultRisk } from '@/utils/mockData'

export default function LenderDashboard() {
  const { data: summary, isLoading } = useLenderSummary()
  const { data: risk, isLoading: riskLoading } = useRiskDistribution()

  const safeSummary = summary || defaultLenderSummary
  const safeRisk = risk || defaultRisk

  return (
    <div>
      <PageHeader title={safeSummary?.lenderName || 'NBFC Lender Overview'} description="Portfolio performance and risk exposure." />

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {isLoading && !summary ? (
          Array.from({ length: 4 }).map((_, i) => <StatCardSkeleton key={i} />)
        ) : (
          <>
            <StatCard label="Portfolio value" value={formatCurrency(safeSummary?.portfolioValue ?? 12500000)} icon={Landmark} accent="primary" />
            <StatCard label="Active loans" value={safeSummary?.activeLoans ?? 384} icon={Wallet} accent="accent" />
            <StatCard label="Avg. interest rate" value={formatPercent(safeSummary?.avgInterestRate ?? 0.125)} icon={Percent} accent="success" />
            <StatCard label="NPA ratio" value={formatPercent(safeSummary?.npaRatio ?? 0.008)} icon={ShieldAlert} accent="warning" trend={-0.4} trendLabel="vs last quarter" />
          </>
        )}
      </div>

      <div className="mt-5 grid grid-cols-1 gap-5 lg:grid-cols-3">
        <div className="lg:col-span-2">
          {riskLoading && !risk ? (
            <ChartSkeleton />
          ) : (
            <DistributionBarChart title="Risk distribution" description="Active loans by risk tier" data={safeRisk} dataKey="count" xKey="risk" />
          )}
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Default rate</CardTitle>
            <CardDescription>Trailing 90 days</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="font-display text-4xl font-semibold text-success">{formatPercent(safeSummary?.defaultRate ?? 0.008)}</p>
            <p className="mt-2 text-sm text-muted-foreground">Well within your configured threshold of 3.0%</p>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}


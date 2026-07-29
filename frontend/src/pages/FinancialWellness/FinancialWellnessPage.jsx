import PageHeader from '@/components/common/PageHeader'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { useFinancialWellness } from '@/hooks/useEmployeeData'
import { Sparkles } from 'lucide-react'

const METRICS = [
  { key: 'debtToIncome', label: 'Debt-to-income ratio', tone: 'primary' },
  { key: 'savingsRatio', label: 'Savings ratio', tone: 'success' },
  { key: 'emiBurden', label: 'EMI burden', tone: 'warning' },
  { key: 'loanUtilization', label: 'Loan utilization', tone: 'accent' },
  { key: 'emergencyReserve', label: 'Emergency reserve', tone: 'success' },
]

export default function FinancialWellnessPage() {
  const { data, isLoading } = useFinancialWellness()

  return (
    <div>
      <PageHeader title="Financial wellness" description="A full breakdown of your financial health signals." />

      <div className="grid grid-cols-1 gap-5 lg:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle>Overall score</CardTitle>
          </CardHeader>
          <CardContent className="flex flex-col items-center py-6">
            <p className="font-display text-5xl font-semibold">{data?.score ?? '—'}</p>
            <p className="mt-1 text-sm text-muted-foreground">out of 100</p>
            <Progress value={data?.score || 0} className="mt-5 w-full" />
          </CardContent>
        </Card>

        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Breakdown</CardTitle>
            <CardDescription>Each metric shown as a percentage of healthy benchmark</CardDescription>
          </CardHeader>
          <CardContent className="space-y-5">
            {!isLoading &&
              METRICS.map((m) => (
                <div key={m.key}>
                  <div className="mb-1.5 flex items-center justify-between text-sm">
                    <span className="text-muted-foreground">{m.label}</span>
                    <span className="font-medium">{data?.[m.key]}%</span>
                  </div>
                  <Progress value={data?.[m.key]} />
                </div>
              ))}
          </CardContent>
        </Card>
      </div>

      <Card className="mt-5">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Sparkles className="h-4 w-4 text-primary" /> Recommendations
          </CardTitle>
          <CardDescription>Generated from your latest financial pattern</CardDescription>
        </CardHeader>
        <CardContent className="space-y-3">
          {(data?.recommendations || []).map((r, i) => (
            <div key={i} className="rounded-xl bg-secondary/30 px-4 py-3 text-sm">
              {r}
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  )
}

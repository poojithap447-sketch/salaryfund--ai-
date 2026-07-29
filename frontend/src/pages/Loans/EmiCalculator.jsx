import { useMemo, useState } from 'react'
import PageHeader from '@/components/common/PageHeader'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Label } from '@/components/ui/label'
import SplitPieChart from '@/components/charts/SplitPieChart'
import { formatCurrency, formatPercent } from '@/utils/format'

function calculateEmi(principal, annualRate, months) {
  const monthlyRate = annualRate / 12 / 100
  if (monthlyRate === 0) return principal / months
  const emi = (principal * monthlyRate * Math.pow(1 + monthlyRate, months)) / (Math.pow(1 + monthlyRate, months) - 1)
  return emi
}

export default function EmiCalculator() {
  const [principal, setPrincipal] = useState(50000)
  const [rate, setRate] = useState(13.5)
  const [months, setMonths] = useState(12)

  const { emi, totalInterest, totalPayment } = useMemo(() => {
    const emiVal = calculateEmi(principal, rate, months)
    const total = emiVal * months
    return { emi: emiVal, totalInterest: total - principal, totalPayment: total }
  }, [principal, rate, months])

  const pieData = [
    { name: 'Principal', value: Math.round(principal) },
    { name: 'Interest', value: Math.round(totalInterest) },
  ]

  return (
    <div>
      <PageHeader title="EMI Calculator" description="Estimate your monthly payment before you apply." />

      <div className="grid grid-cols-1 gap-5 lg:grid-cols-3">
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Loan parameters</CardTitle>
            <CardDescription>Adjust the sliders to see your EMI update instantly</CardDescription>
          </CardHeader>
          <CardContent className="space-y-8">
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <Label>Loan amount</Label>
                <span className="font-medium">{formatCurrency(principal)}</span>
              </div>
              <input
                type="range"
                min={5000}
                max={200000}
                step={1000}
                value={principal}
                onChange={(e) => setPrincipal(Number(e.target.value))}
                className="w-full accent-[hsl(258,90%,66%)]"
              />
            </div>

            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <Label>Interest rate (p.a.)</Label>
                <span className="font-medium">{formatPercent(rate)}</span>
              </div>
              <input
                type="range"
                min={6}
                max={24}
                step={0.1}
                value={rate}
                onChange={(e) => setRate(Number(e.target.value))}
                className="w-full accent-[hsl(199,89%,58%)]"
              />
            </div>

            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <Label>Tenure</Label>
                <span className="font-medium">{months} months</span>
              </div>
              <input
                type="range"
                min={3}
                max={36}
                step={1}
                value={months}
                onChange={(e) => setMonths(Number(e.target.value))}
                className="w-full accent-[hsl(283,70%,62%)]"
              />
            </div>

            <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
              <div className="rounded-xl bg-secondary/40 p-4">
                <p className="text-xs text-muted-foreground">Monthly EMI</p>
                <p className="mt-1 font-display text-xl font-semibold text-primary">{formatCurrency(emi)}</p>
              </div>
              <div className="rounded-xl bg-secondary/40 p-4">
                <p className="text-xs text-muted-foreground">Total interest</p>
                <p className="mt-1 font-display text-xl font-semibold">{formatCurrency(totalInterest)}</p>
              </div>
              <div className="rounded-xl bg-secondary/40 p-4">
                <p className="text-xs text-muted-foreground">Total payment</p>
                <p className="mt-1 font-display text-xl font-semibold">{formatCurrency(totalPayment)}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <SplitPieChart title="Payment breakdown" description="Principal vs interest" data={pieData} />
      </div>
    </div>
  )
}

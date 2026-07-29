import { Lightbulb } from 'lucide-react'
import PageHeader from '@/components/common/PageHeader'
import CareerScoreGauge from '@/pages/Dashboard/Employee/widgets/CareerScoreGauge'
import TrendLineChart from '@/components/charts/TrendLineChart'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { useCareerScore } from '@/hooks/useEmployeeData'

const SUGGESTIONS = [
  'Maintain on-time EMI payments for 3 more cycles to unlock the next tier.',
  'Your employment stability score is strong — tenure over 2 years boosts this significantly.',
  'Avoid applying for multiple loans within the same quarter; it can temporarily lower your score.',
]

export default function CareerScorePage() {
  const { data, isLoading } = useCareerScore()

  return (
    <div>
      <PageHeader title="Career Credit Score™" description="An AI-scored measure of your financial and employment health." />

      <div className="grid grid-cols-1 gap-5 lg:grid-cols-3">
        <CareerScoreGauge score={data?.current} riskLevel={data?.riskLevel} />

        <div className="lg:col-span-2 space-y-5">
          {!isLoading && (
            <TrendLineChart title="Score history" description="Last 6 months" data={data?.history || []} dataKey="score" height={240} />
          )}

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Lightbulb className="h-4 w-4 text-warning" /> Improvement suggestions
              </CardTitle>
              <CardDescription>Personalized, based on your latest activity</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              {SUGGESTIONS.map((s, i) => (
                <div key={i} className="rounded-xl bg-secondary/30 px-4 py-3 text-sm">
                  {s}
                </div>
              ))}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

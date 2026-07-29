import { useParams } from 'react-router-dom'
import { CalendarClock, CheckCircle2, CircleDashed, FileText } from 'lucide-react'
import PageHeader from '@/components/common/PageHeader'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import StatusBadge from '@/components/common/StatusBadge'
import { formatCurrency, formatDate } from '@/utils/format'

const TIMELINE = [
  { label: 'Application submitted', date: '2026-07-21', done: true },
  { label: 'Documents verified', date: '2026-07-22', done: true },
  { label: 'Eligibility & risk scoring', date: '2026-07-22', done: true },
  { label: 'Approval decision', date: '2026-07-23', done: false },
  { label: 'Disbursement', date: null, done: false },
]

export default function LoanDetails() {
  const { id } = useParams()

  return (
    <div>
      <PageHeader title={`Loan ${id}`} description="Full details and repayment timeline for this application." />

      <div className="grid grid-cols-1 gap-5 lg:grid-cols-3">
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FileText className="h-4 w-4 text-primary" /> Timeline
            </CardTitle>
            <CardDescription>Live status of your application</CardDescription>
          </CardHeader>
          <CardContent>
            <ol className="space-y-6">
              {TIMELINE.map((item, idx) => (
                <li key={item.label} className="flex gap-4">
                  <div className="flex flex-col items-center">
                    <div
                      className={`flex h-8 w-8 items-center justify-center rounded-full ${
                        item.done ? 'bg-primary text-primary-foreground' : 'bg-secondary text-muted-foreground'
                      }`}
                    >
                      {item.done ? <CheckCircle2 className="h-4 w-4" /> : <CircleDashed className="h-4 w-4" />}
                    </div>
                    {idx < TIMELINE.length - 1 && <div className="mt-1 h-full w-0.5 flex-1 bg-border" />}
                  </div>
                  <div className="pb-2">
                    <p className="text-sm font-medium">{item.label}</p>
                    <p className="text-xs text-muted-foreground">{item.date ? formatDate(item.date) : 'Pending'}</p>
                  </div>
                </li>
              ))}
            </ol>
          </CardContent>
        </Card>

        <div className="space-y-5">
          <Card>
            <CardHeader>
              <CardTitle>Summary</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3 text-sm">
              <div className="flex justify-between">
                <span className="text-muted-foreground">Status</span>
                <StatusBadge status="pending" />
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Amount</span>
                <span className="font-medium">{formatCurrency(64000)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Tenure</span>
                <span className="font-medium">18 months</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Interest rate</span>
                <span className="font-medium">13.4% p.a.</span>
              </div>
              <div className="flex items-center gap-2 pt-2 text-xs text-muted-foreground">
                <CalendarClock className="h-3.5 w-3.5" /> Next update expected within 24 hours
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

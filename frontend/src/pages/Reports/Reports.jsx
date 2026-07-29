import { useState } from 'react'
import { Download, FileBarChart, Loader2, Plus } from 'lucide-react'
import PageHeader from '@/components/common/PageHeader'
import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import DataTable from '@/components/tables/DataTable'
import StatusBadge from '@/components/common/StatusBadge'
import { toast } from '@/hooks/useToast'
import { formatDate } from '@/utils/format'

const INITIAL_REPORTS = [
  { id: 'RPT-104', name: 'Monthly Payroll Summary', type: 'Payroll', date: '2026-07-01', status: 'success' },
  { id: 'RPT-103', name: 'Loan Portfolio Report', type: 'Loans', date: '2026-06-28', status: 'success' },
  { id: 'RPT-102', name: 'Financial Wellness Cohort', type: 'Wellness', date: '2026-06-15', status: 'success' },
  { id: 'RPT-101', name: 'Fraud Detection Audit', type: 'Risk', date: '2026-06-01', status: 'warning' },
]

const columns = [
  { key: 'id', label: 'Report ID' },
  { key: 'name', label: 'Name', render: (r) => <span className="flex items-center gap-2"><FileBarChart className="h-4 w-4 text-muted-foreground" />{r.name}</span> },
  { key: 'type', label: 'Type' },
  { key: 'date', label: 'Generated on', render: (r) => formatDate(r.date) },
  { key: 'status', label: 'Status', render: (r) => <StatusBadge status={r.status} /> },
  {
    key: 'action',
    label: '',
    render: () => (
      <button className="flex items-center gap-1 text-sm text-primary hover:underline">
        <Download className="h-3.5 w-3.5" /> Download
      </button>
    ),
  },
]

export default function Reports() {
  const [reports, setReports] = useState(INITIAL_REPORTS)
  const [generating, setGenerating] = useState(false)

  function generateReport() {
    setGenerating(true)
    setTimeout(() => {
      setReports((prev) => [
        { id: `RPT-${105 + prev.length}`, name: 'Custom Analytics Export', type: 'Analytics', date: new Date().toISOString(), status: 'success' },
        ...prev,
      ])
      setGenerating(false)
      toast({ title: 'Report generated', description: 'Available for download now.', variant: 'success' })
    }, 1400)
  }

  return (
    <div>
      <PageHeader
        title="Reports"
        description="Generate and download reports across payroll, loans, and risk."
        actions={
          <Button variant="aurora" onClick={generateReport} disabled={generating}>
            {generating ? <Loader2 className="h-4 w-4 animate-spin" /> : <Plus className="h-4 w-4" />}
            Generate report
          </Button>
        }
      />
      <Card>
        <CardContent className="p-5">
          <DataTable columns={columns} data={reports} />
        </CardContent>
      </Card>
    </div>
  )
}

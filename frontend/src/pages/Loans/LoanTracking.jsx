import { Link } from 'react-router-dom'
import PageHeader from '@/components/common/PageHeader'
import { Card, CardContent } from '@/components/ui/card'
import { TableSkeleton } from '@/components/common/Skeletons'
import DataTable from '@/components/tables/DataTable'
import StatusBadge from '@/components/common/StatusBadge'
import { Button } from '@/components/ui/button'
import { useLoans } from '@/hooks/useLoans'
import { formatCurrency, formatDate } from '@/utils/format'
import { CreditCard, Eye } from 'lucide-react'
import { ROUTES } from '@/constants'

const columns = [
  { key: 'id', label: 'Loan ID', sortable: true },
  { key: 'type', label: 'Type' },
  { key: 'amount', label: 'Amount', sortable: true, render: (r) => formatCurrency(r.amount) },
  { key: 'date', label: 'Applied on', sortable: true, render: (r) => formatDate(r.date) },
  { key: 'status', label: 'Status', render: (r) => <StatusBadge status={r.status} /> },
  {
    key: 'action',
    label: '',
    render: (r) => (
      <Link to={`/loans/${r.id}`} className="flex items-center gap-1 text-sm text-primary hover:underline">
        <Eye className="h-3.5 w-3.5" /> View
      </Link>
    ),
  },
]

export default function LoanTracking() {
  const { data, isLoading } = useLoans()

  return (
    <div>
      <PageHeader
        title="Loan tracking"
        description="All your loan applications, past and present."
        actions={
          <Button asChild variant="aurora">
            <Link to={ROUTES.LOAN_APPLICATION}>
              <CreditCard className="h-4 w-4" /> New application
            </Link>
          </Button>
        }
      />

      <Card>
        <CardContent className="p-5">
          {isLoading ? <TableSkeleton /> : <DataTable columns={columns} data={data} />}
        </CardContent>
      </Card>
    </div>
  )
}

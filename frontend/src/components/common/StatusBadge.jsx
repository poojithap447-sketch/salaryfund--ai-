import { Badge } from '@/components/ui/badge'

const STATUS_MAP = {
  pending: { variant: 'warning', label: 'Pending' },
  approved: { variant: 'success', label: 'Approved' },
  rejected: { variant: 'danger', label: 'Rejected' },
  disbursed: { variant: 'success', label: 'Disbursed' },
  active: { variant: 'default', label: 'Active' },
  closed: { variant: 'secondary', label: 'Closed' },
  synced: { variant: 'success', label: 'Synced' },
  info: { variant: 'default', label: 'Info' },
  warning: { variant: 'warning', label: 'Warning' },
  success: { variant: 'success', label: 'Success' },
}

export default function StatusBadge({ status }) {
  const config = STATUS_MAP[status] || { variant: 'secondary', label: status }
  return <Badge variant={config.variant}>{config.label}</Badge>
}

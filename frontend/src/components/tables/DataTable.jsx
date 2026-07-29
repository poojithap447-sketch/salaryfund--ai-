import { useMemo, useState } from 'react'
import { ArrowUpDown } from 'lucide-react'
import { cn } from '@/utils/cn'
import EmptyState from '@/components/common/EmptyState'

export default function DataTable({ columns, data, emptyMessage = 'No records found.' }) {
  const [sort, setSort] = useState({ key: null, dir: 'asc' })

  const sortedData = useMemo(() => {
    if (!sort.key) return data
    return [...data].sort((a, b) => {
      const av = a[sort.key]
      const bv = b[sort.key]
      if (av === bv) return 0
      const result = av > bv ? 1 : -1
      return sort.dir === 'asc' ? result : -result
    })
  }, [data, sort])

  function toggleSort(key) {
    setSort((prev) => (prev.key === key ? { key, dir: prev.dir === 'asc' ? 'desc' : 'asc' } : { key, dir: 'asc' }))
  }

  if (!data || data.length === 0) return <EmptyState title="No data yet" description={emptyMessage} />

  return (
    <div className="overflow-x-auto rounded-2xl border border-border">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-border bg-secondary/30">
            {columns.map((col) => (
              <th key={col.key} className="px-4 py-3 text-left font-medium text-muted-foreground">
                {col.sortable ? (
                  <button onClick={() => toggleSort(col.key)} className="flex items-center gap-1 hover:text-foreground">
                    {col.label}
                    <ArrowUpDown className="h-3 w-3" />
                  </button>
                ) : (
                  col.label
                )}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {sortedData.map((row, idx) => (
            <tr key={row.id || idx} className={cn('border-b border-border last:border-0 hover:bg-secondary/20 transition-colors')}>
              {columns.map((col) => (
                <td key={col.key} className="px-4 py-3">
                  {col.render ? col.render(row) : row[col.key]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export function formatCurrency(value, currency = 'INR') {
  if (value === null || value === undefined || Number.isNaN(value)) return '—'
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency,
    maximumFractionDigits: 0,
  }).format(value)
}

export function formatCompactNumber(value) {
  if (value === null || value === undefined) return '—'
  return new Intl.NumberFormat('en-IN', { notation: 'compact', maximumFractionDigits: 1 }).format(value)
}

export function formatDate(date, opts = {}) {
  if (!date) return '—'
  return new Intl.DateTimeFormat('en-IN', { day: 'numeric', month: 'short', year: 'numeric', ...opts }).format(
    new Date(date)
  )
}

export function formatPercent(value, digits = 1) {
  if (value === null || value === undefined) return '—'
  return `${value.toFixed(digits)}%`
}

export function initials(name = '') {
  return name
    .split(' ')
    .map((p) => p[0])
    .slice(0, 2)
    .join('')
    .toUpperCase()
}

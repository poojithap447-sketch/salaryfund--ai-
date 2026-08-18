import { Area, AreaChart, ResponsiveContainer, Tooltip, XAxis, YAxis, CartesianGrid } from 'recharts'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

function AreaTooltip({ active, payload, label, valueFormatter }) {
  if (!active || !payload?.length) return null
  const item = payload[0]
  return (
    <div className="rounded-xl border border-white/15 bg-slate-900/95 px-3.5 py-2.5 shadow-2xl backdrop-blur-md">
      <p className="mb-1 text-[11px] font-semibold text-slate-400 uppercase tracking-wider">{label}</p>
      <div className="flex items-center gap-2">
        <span className="h-2.5 w-2.5 rounded-full shrink-0" style={{ backgroundColor: item.color || 'hsl(199 89% 58%)' }} />
        <span className="text-xs font-medium text-slate-300">{item.name || item.dataKey}:</span>
        <span className="text-xs font-bold text-white">{valueFormatter ? valueFormatter(item.value) : item.value}</span>
      </div>
    </div>
  )
}

export default function TrendAreaChart({ title, description, data, dataKey, xKey = 'month', color = 'hsl(199 89% 58%)', valueFormatter, height = 260 }) {
  const gradientId = `gradient-${dataKey}`
  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
        {description && <CardDescription>{description}</CardDescription>}
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={height}>
          <AreaChart data={data} margin={{ top: 4, right: 8, left: -16, bottom: 0 }}>
            <defs>
              <linearGradient id={gradientId} x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor={color} stopOpacity={0.35} />
                <stop offset="100%" stopColor={color} stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" vertical={false} />
            <XAxis dataKey={xKey} tick={{ fontSize: 12, fill: 'hsl(var(--muted-foreground))' }} axisLine={false} tickLine={false} />
            <YAxis tick={{ fontSize: 12, fill: 'hsl(var(--muted-foreground))' }} axisLine={false} tickLine={false} width={48} />
            <Tooltip content={<AreaTooltip valueFormatter={valueFormatter} />} />
            <Area type="monotone" dataKey={dataKey} stroke={color} strokeWidth={2.5} fill={`url(#${gradientId})`} />
          </AreaChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}


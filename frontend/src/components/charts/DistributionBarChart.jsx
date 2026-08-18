import { Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis, CartesianGrid, Cell } from 'recharts'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

const PALETTE = ['hsl(258 90% 66%)', 'hsl(283 70% 62%)', 'hsl(199 89% 58%)', 'hsl(152 55% 48%)', 'hsl(38 92% 55%)']

function BarTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null
  const item = payload[0]
  const fillColor = item.payload?.fill || item.color || PALETTE[0]
  return (
    <div className="rounded-xl border border-white/15 bg-slate-900/95 px-3.5 py-2.5 shadow-2xl backdrop-blur-md">
      <p className="mb-1 text-[11px] font-semibold text-slate-400 uppercase tracking-wider">{label}</p>
      <div className="flex items-center gap-2">
        <span className="h-2.5 w-2.5 rounded-full shrink-0" style={{ backgroundColor: fillColor }} />
        <span className="text-xs font-medium text-slate-300">{item.name || 'Count'}:</span>
        <span className="text-xs font-bold text-white">{item.value}</span>
      </div>
    </div>
  )
}

export default function DistributionBarChart({ title, description, data, dataKey, xKey, height = 280 }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
        {description && <CardDescription>{description}</CardDescription>}
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={height}>
          <BarChart data={data} margin={{ top: 4, right: 8, left: -16, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" vertical={false} />
            <XAxis dataKey={xKey} tick={{ fontSize: 12, fill: 'hsl(var(--muted-foreground))' }} axisLine={false} tickLine={false} />
            <YAxis tick={{ fontSize: 12, fill: 'hsl(var(--muted-foreground))' }} axisLine={false} tickLine={false} width={40} />
            <Tooltip content={<BarTooltip />} />
            <Bar dataKey={dataKey} radius={[8, 8, 0, 0]}>
              {data.map((_, i) => (
                <Cell key={i} fill={PALETTE[i % PALETTE.length]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}


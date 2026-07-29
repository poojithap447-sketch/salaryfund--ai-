import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis, CartesianGrid } from 'recharts'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

function ChartTooltip({ active, payload, label, valueFormatter }) {
  if (!active || !payload?.length) return null
  return (
    <div className="glass-raised rounded-lg px-3 py-2 text-xs shadow-xl">
      <p className="font-medium text-muted-foreground">{label}</p>
      {payload.map((p) => (
        <p key={p.dataKey} className="font-semibold" style={{ color: p.color }}>
          {valueFormatter ? valueFormatter(p.value) : p.value}
        </p>
      ))}
    </div>
  )
}

export default function TrendLineChart({ title, description, data, dataKey, xKey = 'month', color = 'hsl(258 90% 66%)', valueFormatter, height = 260 }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
        {description && <CardDescription>{description}</CardDescription>}
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={height}>
          <LineChart data={data} margin={{ top: 4, right: 8, left: -16, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" vertical={false} />
            <XAxis dataKey={xKey} tick={{ fontSize: 12, fill: 'hsl(var(--muted-foreground))' }} axisLine={false} tickLine={false} />
            <YAxis tick={{ fontSize: 12, fill: 'hsl(var(--muted-foreground))' }} axisLine={false} tickLine={false} width={48} />
            <Tooltip content={<ChartTooltip valueFormatter={valueFormatter} />} />
            <Line type="monotone" dataKey={dataKey} stroke={color} strokeWidth={2.5} dot={{ r: 3, fill: color }} activeDot={{ r: 5 }} />
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}

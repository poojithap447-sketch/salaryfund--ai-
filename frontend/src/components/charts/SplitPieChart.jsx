import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip, Legend } from 'recharts'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

const PALETTE = ['hsl(258 90% 66%)', 'hsl(283 70% 62%)', 'hsl(199 89% 58%)', 'hsl(38 92% 55%)']

function PieTooltip({ active, payload }) {
  if (!active || !payload?.length) return null
  const item = payload[0]
  const fillColor = item.payload?.fill || item.color || PALETTE[0]
  return (
    <div className="rounded-xl border border-white/15 bg-slate-900/95 px-3.5 py-2.5 shadow-2xl backdrop-blur-md">
      <div className="flex items-center gap-2">
        <span className="h-2.5 w-2.5 rounded-full shrink-0" style={{ backgroundColor: fillColor }} />
        <span className="text-xs font-medium text-slate-300">{item.name}:</span>
        <span className="text-xs font-bold text-white">{item.value}</span>
      </div>
    </div>
  )
}

export default function SplitPieChart({ title, description, data, height = 260 }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
        {description && <CardDescription>{description}</CardDescription>}
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={height}>
          <PieChart>
            <Pie data={data} dataKey="value" nameKey="name" innerRadius={55} outerRadius={90} paddingAngle={3}>
              {data.map((_, i) => (
                <Cell key={i} fill={PALETTE[i % PALETTE.length]} stroke="transparent" />
              ))}
            </Pie>
            <Tooltip content={<PieTooltip />} />
            <Legend
              iconType="circle"
              iconSize={8}
              formatter={(value) => <span className="text-xs text-muted-foreground">{value}</span>}
            />
          </PieChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}


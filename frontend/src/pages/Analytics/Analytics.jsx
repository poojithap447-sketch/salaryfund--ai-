import PageHeader from '@/components/common/PageHeader'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import TrendAreaChart from '@/components/charts/TrendAreaChart'
import DistributionBarChart from '@/components/charts/DistributionBarChart'
import SplitPieChart from '@/components/charts/SplitPieChart'
import { revenueTrend, riskDistribution, loanTypeSplit, departmentAnalytics } from '@/utils/mockData'
import { formatCurrency } from '@/utils/format'

export default function Analytics() {
  return (
    <div>
      <PageHeader title="Analytics" description="Cross-cutting insight into loans, risk, and revenue." />

      <Tabs defaultValue="loans">
        <TabsList>
          <TabsTrigger value="loans">Loans</TabsTrigger>
          <TabsTrigger value="risk">Risk</TabsTrigger>
          <TabsTrigger value="revenue">Revenue</TabsTrigger>
        </TabsList>

        <TabsContent value="loans">
          <div className="grid grid-cols-1 gap-5 lg:grid-cols-3">
            <div className="lg:col-span-2">
              <DistributionBarChart title="Loans by department" data={departmentAnalytics} dataKey="activeLoans" xKey="department" />
            </div>
            <SplitPieChart title="Loan type mix" data={loanTypeSplit} />
          </div>
        </TabsContent>

        <TabsContent value="risk">
          <DistributionBarChart title="Risk distribution" description="Active loans by risk tier" data={riskDistribution} dataKey="count" xKey="risk" height={320} />
        </TabsContent>

        <TabsContent value="revenue">
          <TrendAreaChart title="Revenue trend" description="Last 6 months" data={revenueTrend} dataKey="revenue" valueFormatter={formatCurrency} height={320} />
        </TabsContent>
      </Tabs>
    </div>
  )
}

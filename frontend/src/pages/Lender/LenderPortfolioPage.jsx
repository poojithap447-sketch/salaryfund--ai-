import { useState } from 'react'
import { Landmark, Search, ShieldCheck, CheckCircle2, XCircle, ArrowUpRight, DollarSign, Wallet, Percent, ShieldAlert } from 'lucide-react'
import PageHeader from '@/components/common/PageHeader'
import StatCard from '@/components/common/StatCard'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { mockLenderPortfolio, lenderSummary } from '@/utils/mockData'
import { formatCurrency, formatPercent } from '@/utils/format'
import { toast } from '@/hooks/useToast'

export default function LenderPortfolioPage() {
  const [portfolio, setPortfolio] = useState(mockLenderPortfolio)
  const [search, setSearch] = useState('')
  const [riskFilter, setRiskFilter] = useState('ALL')
  const [statusFilter, setStatusFilter] = useState('ALL')

  const filteredPortfolio = portfolio.filter((loan) => {
    const matchesSearch =
      loan.id.toLowerCase().includes(search.toLowerCase()) ||
      loan.borrower_name.toLowerCase().includes(search.toLowerCase()) ||
      loan.employee_code.toLowerCase().includes(search.toLowerCase())
    const matchesRisk = riskFilter === 'ALL' || loan.risk_tier === riskFilter
    const matchesStatus = statusFilter === 'ALL' || loan.status === statusFilter
    return matchesSearch && matchesRisk && matchesStatus
  })

  function handleApprove(loanId, borrowerName) {
    setPortfolio(
      portfolio.map((item) =>
        item.id === loanId ? { ...item, status: 'Disbursed' } : item
      )
    )
    toast({
      title: 'Loan Disbursed Successfully!',
      description: `Disbursement approved for ${borrowerName} (${loanId}). Capital transferred to escrow.`,
      variant: 'success',
    })
  }

  function handleReject(loanId, borrowerName) {
    setPortfolio(
      portfolio.map((item) =>
        item.id === loanId ? { ...item, status: 'Underwriting Rejected' } : item
      )
    )
    toast({
      title: 'Application Rejected',
      description: `Loan ${loanId} for ${borrowerName} was marked as rejected.`,
      variant: 'destructive',
    })
  }

  return (
    <div>
      <PageHeader
        title="NBFC Loan Portfolio & Capital Underwriting"
        description="Review active loans, analyze borrower risk scores, and disburse capital into salary escrow."
      />

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard label="Total Portfolio Value" value={formatCurrency(lenderSummary.portfolioValue)} icon={Landmark} accent="primary" />
        <StatCard label="Active Loans Disbursed" value={lenderSummary.activeLoans} icon={Wallet} accent="accent" />
        <StatCard label="Average Yield (P.A.)" value={formatPercent(lenderSummary.avgInterestRate)} icon={Percent} accent="success" />
        <StatCard label="Pending Underwriting" value={portfolio.filter((p) => p.status.includes('Pending')).length} icon={ShieldAlert} accent="warning" />
      </div>

      <Card className="mt-6">
        <CardHeader className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <CardTitle>Capital Allocation & Loan Stream</CardTitle>
            <CardDescription>Live list of underwritten and pending loans across partner employers.</CardDescription>
          </div>
          <div className="flex flex-col sm:flex-row items-center gap-3">
            <div className="relative w-full sm:w-64">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search loan ID, borrower, key…"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="pl-9"
              />
            </div>
            <Select value={riskFilter} onValueChange={setRiskFilter}>
              <SelectTrigger className="w-full sm:w-36">
                <SelectValue placeholder="Risk Tier" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="ALL">All Risks</SelectItem>
                <SelectItem value="Low">Low Risk</SelectItem>
                <SelectItem value="Medium">Medium Risk</SelectItem>
                <SelectItem value="High">High Risk</SelectItem>
              </SelectContent>
            </Select>
            <Select value={statusFilter} onValueChange={setStatusFilter}>
              <SelectTrigger className="w-full sm:w-44">
                <SelectValue placeholder="Status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="ALL">All Statuses</SelectItem>
                <SelectItem value="Disbursed">Disbursed</SelectItem>
                <SelectItem value="Underwriting Approved">Underwriting Approved</SelectItem>
                <SelectItem value="Pending NBFC Approval">Pending Approval</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="border-b border-border text-xs font-semibold uppercase text-muted-foreground">
                <tr>
                  <th className="py-3 px-3">Loan Ref & Date</th>
                  <th className="py-3 px-3">Borrower (Key)</th>
                  <th className="py-3 px-3">Principal Amount</th>
                  <th className="py-3 px-3">Interest / EMI</th>
                  <th className="py-3 px-3">Career Score™</th>
                  <th className="py-3 px-3">Risk Tier</th>
                  <th className="py-3 px-3">Status</th>
                  <th className="py-3 px-3 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border/40">
                {filteredPortfolio.map((loan) => (
                  <tr key={loan.id} className="hover:bg-secondary/20 transition-colors">
                    <td className="py-3.5 px-3">
                      <div className="font-mono text-xs font-semibold text-primary">{loan.id}</div>
                      <div className="text-[11px] text-muted-foreground">{loan.disbursement_date}</div>
                    </td>
                    <td className="py-3.5 px-3">
                      <div className="font-medium text-foreground">{loan.borrower_name}</div>
                      <div className="flex items-center gap-1.5 mt-0.5">
                        <span className="font-mono text-[10px] px-1.5 py-0.2 rounded bg-secondary text-muted-foreground border border-border">
                          {loan.employee_code}
                        </span>
                        <span className="text-[11px] text-muted-foreground">{loan.employer_name}</span>
                      </div>
                    </td>
                    <td className="py-3.5 px-3 font-semibold">{formatCurrency(loan.principal_amount)}</td>
                    <td className="py-3.5 px-3">
                      <div className="text-xs font-medium">{loan.interest_rate}% p.a.</div>
                      <div className="text-[11px] text-muted-foreground">{formatCurrency(loan.monthly_emi)} / mo</div>
                    </td>
                    <td className="py-3.5 px-3">
                      <div className="flex items-center gap-1.5">
                        <ShieldCheck className="h-4 w-4 text-emerald-400" />
                        <span className="font-semibold text-foreground">{loan.career_score}</span>
                      </div>
                    </td>
                    <td className="py-3.5 px-3">
                      <Badge
                        variant={
                          loan.risk_tier === 'Low' ? 'success' : loan.risk_tier === 'Medium' ? 'warning' : 'danger'
                        }
                      >
                        {loan.risk_tier} Risk
                      </Badge>
                    </td>
                    <td className="py-3.5 px-3">
                      <Badge
                        variant={
                          loan.status === 'Disbursed'
                            ? 'success'
                            : loan.status.includes('Pending')
                            ? 'warning'
                            : 'accent'
                        }
                      >
                        {loan.status}
                      </Badge>
                    </td>
                    <td className="py-3.5 px-3 text-right">
                      {loan.status.includes('Pending') || loan.status === 'Underwriting Approved' ? (
                        <div className="flex items-center justify-end gap-1.5">
                          <Button
                            variant="aurora"
                            size="sm"
                            className="h-7 text-xs px-2.5"
                            onClick={() => handleApprove(loan.id, loan.borrower_name)}
                          >
                            <CheckCircle2 className="mr-1 h-3.5 w-3.5" /> Disburse
                          </Button>
                          <Button
                            variant="ghost"
                            size="sm"
                            className="h-7 text-xs px-2 text-destructive hover:bg-destructive/10"
                            onClick={() => handleReject(loan.id, loan.borrower_name)}
                          >
                            <XCircle className="h-3.5 w-3.5" />
                          </Button>
                        </div>
                      ) : (
                        <Button
                          variant="ghost"
                          size="sm"
                          className="h-7 text-xs text-muted-foreground hover:text-foreground"
                          onClick={() =>
                            toast({
                              title: `Contract ${loan.id}`,
                              description: `Borrower: ${loan.borrower_name} | Disbursed: ${formatCurrency(loan.principal_amount)} at ${loan.interest_rate}% P.A.`,
                            })
                          }
                        >
                          Contract <ArrowUpRight className="ml-1 h-3 w-3" />
                        </Button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

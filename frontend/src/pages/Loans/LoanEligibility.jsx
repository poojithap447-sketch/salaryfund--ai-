import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { Link } from 'react-router-dom'
import { CheckCircle2, Gauge, Loader2 } from 'lucide-react'
import PageHeader from '@/components/common/PageHeader'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { Badge } from '@/components/ui/badge'
import { useLoanEligibility } from '@/hooks/useLoans'
import { formatCurrency, formatPercent } from '@/utils/format'
import { ROUTES } from '@/constants'

export default function LoanEligibility() {
  const { register, handleSubmit } = useForm({
    defaultValues: { monthlySalary: 128000, tenureMonths: 18, existingEmi: 5600 },
  })
  const { mutate, data: result, isPending } = useLoanEligibility()

  function onSubmit(values) {
    mutate({
      monthlySalary: Number(values.monthlySalary),
      tenureMonths: Number(values.tenureMonths),
      existingEmi: Number(values.existingEmi),
    })
  }

  return (
    <div>
      <PageHeader title="Check loan eligibility" description="Get an instant, AI-scored estimate before you apply." />

      <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Gauge className="h-4 w-4 text-primary" /> Your details
            </CardTitle>
            <CardDescription>Estimates use your latest payroll data automatically where possible.</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
              <div className="space-y-2">
                <Label>Monthly salary (₹)</Label>
                <Input type="number" {...register('monthlySalary', { required: true, min: 10000 })} />
              </div>
              <div className="space-y-2">
                <Label>Preferred tenure (months)</Label>
                <Input type="number" {...register('tenureMonths', { required: true, min: 3, max: 36 })} />
              </div>
              <div className="space-y-2">
                <Label>Existing monthly EMI (₹)</Label>
                <Input type="number" {...register('existingEmi')} />
              </div>
              <Button type="submit" variant="aurora" className="w-full" disabled={isPending}>
                {isPending && <Loader2 className="h-4 w-4 animate-spin" />}
                Check eligibility
              </Button>
            </form>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Result</CardTitle>
            <CardDescription>Powered by the eligibility engine (XGBoost + SHAP)</CardDescription>
          </CardHeader>
          <CardContent>
            {!result && !isPending && (
              <div className="flex flex-col items-center justify-center py-16 text-center text-sm text-muted-foreground">
                Fill in your details to see your estimate.
              </div>
            )}
            {isPending && (
              <div className="flex flex-col items-center justify-center gap-2 py-16 text-center text-sm text-muted-foreground">
                <Loader2 className="h-5 w-5 animate-spin" /> Scoring your eligibility…
              </div>
            )}
            {result && (
              <div className="space-y-6">
                <div className="flex items-center gap-3">
                  <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-success/10">
                    <CheckCircle2 className="h-5 w-5 text-success" />
                  </div>
                  <div>
                    <p className="font-medium">{result.eligible ? "You're eligible" : 'Not eligible right now'}</p>
                    <p className="text-xs text-muted-foreground">Confidence: {formatPercent(result.confidence * 100)}</p>
                  </div>
                </div>

                <div className="rounded-xl bg-secondary/40 p-4">
                  <p className="text-xs text-muted-foreground">Eligible amount</p>
                  <p className="font-display text-3xl font-semibold">{formatCurrency(result.eligibleAmount)}</p>
                </div>

                <div>
                  <div className="mb-1.5 flex items-center justify-between text-sm">
                    <span className="text-muted-foreground">Approval probability</span>
                    <span className="font-medium">{formatPercent(result.approvalProbability)}</span>
                  </div>
                  <Progress value={result.approvalProbability} />
                </div>

                <div className="flex items-center justify-between">
                  <span className="text-sm text-muted-foreground">Risk level</span>
                  <Badge variant="success">{result.riskLevel}</Badge>
                </div>

                <Button asChild variant="aurora" className="w-full">
                  <Link to={ROUTES.LOAN_APPLICATION}>Continue to application</Link>
                </Button>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

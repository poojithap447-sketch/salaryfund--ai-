import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { motion, AnimatePresence } from 'framer-motion'
import { ArrowLeft, ArrowRight, CheckCircle2, Loader2 } from 'lucide-react'
import PageHeader from '@/components/common/PageHeader'
import Stepper from '@/components/forms/Stepper'
import FileUpload from '@/components/forms/FileUpload'
import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { useApplyLoan } from '@/hooks/useLoans'
import { toast } from '@/hooks/useToast'
import { LOAN_TYPES } from '@/constants'
import { formatCurrency } from '@/utils/format'

const STEPS = ['Loan Type', 'Amount & Tenure', 'Purpose', 'Employment', 'Bank Details', 'Documents', 'Review']

export default function LoanApplication() {
  const navigate = useNavigate()
  const [step, setStep] = useState(0)
  const [submitted, setSubmitted] = useState(null)
  const [documents, setDocuments] = useState([])
  const { mutate, isPending } = useApplyLoan()
  const { register, handleSubmit, watch, setValue, trigger } = useForm({
    defaultValues: {
      loanType: 'salary_advance',
      amount: 30000,
      tenureMonths: 12,
      purpose: '',
      employerName: 'Nimbus Retail Pvt Ltd',
      designation: 'Senior Product Designer',
      monthlyIncome: 128000,
      bankAccount: '',
      ifsc: '',
    },
  })
  const values = watch()

  function next() {
    setStep((s) => Math.min(s + 1, STEPS.length - 1))
  }
  function back() {
    setStep((s) => Math.max(s - 1, 0))
  }

  function onFinalSubmit() {
    mutate(values, {
      onSuccess: (data) => {
        setSubmitted(data)
        toast({ title: 'Application submitted', description: `Reference ${data.id}`, variant: 'success' })
      },
    })
  }

  if (submitted) {
    return (
      <div className="mx-auto max-w-lg py-16 text-center">
        <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-success/10">
          <CheckCircle2 className="h-7 w-7 text-success" />
        </div>
        <h1 className="mt-6 font-display text-2xl font-semibold">Application submitted</h1>
        <p className="mt-2 text-muted-foreground">
          Reference <span className="font-medium text-foreground">{submitted.id}</span> is now{' '}
          <span className="capitalize">{submitted.status}</span> review. We'll notify you the moment a decision is made.
        </p>
        <Button variant="aurora" size="lg" className="mt-8" onClick={() => navigate('/loans/tracking')}>
          Track this application
        </Button>
      </div>
    )
  }

  return (
    <div>
      <PageHeader title="Apply for a loan" description="Complete each step — most applicants finish in under 3 minutes." />

      <Card className="mx-auto max-w-3xl">
        <CardContent className="p-6 sm:p-8">
          <Stepper steps={STEPS} currentStep={step} />

          <AnimatePresence mode="wait">
            <motion.div
              key={step}
              initial={{ opacity: 0, x: 16 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -16 }}
              transition={{ duration: 0.25 }}
              className="mt-8"
            >
              {step === 0 && (
                <div className="space-y-4">
                  <Label>Select loan type</Label>
                  <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
                    {LOAN_TYPES.map((type) => (
                      <button
                        key={type.value}
                        type="button"
                        onClick={() => setValue('loanType', type.value)}
                        className={`rounded-xl border-2 p-4 text-left transition-colors ${
                          values.loanType === type.value ? 'border-primary bg-primary/5' : 'border-border hover:border-primary/40'
                        }`}
                      >
                        <p className="font-medium">{type.label}</p>
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {step === 1 && (
                <div className="space-y-5">
                  <div className="space-y-2">
                    <Label>Loan amount: {formatCurrency(values.amount)}</Label>
                    <input
                      type="range"
                      min={5000}
                      max={100000}
                      step={1000}
                      {...register('amount', { valueAsNumber: true })}
                      className="w-full accent-[hsl(258,90%,66%)]"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label>Tenure (months)</Label>
                    <Select defaultValue={String(values.tenureMonths)} onValueChange={(v) => setValue('tenureMonths', Number(v))}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {[3, 6, 12, 18, 24, 36].map((m) => (
                          <SelectItem key={m} value={String(m)}>
                            {m} months
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              )}

              {step === 2 && (
                <div className="space-y-2">
                  <Label htmlFor="purpose">What's this loan for?</Label>
                  <textarea
                    id="purpose"
                    {...register('purpose')}
                    rows={5}
                    placeholder="E.g. Medical emergency, home repairs, education fees…"
                    className="flex w-full rounded-xl border border-input bg-surface/60 px-4 py-3 text-sm focus-ring placeholder:text-muted-foreground"
                  />
                </div>
              )}

              {step === 3 && (
                <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                  <div className="space-y-2">
                    <Label>Employer</Label>
                    <Input {...register('employerName')} />
                  </div>
                  <div className="space-y-2">
                    <Label>Designation</Label>
                    <Input {...register('designation')} />
                  </div>
                  <div className="space-y-2 sm:col-span-2">
                    <Label>Monthly income (₹)</Label>
                    <Input type="number" {...register('monthlyIncome')} />
                  </div>
                </div>
              )}

              {step === 4 && (
                <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                  <div className="space-y-2">
                    <Label>Bank account number</Label>
                    <Input {...register('bankAccount', { required: true })} />
                  </div>
                  <div className="space-y-2">
                    <Label>IFSC code</Label>
                    <Input {...register('ifsc', { required: true })} />
                  </div>
                </div>
              )}

              {step === 5 && (
                <FileUpload label="Upload salary slip & ID proof" multiple onFilesChange={setDocuments} />
              )}

              {step === 6 && (
                <div className="space-y-3">
                  {[
                    ['Loan type', LOAN_TYPES.find((t) => t.value === values.loanType)?.label],
                    ['Amount', formatCurrency(values.amount)],
                    ['Tenure', `${values.tenureMonths} months`],
                    ['Employer', values.employerName],
                    ['Documents', `${documents.length} file(s) attached`],
                  ].map(([label, value]) => (
                    <div key={label} className="flex items-center justify-between rounded-xl bg-secondary/30 px-4 py-3 text-sm">
                      <span className="text-muted-foreground">{label}</span>
                      <span className="font-medium">{value}</span>
                    </div>
                  ))}
                </div>
              )}
            </motion.div>
          </AnimatePresence>

          <div className="mt-8 flex items-center justify-between">
            <Button variant="ghost" onClick={back} disabled={step === 0}>
              <ArrowLeft className="h-4 w-4" /> Back
            </Button>
            {step < STEPS.length - 1 ? (
              <Button variant="aurora" onClick={next}>
                Continue <ArrowRight className="h-4 w-4" />
              </Button>
            ) : (
              <Button variant="aurora" onClick={handleSubmit(onFinalSubmit)} disabled={isPending}>
                {isPending && <Loader2 className="h-4 w-4 animate-spin" />}
                Submit application
              </Button>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

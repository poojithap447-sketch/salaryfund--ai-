import { useForm } from 'react-hook-form'
import { LifeBuoy, Mail, MessageSquare } from 'lucide-react'
import PageHeader from '@/components/common/PageHeader'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Button } from '@/components/ui/button'
import { toast } from '@/hooks/useToast'

const FAQS = [
  { q: 'How is my Career Credit Score calculated?', a: 'It combines employment stability, salary growth, attendance, and repayment behavior into a 300–900 score.' },
  { q: 'How fast is disbursement after approval?', a: 'Most approved loans are disbursed to your linked bank account within minutes.' },
  { q: 'Can I repay my loan early?', a: 'Yes, early repayment is supported with no prepayment penalty on salary advances.' },
]

export default function Support() {
  const { register, handleSubmit, reset } = useForm()

  function onSubmit() {
    toast({ title: 'Message sent', description: "Our team will respond within 24 hours.", variant: 'success' })
    reset()
  }

  return (
    <div>
      <PageHeader title="Support" description="Get help with loans, payroll sync, or your account." />

      <div className="grid grid-cols-1 gap-5 lg:grid-cols-3">
        <div className="lg:col-span-2 space-y-3">
          {FAQS.map((f) => (
            <Card key={f.q}>
              <CardContent className="p-5">
                <p className="flex items-center gap-2 font-medium">
                  <LifeBuoy className="h-4 w-4 text-primary" /> {f.q}
                </p>
                <p className="mt-1.5 text-sm text-muted-foreground">{f.a}</p>
              </CardContent>
            </Card>
          ))}
        </div>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <MessageSquare className="h-4 w-4 text-primary" /> Contact us
            </CardTitle>
            <CardDescription>We typically respond within a day</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <div className="space-y-2">
                <Label>Subject</Label>
                <Input {...register('subject', { required: true })} />
              </div>
              <div className="space-y-2">
                <Label>Message</Label>
                <textarea
                  rows={4}
                  {...register('message', { required: true })}
                  className="flex w-full rounded-xl border border-input bg-surface/60 px-4 py-3 text-sm focus-ring"
                />
              </div>
              <Button type="submit" variant="aurora" className="w-full">
                <Mail className="h-4 w-4" /> Send message
              </Button>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

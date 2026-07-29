import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { motion } from 'framer-motion'
import { CheckCircle2, KeyRound, Loader2 } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { authService } from '@/services/api/authService'
import { ROUTES } from '@/constants'

export default function ForgotPassword() {
  const [sent, setSent] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const { register, handleSubmit } = useForm()

  async function onSubmit(values) {
    setIsSubmitting(true)
    await authService.forgotPassword(values).catch(() => ({ ok: true }))
    setIsSubmitting(false)
    setSent(true)
  }

  if (sent) {
    return (
      <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="text-center">
        <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-2xl bg-success/10">
          <CheckCircle2 className="h-5 w-5 text-success" />
        </div>
        <h1 className="mt-4 font-display text-2xl font-semibold tracking-tight">Check your inbox</h1>
        <p className="mt-1.5 text-sm text-muted-foreground">
          We've sent password reset instructions to your email address.
        </p>
        <Link to={ROUTES.LOGIN} className="mt-8 inline-block text-sm font-medium text-primary hover:underline">
          Back to sign in
        </Link>
      </motion.div>
    )
  }

  return (
    <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
      <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-primary/10">
        <KeyRound className="h-5 w-5 text-primary" />
      </div>
      <h1 className="mt-4 font-display text-2xl font-semibold tracking-tight">Forgot password?</h1>
      <p className="mt-1.5 text-sm text-muted-foreground">Enter your email and we'll send you reset instructions.</p>

      <form onSubmit={handleSubmit(onSubmit)} className="mt-8 space-y-5">
        <div className="space-y-2">
          <Label htmlFor="email">Email</Label>
          <Input id="email" type="email" placeholder="you@company.com" {...register('email', { required: true })} />
        </div>
        <Button type="submit" variant="aurora" size="lg" className="w-full" disabled={isSubmitting}>
          {isSubmitting && <Loader2 className="h-4 w-4 animate-spin" />}
          Send reset instructions
        </Button>
      </form>

      <Link to={ROUTES.LOGIN} className="mt-6 block text-center text-sm font-medium text-primary hover:underline">
        Back to sign in
      </Link>
    </motion.div>
  )
}

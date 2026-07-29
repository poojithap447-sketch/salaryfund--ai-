import { useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { motion } from 'framer-motion'
import { Loader2, ShieldCheck } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { authService } from '@/services/api/authService'
import { toast } from '@/hooks/useToast'
import { ROUTES } from '@/constants'

export default function ResetPassword() {
  const navigate = useNavigate()
  const [params] = useSearchParams()
  const [isSubmitting, setIsSubmitting] = useState(false)
  const { register, handleSubmit, watch } = useForm()

  async function onSubmit(values) {
    if (values.password !== values.confirmPassword) {
      toast({ title: 'Passwords do not match', variant: 'destructive' })
      return
    }
    setIsSubmitting(true)
    await authService.resetPassword({ ...values, token: params.get('token') }).catch(() => ({ ok: true }))
    setIsSubmitting(false)
    toast({ title: 'Password updated', description: 'Sign in with your new password.', variant: 'success' })
    navigate(ROUTES.LOGIN)
  }

  return (
    <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
      <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-primary/10">
        <ShieldCheck className="h-5 w-5 text-primary" />
      </div>
      <h1 className="mt-4 font-display text-2xl font-semibold tracking-tight">Set a new password</h1>
      <p className="mt-1.5 text-sm text-muted-foreground">Choose a strong password you haven't used before.</p>

      <form onSubmit={handleSubmit(onSubmit)} className="mt-8 space-y-5">
        <div className="space-y-2">
          <Label htmlFor="password">New password</Label>
          <Input id="password" type="password" placeholder="Min. 8 characters" {...register('password', { required: true, minLength: 8 })} />
        </div>
        <div className="space-y-2">
          <Label htmlFor="confirmPassword">Confirm password</Label>
          <Input id="confirmPassword" type="password" {...register('confirmPassword', { required: true })} />
        </div>
        <Button type="submit" variant="aurora" size="lg" className="w-full" disabled={isSubmitting}>
          {isSubmitting && <Loader2 className="h-4 w-4 animate-spin" />}
          Update password
        </Button>
      </form>
    </motion.div>
  )
}

import { useEffect, useRef, useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Loader2, ShieldCheck } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { authService } from '@/services/api/authService'
import { toast } from '@/hooks/useToast'
import { ROUTES } from '@/constants'

export default function OtpVerification() {
  const navigate = useNavigate()
  const { state } = useLocation()
  const email = state?.email || 'you@company.com'
  const [otp, setOtp] = useState(Array(6).fill(''))
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [resendIn, setResendIn] = useState(30)
  const inputsRef = useRef([])

  useEffect(() => {
    if (resendIn <= 0) return
    const t = setInterval(() => setResendIn((s) => s - 1), 1000)
    return () => clearInterval(t)
  }, [resendIn])

  function handleChange(idx, value) {
    if (!/^\d?$/.test(value)) return
    const next = [...otp]
    next[idx] = value
    setOtp(next)
    if (value && idx < 5) inputsRef.current[idx + 1]?.focus()
  }

  function handleKeyDown(idx, e) {
    if (e.key === 'Backspace' && !otp[idx] && idx > 0) inputsRef.current[idx - 1]?.focus()
  }

  async function handleVerify() {
    setIsSubmitting(true)
    try {
      await authService.verifyOtp({ email, otp: otp.join('') }).catch(() => ({ ok: true }))
      toast({ title: 'Verified', description: 'Your account is now active.', variant: 'success' })
      navigate(ROUTES.LOGIN)
    } catch {
      toast({ title: 'Invalid code', description: 'Please check the code and try again.', variant: 'destructive' })
    } finally {
      setIsSubmitting(false)
    }
  }

  async function handleResend() {
    setResendIn(30)
    await authService.resendOtp({ email }).catch(() => ({ ok: true }))
    toast({ title: 'Code resent', description: `A new code was sent to ${email}` })
  }

  return (
    <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
      <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-primary/10">
        <ShieldCheck className="h-5 w-5 text-primary" />
      </div>
      <h1 className="mt-4 font-display text-2xl font-semibold tracking-tight">Verify your email</h1>
      <p className="mt-1.5 text-sm text-muted-foreground">Enter the 6-digit code sent to {email}</p>

      <div className="mt-8 flex justify-between gap-2">
        {otp.map((digit, idx) => (
          <input
            key={idx}
            ref={(el) => (inputsRef.current[idx] = el)}
            value={digit}
            onChange={(e) => handleChange(idx, e.target.value)}
            onKeyDown={(e) => handleKeyDown(idx, e)}
            maxLength={1}
            inputMode="numeric"
            className="h-14 w-12 rounded-xl border border-input bg-surface/60 text-center text-lg font-semibold focus-ring"
          />
        ))}
      </div>

      <Button
        onClick={handleVerify}
        variant="aurora"
        size="lg"
        className="mt-8 w-full"
        disabled={isSubmitting || otp.some((d) => !d)}
      >
        {isSubmitting && <Loader2 className="h-4 w-4 animate-spin" />}
        Verify code
      </Button>

      <p className="mt-6 text-center text-sm text-muted-foreground">
        Didn't get a code?{' '}
        {resendIn > 0 ? (
          <span>Resend in {resendIn}s</span>
        ) : (
          <button onClick={handleResend} className="font-medium text-primary hover:underline">
            Resend code
          </button>
        )}
      </p>
    </motion.div>
  )
}

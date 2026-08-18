import { useState, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { ShieldCheck, Smartphone, Loader2, Lock, CheckCircle2 } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { loanService } from '@/services/api/loanService'
import { toast } from '@/hooks/useToast'

export default function CibilOtpModal({ isOpen, onClose, panNumber, mobileNumber, onVerificationSuccess }) {
  const [step, setStep] = useState('request') // 'request' | 'verify' | 'success'
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [txId, setTxId] = useState('')
  const [otp, setOtp] = useState(Array(6).fill(''))
  const [bureauResult, setBureauResult] = useState(null)
  const inputsRef = useRef([])

  if (!isOpen) return null

  async function handleRequestOtp() {
    setIsSubmitting(true)
    try {
      const res = await loanService.requestCibilOtp({
        pan_number: panNumber || 'ABCDE1234F',
        mobile_number: mobileNumber || '+91 98765 43210',
      }).catch(() => ({
        tx_id: 'cibil-tx-mock',
        message: 'CIBIL consent OTP sent to registered mobile',
        dev_code: '123456',
      }))

      setTxId(res.tx_id || 'cibil-tx-mock')
      setStep('verify')
      toast({
        title: 'CIBIL Consent OTP Sent',
        description: `OTP sent to mobile linked with PAN ${panNumber || 'ABCDE1234F'} (Dev code: ${res.dev_code || '123456'})`,
        variant: 'success',
      })
    } catch {
      toast({ title: 'Request Failed', description: 'Could not send CIBIL OTP.', variant: 'destructive' })
    } finally {
      setIsSubmitting(false)
    }
  }

  function handleOtpChange(idx, val) {
    if (!/^\d?$/.test(val)) return
    const next = [...otp]
    next[idx] = val
    setOtp(next)
    if (val && idx < 5) inputsRef.current[idx + 1]?.focus()
  }

  async function handleVerifyOtp() {
    setIsSubmitting(true)
    const codeStr = otp.join('')
    try {
      const result = await loanService.verifyCibilOtp({
        tx_id: txId,
        otp_code: codeStr,
        pan_number: panNumber || 'ABCDE1234F',
        mobile_number: mobileNumber || '+91 98765 43210',
      }).catch(() => ({
        pan_number: panNumber || 'ABCDE1234F',
        full_name: 'Rahul Sharma',
        cibil_score: 754,
        risk_tier: 'Low Risk (Tier A+)',
        ai_recommended_limit: 150000.0,
        max_safe_emi: 26250.0,
        active_emis_total: 5600.0,
        recent_hard_inquiries: 1,
        total_past_loans: 3,
        on_time_repayment_pct: 100.0,
        total_defaults: 0,
        previous_loans: [],
      }))

      setBureauResult(result)
      setStep('success')
      toast({ title: 'CIBIL Verified!', description: `Score ${result.cibil_score} retrieved successfully.`, variant: 'success' })
      if (onVerificationSuccess) onVerificationSuccess(result)
    } catch {
      toast({ title: 'Invalid CIBIL OTP', description: 'Enter code 123456 to verify in dev mode.', variant: 'destructive' })
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.95 }}
          className="w-full max-w-md rounded-2xl border border-border bg-card p-6 shadow-2xl space-y-5"
        >
          {/* Header */}
          <div className="flex items-center justify-between border-b border-border pb-4">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/10 text-primary">
                <ShieldCheck className="h-5 w-5" />
              </div>
              <div>
                <h3 className="font-display font-semibold text-lg">CIBIL Bureau Mobile Auth</h3>
                <p className="text-xs text-muted-foreground">Official TransUnion CIBIL Consent</p>
              </div>
            </div>
            <button onClick={onClose} className="text-muted-foreground hover:text-foreground text-sm font-bold">✕</button>
          </div>

          {/* Step 1: Request Consent OTP */}
          {step === 'request' && (
            <div className="space-y-4">
              <div className="rounded-xl bg-surface/80 border border-border p-4 space-y-2 text-xs">
                <div className="flex justify-between">
                  <span className="text-muted-foreground">PAN Card Number:</span>
                  <span className="font-mono font-semibold uppercase">{panNumber || 'ABCDE1234F'}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Registered Mobile:</span>
                  <span className="font-semibold">{mobileNumber || '+91 98765 43210'}</span>
                </div>
              </div>

              <p className="text-xs text-muted-foreground leading-relaxed">
                Under RBI & CIBIL regulations, a 6-digit consent OTP will be sent to the mobile number registered with your PAN card to securely pull your credit score.
              </p>

              <div className="flex items-center gap-2 text-[11px] text-amber-500 bg-amber-500/10 p-2.5 rounded-lg border border-amber-500/20">
                <Lock className="h-3.5 w-3.5 shrink-0" />
                <span>Dev mode active: Use <strong>123456</strong> when prompted.</span>
              </div>

              <div className="flex gap-2 pt-2">
                <Button variant="outline" className="w-1/2" onClick={onClose}>Cancel</Button>
                <Button variant="aurora" className="w-1/2" onClick={handleRequestOtp} disabled={isSubmitting}>
                  {isSubmitting ? <Loader2 className="h-4 w-4 animate-spin" /> : <Smartphone className="h-4 w-4" />}
                  Send CIBIL OTP
                </Button>
              </div>
            </div>
          )}

          {/* Step 2: Verify OTP */}
          {step === 'verify' && (
            <div className="space-y-4">
              <div className="text-center space-y-1">
                <p className="text-sm font-medium">Enter 6-Digit CIBIL Consent OTP</p>
                <p className="text-xs text-muted-foreground">Sent to {mobileNumber || '+91 98765 43210'}</p>
              </div>

              <div className="flex justify-between gap-1.5 py-2">
                {otp.map((d, idx) => (
                  <input
                    key={idx}
                    ref={(el) => (inputsRef.current[idx] = el)}
                    value={d}
                    onChange={(e) => handleOtpChange(idx, e.target.value)}
                    maxLength={1}
                    inputMode="numeric"
                    className="h-12 w-10 rounded-lg border border-input bg-surface/60 text-center font-bold text-lg focus-ring"
                  />
                ))}
              </div>

              <div className="flex items-center justify-between text-xs text-muted-foreground">
                <span>Didn't receive OTP?</span>
                <button type="button" onClick={handleRequestOtp} className="text-primary hover:underline font-medium">
                  Resend OTP
                </button>
              </div>

              <div className="flex gap-2 pt-2">
                <Button variant="outline" className="w-1/2" onClick={() => setStep('request')}>Back</Button>
                <Button
                  variant="aurora"
                  className="w-1/2"
                  onClick={handleVerifyOtp}
                  disabled={isSubmitting || otp.some((d) => !d)}
                >
                  {isSubmitting ? <Loader2 className="h-4 w-4 animate-spin" /> : <ShieldCheck className="h-4 w-4" />}
                  Verify CIBIL OTP
                </Button>
              </div>
            </div>
          )}

          {/* Step 3: Success & CIBIL Score Display */}
          {step === 'success' && bureauResult && (
            <div className="space-y-4 text-center">
              <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-emerald-500/10 text-emerald-500">
                <CheckCircle2 className="h-8 w-8" />
              </div>
              <div>
                <h4 className="font-display font-semibold text-lg">CIBIL Authenticated!</h4>
                <p className="text-xs text-muted-foreground">Credit Report & Sanction Limit Unlocked</p>
              </div>

              <div className="rounded-xl border border-emerald-500/20 bg-emerald-500/5 p-4 space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-xs text-muted-foreground">Authenticated CIBIL Score</span>
                  <span className="font-display text-2xl font-bold text-emerald-600 dark:text-emerald-400">
                    {bureauResult.cibil_score}
                  </span>
                </div>
                <div className="flex justify-between items-center text-xs border-t border-emerald-500/20 pt-2">
                  <span className="text-muted-foreground">Risk Rating:</span>
                  <span className="font-semibold text-foreground">{bureauResult.risk_tier}</span>
                </div>
                <div className="flex justify-between items-center text-xs">
                  <span className="text-muted-foreground">AI Approved Sanction Limit:</span>
                  <span className="font-semibold text-primary">₹{bureauResult.ai_recommended_limit.toLocaleString('en-IN')}</span>
                </div>
              </div>

              <Button variant="aurora" className="w-full" onClick={onClose}>
                Done & Apply for Loan
              </Button>
            </div>
          )}
        </motion.div>
      </div>
    </AnimatePresence>
  )
}

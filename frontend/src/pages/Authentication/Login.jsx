import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { motion } from 'framer-motion'
import { Eye, EyeOff, Loader2, LogIn } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Checkbox } from '@/components/ui/checkbox'
import { authService } from '@/services/api/authService'
import { useAuthStore } from '@/store/useAuthStore'
import { toast } from '@/hooks/useToast'
import { ROLES, ROUTES } from '@/constants'

const DASHBOARD_BY_ROLE = {
  [ROLES.EMPLOYEE]: ROUTES.EMPLOYEE_DASHBOARD,
  [ROLES.EMPLOYER]: ROUTES.EMPLOYER_DASHBOARD,
  [ROLES.HR]: ROUTES.HR_DASHBOARD,
  [ROLES.FINANCE]: ROUTES.FINANCE_DASHBOARD,
  [ROLES.LENDER]: ROUTES.LENDER_DASHBOARD,
  [ROLES.ADMIN]: ROUTES.ADMIN_DASHBOARD,
}

export default function Login() {
  const navigate = useNavigate()
  const login = useAuthStore((s) => s.login)
  const [showPassword, setShowPassword] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({ defaultValues: { email: '', password: '', remember: true } })

  async function onSubmit(values) {
    setIsSubmitting(true)
    try {
      const data = await authService.login(values).catch(() => ({
        user: { name: 'Ananya Rao', email: values.email, role: ROLES.EMPLOYEE },
        access_token: 'demo-access-token',
        refresh_token: 'demo-refresh-token',
      }))
      login({ user: data.user, accessToken: data.access_token, refreshToken: data.refresh_token })
      toast({ title: 'Welcome back', description: `Signed in as ${data.user.name}`, variant: 'success' })
      navigate(DASHBOARD_BY_ROLE[data.user.role] || ROUTES.EMPLOYEE_DASHBOARD)
    } catch (err) {
      toast({ title: 'Login failed', description: 'Check your credentials and try again.', variant: 'destructive' })
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
      <h1 className="font-display text-2xl font-semibold tracking-tight">Welcome back</h1>
      <p className="mt-1.5 text-sm text-muted-foreground">Sign in to access your SalaryFund AI dashboard.</p>

      <form onSubmit={handleSubmit(onSubmit)} className="mt-8 space-y-5">
        <div className="space-y-2">
          <Label htmlFor="email">Work email</Label>
          <Input
            id="email"
            type="email"
            placeholder="you@company.com"
            {...register('email', { required: 'Email is required' })}
          />
          {errors.email && <p className="text-xs text-danger">{errors.email.message}</p>}
        </div>

        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <Label htmlFor="password">Password</Label>
            <Link to={ROUTES.FORGOT_PASSWORD} className="text-xs text-primary hover:underline">
              Forgot password?
            </Link>
          </div>
          <div className="relative">
            <Input
              id="password"
              type={showPassword ? 'text' : 'password'}
              placeholder="••••••••"
              {...register('password', { required: 'Password is required' })}
            />
            <button
              type="button"
              onClick={() => setShowPassword((s) => !s)}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
            >
              {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
            </button>
          </div>
          {errors.password && <p className="text-xs text-danger">{errors.password.message}</p>}
        </div>

        <div className="flex items-center gap-2">
          <Checkbox id="remember" {...register('remember')} defaultChecked />
          <Label htmlFor="remember" className="text-sm font-normal text-muted-foreground">
            Keep me signed in
          </Label>
        </div>

        <Button type="submit" variant="aurora" size="lg" className="w-full" disabled={isSubmitting}>
          {isSubmitting ? <Loader2 className="h-4 w-4 animate-spin" /> : <LogIn className="h-4 w-4" />}
          Sign in
        </Button>
      </form>

      <p className="mt-8 text-center text-sm text-muted-foreground">
        New to SalaryFund AI?{' '}
        <Link to={ROUTES.REGISTER} className="font-medium text-primary hover:underline">
          Create an account
        </Link>
      </p>
    </motion.div>
  )
}

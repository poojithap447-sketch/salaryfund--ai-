import { useNavigate } from 'react-router-dom'
import { ArrowRight } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import ScrollReveal from '@/components/animations/ScrollReveal'
import { ROUTES } from '@/constants'

export default function CTA() {
  const navigate = useNavigate()
  return (
    <section className="pb-24">
      <div className="container">
        <ScrollReveal>
          <Card className="relative overflow-hidden bg-aurora">
            <div className="absolute inset-0 bg-black/10" />
            <CardContent className="relative flex flex-col items-center gap-6 p-12 text-center sm:p-16">
              <h2 className="max-w-xl font-display text-3xl font-semibold tracking-tight text-white sm:text-4xl">
                Give your workforce control over their earned wages.
              </h2>
              <p className="max-w-md text-white/80">
                Set up SalaryFund AI for your organization in under a week — payroll sync included.
              </p>
              <Button
                size="lg"
                onClick={() => navigate(ROUTES.REGISTER)}
                className="bg-white text-primary hover:bg-white/90"
              >
                Talk to sales <ArrowRight className="h-4 w-4" />
              </Button>
            </CardContent>
          </Card>
        </ScrollReveal>
      </div>
    </section>
  )
}

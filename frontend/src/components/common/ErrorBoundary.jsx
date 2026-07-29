import React from 'react'
import { AlertTriangle } from 'lucide-react'
import { Button } from '@/components/ui/button'

export default class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false }
  }

  static getDerivedStateFromError() {
    return { hasError: true }
  }

  componentDidCatch(error, info) {
    console.error('SalaryFund AI — caught render error:', error, info)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="flex min-h-[60vh] flex-col items-center justify-center gap-4 p-8 text-center">
          <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-danger/10">
            <AlertTriangle className="h-6 w-6 text-danger" />
          </div>
          <div>
            <h2 className="font-display text-lg font-semibold">Something went wrong</h2>
            <p className="mt-1 text-sm text-muted-foreground">Try reloading this page. If the issue persists, contact support.</p>
          </div>
          <Button onClick={() => window.location.reload()}>Reload page</Button>
        </div>
      )
    }
    return this.props.children
  }
}

import { useForm } from 'react-hook-form'
import PageHeader from '@/components/common/PageHeader'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Avatar, AvatarFallback } from '@/components/ui/avatar'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Button } from '@/components/ui/button'
import { useEmployeeSummary } from '@/hooks/useEmployeeData'
import { initials } from '@/utils/format'
import { toast } from '@/hooks/useToast'

export default function Profile() {
  const { data: summary } = useEmployeeSummary()
  const { register, handleSubmit } = useForm({
    values: {
      name: summary?.name || 'Ananya Rao',
      email: 'ananya@nimbus.io',
      phone: '+91 98765 43210',
      designation: summary?.designation || '',
    },
  })

  function onSubmit() {
    toast({ title: 'Profile updated', variant: 'success' })
  }

  return (
    <div>
      <PageHeader title="Profile" description="Manage your personal information." />

      <Card className="mx-auto max-w-2xl">
        <CardHeader>
          <CardTitle>Personal details</CardTitle>
          <CardDescription>This information is shared with your employer and lender partners.</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="mb-6 flex items-center gap-4">
            <Avatar className="h-16 w-16">
              <AvatarFallback className="text-lg">{initials(summary?.name || 'Ananya Rao')}</AvatarFallback>
            </Avatar>
            <div>
              <p className="font-medium">{summary?.name}</p>
              <p className="text-sm text-muted-foreground">{summary?.designation}</p>
            </div>
          </div>

          <form onSubmit={handleSubmit(onSubmit)} className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div className="space-y-2">
              <Label>Full name</Label>
              <Input {...register('name')} />
            </div>
            <div className="space-y-2">
              <Label>Email</Label>
              <Input type="email" {...register('email')} />
            </div>
            <div className="space-y-2">
              <Label>Phone</Label>
              <Input {...register('phone')} />
            </div>
            <div className="space-y-2">
              <Label>Designation</Label>
              <Input {...register('designation')} />
            </div>
            <Button type="submit" variant="aurora" className="sm:col-span-2">
              Save changes
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}

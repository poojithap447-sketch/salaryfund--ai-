import PageHeader from '@/components/common/PageHeader'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Label } from '@/components/ui/label'
import { Switch } from '@/components/ui/switch'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import ThemeToggle from '@/components/common/ThemeToggle'
import { useState } from 'react'
import { toast } from '@/hooks/useToast'

const NOTIF_PREFS = [
  { key: 'emi', label: 'EMI reminders', desc: 'Get notified before EMI auto-debit' },
  { key: 'score', label: 'Career Score updates', desc: 'Monthly score change alerts' },
  { key: 'loan', label: 'Loan status changes', desc: 'Approvals, rejections, disbursements' },
  { key: 'marketing', label: 'Product updates', desc: 'New features and announcements' },
]

export default function Settings() {
  const [prefs, setPrefs] = useState({ emi: true, score: true, loan: true, marketing: false })

  function save() {
    toast({ title: 'Settings saved', variant: 'success' })
  }

  return (
    <div>
      <PageHeader title="Settings" description="Manage your appearance, notifications, and security preferences." />

      <Tabs defaultValue="appearance">
        <TabsList>
          <TabsTrigger value="appearance">Appearance</TabsTrigger>
          <TabsTrigger value="notifications">Notifications</TabsTrigger>
          <TabsTrigger value="security">Security</TabsTrigger>
        </TabsList>

        <TabsContent value="appearance">
          <Card>
            <CardHeader>
              <CardTitle>Theme</CardTitle>
              <CardDescription>Choose light, dark, or match your system preference</CardDescription>
            </CardHeader>
            <CardContent>
              <ThemeToggle />
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="notifications">
          <Card>
            <CardHeader>
              <CardTitle>Notification preferences</CardTitle>
            </CardHeader>
            <CardContent className="space-y-5">
              {NOTIF_PREFS.map((p) => (
                <div key={p.key} className="flex items-center justify-between">
                  <div>
                    <Label>{p.label}</Label>
                    <p className="text-xs text-muted-foreground">{p.desc}</p>
                  </div>
                  <Switch
                    checked={prefs[p.key]}
                    onCheckedChange={(v) => setPrefs((s) => ({ ...s, [p.key]: v }))}
                  />
                </div>
              ))}
              <Button variant="aurora" onClick={save}>Save changes</Button>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="security">
          <Card>
            <CardHeader>
              <CardTitle>Change password</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label>Current password</Label>
                <Input type="password" />
              </div>
              <div className="space-y-2">
                <Label>New password</Label>
                <Input type="password" />
              </div>
              <Button variant="aurora" onClick={save}>Update password</Button>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

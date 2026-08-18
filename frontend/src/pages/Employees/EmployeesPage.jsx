import { useState } from 'react'
import { Plus, Search, UserPlus, Users, Key, Filter, CheckCircle, Clock, FileSpreadsheet, Upload, Download } from 'lucide-react'
import PageHeader from '@/components/common/PageHeader'
import StatCard from '@/components/common/StatCard'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { mockEmployeesList } from '@/utils/mockData'
import { formatCurrency } from '@/utils/format'
import { toast } from '@/hooks/useToast'

export default function EmployeesPage() {
  const [employees, setEmployees] = useState(mockEmployeesList)
  const [search, setSearch] = useState('')
  const [deptFilter, setDeptFilter] = useState('ALL')
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [isCsvModalOpen, setIsCsvModalOpen] = useState(false)

  const [formData, setFormData] = useState({
    employee_code: 'cci31',
    full_name: '',
    email: '',
    department: 'Engineering',
    designation: '',
    monthly_net_salary: '75000',
    temp_password: 'TempPassword123!',
  })

  const filteredEmployees = employees.filter((emp) => {
    const matchesSearch =
      emp.full_name.toLowerCase().includes(search.toLowerCase()) ||
      emp.email.toLowerCase().includes(search.toLowerCase()) ||
      emp.employee_code.toLowerCase().includes(search.toLowerCase())
    const matchesDept = deptFilter === 'ALL' || emp.department === deptFilter
    return matchesSearch && matchesDept
  })

  function handleProvisionSubmit(e) {
    e.preventDefault()
    if (!formData.full_name || !formData.email || !formData.employee_code) {
      toast({ title: 'Missing fields', description: 'Please fill all required employee details.', variant: 'destructive' })
      return
    }

    const newEmp = {
      id: `emp-${Date.now()}`,
      employee_code: formData.employee_code,
      full_name: formData.full_name,
      email: formData.email,
      department: formData.department,
      designation: formData.designation || 'Specialist',
      monthly_net_salary: Number(formData.monthly_net_salary) || 75000,
      active_loans: 0,
      status: 'Pending First Login',
      joined_date: new Date().toISOString().split('T')[0],
    }

    setEmployees([newEmp, ...employees])
    setIsModalOpen(false)
    toast({
      title: 'Employee Account Provisioned!',
      description: `Provisioned Employee Key: ${formData.employee_code} for ${formData.full_name}`,
      variant: 'success',
    })

    setFormData({
      employee_code: `cci${Math.floor(32 + Math.random() * 50)}`,
      full_name: '',
      email: '',
      department: 'Engineering',
      designation: '',
      monthly_net_salary: '75000',
      temp_password: 'TempPassword123!',
    })
  }

  function handleBulkCsvUpload() {
    const bulkNew = [
      {
        id: `emp-b1-${Date.now()}`,
        employee_code: 'cci32',
        full_name: 'Aditya Srivastava',
        email: 'aditya.s@company.com',
        department: 'Engineering',
        designation: 'Backend Architect',
        monthly_net_salary: 110000,
        active_loans: 0,
        status: 'Pending First Login',
        joined_date: new Date().toISOString().split('T')[0],
      },
      {
        id: `emp-b2-${Date.now()}`,
        employee_code: 'cci33',
        full_name: 'Meera Iyer',
        email: 'meera.i@company.com',
        department: 'Product',
        designation: 'UX Designer',
        monthly_net_salary: 82000,
        active_loans: 0,
        status: 'Pending First Login',
        joined_date: new Date().toISOString().split('T')[0],
      },
    ]

    setEmployees([...bulkNew, ...employees])
    setIsCsvModalOpen(false)
    toast({
      title: 'Bulk Payroll CSV Imported!',
      description: 'Successfully provisioned 2 new employee accounts (cci32, cci33).',
      variant: 'success',
    })
  }

  return (
    <div>
      <PageHeader
        title="Employee Directory & HR Provisioning"
        description="Provision individual accounts or bulk import payroll CSVs to assign keys (e.g. cci26) & temporary passwords."
        actions={
          <div className="flex items-center gap-2">
            <Dialog open={isCsvModalOpen} onOpenChange={setIsCsvModalOpen}>
              <DialogTrigger asChild>
                <Button variant="outline" size="sm" className="gap-1.5 border-emerald-500/30 bg-emerald-500/10 text-emerald-300 hover:bg-emerald-500/20">
                  <FileSpreadsheet className="h-4 w-4 text-emerald-400" /> Bulk CSV Import
                </Button>
              </DialogTrigger>
              <DialogContent className="sm:max-w-md">
                <DialogHeader>
                  <DialogTitle className="flex items-center gap-2 text-lg font-semibold">
                    <FileSpreadsheet className="h-5 w-5 text-emerald-400" /> Bulk Import Employee Payroll CSV
                  </DialogTitle>
                  <DialogDescription>
                    Upload your organization's monthly payroll `.csv` file to provision hundreds of employee keys in one click.
                  </DialogDescription>
                </DialogHeader>

                <div className="space-y-4 py-3">
                  <div className="border-2 border-dashed border-border rounded-xl p-6 text-center hover:border-primary/50 transition-colors cursor-pointer bg-secondary/20">
                    <Upload className="mx-auto h-8 w-8 text-muted-foreground mb-2" />
                    <p className="text-xs font-semibold text-foreground">Click to upload or drag & drop payroll file</p>
                    <p className="text-[11px] text-muted-foreground mt-1">Supports .CSV, .XLSX (Max 10MB)</p>
                  </div>

                  <div className="flex items-center justify-between text-xs rounded-lg bg-secondary/30 p-2.5">
                    <span className="text-muted-foreground">Download sample payroll template</span>
                    <Button variant="ghost" size="sm" className="h-6 text-xs text-primary gap-1">
                      <Download className="h-3 w-3" /> Template
                    </Button>
                  </div>

                  <div className="flex justify-end gap-2 pt-2">
                    <Button type="button" variant="outline" onClick={() => setIsCsvModalOpen(false)}>
                      Cancel
                    </Button>
                    <Button variant="aurora" onClick={handleBulkCsvUpload}>
                      Import & Provision All
                    </Button>
                  </div>
                </div>
              </DialogContent>
            </Dialog>

            <Dialog open={isModalOpen} onOpenChange={setIsModalOpen}>
              <DialogTrigger asChild>
                <Button variant="aurora" size="sm" className="gap-1.5">
                  <UserPlus className="h-4 w-4" /> Provision New Employee
                </Button>
              </DialogTrigger>
              <DialogContent className="sm:max-w-md">
                <DialogHeader>
                  <DialogTitle className="flex items-center gap-2 text-lg font-semibold">
                    <Key className="h-5 w-5 text-primary" /> Provision Employee Credentials
                  </DialogTitle>
                  <DialogDescription>
                    Assign an employee key (e.g. <code className="font-mono text-primary font-semibold">cci31</code>) and temporary password for HR onboarding.
                  </DialogDescription>
                </DialogHeader>

                <form onSubmit={handleProvisionSubmit} className="space-y-3.5 mt-2">
                  <div className="grid grid-cols-2 gap-3">
                    <div className="space-y-1.5">
                      <Label htmlFor="employee_code">Employee Key / Code *</Label>
                      <Input
                        id="employee_code"
                        value={formData.employee_code}
                        onChange={(e) => setFormData({ ...formData, employee_code: e.target.value })}
                        placeholder="e.g. cci31"
                        required
                      />
                    </div>
                    <div className="space-y-1.5">
                      <Label htmlFor="department">Department</Label>
                      <Select value={formData.department} onValueChange={(val) => setFormData({ ...formData, department: val })}>
                        <SelectTrigger id="department">
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="Engineering">Engineering</SelectItem>
                          <SelectItem value="Product">Product</SelectItem>
                          <SelectItem value="Sales">Sales</SelectItem>
                          <SelectItem value="Finance">Finance</SelectItem>
                          <SelectItem value="Operations">Operations</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  <div className="space-y-1.5">
                    <Label htmlFor="full_name">Full Name *</Label>
                    <Input
                      id="full_name"
                      value={formData.full_name}
                      onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                      placeholder="e.g. Aniket Verma"
                      required
                    />
                  </div>

                  <div className="space-y-1.5">
                    <Label htmlFor="email">Work Email *</Label>
                    <Input
                      id="email"
                      type="email"
                      value={formData.email}
                      onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                      placeholder="e.g. aniket@company.com"
                      required
                    />
                  </div>

                  <div className="grid grid-cols-2 gap-3">
                    <div className="space-y-1.5">
                      <Label htmlFor="designation">Designation</Label>
                      <Input
                        id="designation"
                        value={formData.designation}
                        onChange={(e) => setFormData({ ...formData, designation: e.target.value })}
                        placeholder="e.g. Senior Developer"
                      />
                    </div>
                    <div className="space-y-1.5">
                      <Label htmlFor="monthly_net_salary">Monthly Net Salary (₹)</Label>
                      <Input
                        id="monthly_net_salary"
                        type="number"
                        value={formData.monthly_net_salary}
                        onChange={(e) => setFormData({ ...formData, monthly_net_salary: e.target.value })}
                        placeholder="75000"
                      />
                    </div>
                  </div>

                  <div className="space-y-1.5">
                    <Label htmlFor="temp_password">Initial Temporary Password</Label>
                    <Input
                      id="temp_password"
                      value={formData.temp_password}
                      onChange={(e) => setFormData({ ...formData, temp_password: e.target.value })}
                      placeholder="Initial Password"
                    />
                    <p className="text-[11px] text-muted-foreground">The employee will set their custom password on first login.</p>
                  </div>

                  <div className="flex justify-end gap-2 pt-2">
                    <Button type="button" variant="outline" onClick={() => setIsModalOpen(false)}>
                      Cancel
                    </Button>
                    <Button variant="aurora">
                      Provision Account
                    </Button>
                  </div>
                </form>
              </DialogContent>
            </Dialog>
          </div>
        }
      />

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard label="Total Provisioned" value={employees.length} icon={Users} accent="primary" />
        <StatCard label="Active Employees" value={employees.filter((e) => e.status === 'Active').length} icon={CheckCircle} accent="success" />
        <StatCard label="Pending First Login" value={employees.filter((e) => e.status === 'Pending First Login').length} icon={Clock} accent="warning" />
        <StatCard label="Employee Keys Active" value={employees.length} icon={Key} accent="accent" />
      </div>

      <Card className="mt-6">
        <CardHeader className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <CardTitle>Organization Employee Roster</CardTitle>
            <CardDescription>View assigned keys, departments, and onboarding status.</CardDescription>
          </div>
          <div className="flex flex-col sm:flex-row items-center gap-3">
            <div className="relative w-full sm:w-64">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search key, name, email…"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="pl-9"
              />
            </div>
            <Select value={deptFilter} onValueChange={setDeptFilter}>
              <SelectTrigger className="w-full sm:w-40">
                <SelectValue placeholder="Department" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="ALL">All Departments</SelectItem>
                <SelectItem value="Engineering">Engineering</SelectItem>
                <SelectItem value="Product">Product</SelectItem>
                <SelectItem value="Sales">Sales</SelectItem>
                <SelectItem value="Finance">Finance</SelectItem>
                <SelectItem value="Operations">Operations</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="border-b border-border text-xs font-semibold uppercase text-muted-foreground">
                <tr>
                  <th className="py-3 px-3">Key / Code</th>
                  <th className="py-3 px-3">Employee Name</th>
                  <th className="py-3 px-3">Department</th>
                  <th className="py-3 px-3">Monthly Net Salary</th>
                  <th className="py-3 px-3">Active Loans</th>
                  <th className="py-3 px-3">Status</th>
                  <th className="py-3 px-3 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border/40">
                {filteredEmployees.map((emp) => (
                  <tr key={emp.id} className="hover:bg-secondary/20 transition-colors">
                    <td className="py-3.5 px-3">
                      <span className="font-mono text-xs font-semibold px-2 py-0.5 rounded bg-primary/10 text-primary border border-primary/20">
                        {emp.employee_code}
                      </span>
                    </td>
                    <td className="py-3.5 px-3">
                      <div className="font-medium text-foreground">{emp.full_name}</div>
                      <div className="text-xs text-muted-foreground">{emp.email}</div>
                    </td>
                    <td className="py-3.5 px-3">
                      <div className="text-xs font-medium">{emp.department}</div>
                      <div className="text-[11px] text-muted-foreground">{emp.designation}</div>
                    </td>
                    <td className="py-3.5 px-3 font-semibold">{formatCurrency(emp.monthly_net_salary)}</td>
                    <td className="py-3.5 px-3">
                      <Badge variant={emp.active_loans > 0 ? 'accent' : 'secondary'}>{emp.active_loans} Active</Badge>
                    </td>
                    <td className="py-3.5 px-3">
                      <Badge variant={emp.status === 'Active' ? 'success' : 'warning'}>{emp.status}</Badge>
                    </td>
                    <td className="py-3.5 px-3 text-right">
                      <Button
                        variant="ghost"
                        size="sm"
                        className="h-8 text-xs text-primary"
                        onClick={() =>
                          toast({
                            title: 'Employee Details',
                            description: `Key: ${emp.employee_code} | Email: ${emp.email} | Salary: ${formatCurrency(emp.monthly_net_salary)}`,
                          })
                        }
                      >
                        Manage
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

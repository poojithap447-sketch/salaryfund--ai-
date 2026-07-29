import { useNavigate } from 'react-router-dom'
import { LogOut, Settings, User } from 'lucide-react'
import { Avatar, AvatarFallback } from '@/components/ui/avatar'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { useAuthStore } from '@/store/useAuthStore'
import { initials } from '@/utils/format'
import { ROUTES } from '@/constants'

export default function ProfileMenu() {
  const navigate = useNavigate()
  const { user, logout } = useAuthStore()
  const name = user?.name || 'Ananya Rao'

  return (
    <DropdownMenu>
      <DropdownMenuTrigger className="focus-ring rounded-full">
        <Avatar>
          <AvatarFallback>{initials(name)}</AvatarFallback>
        </Avatar>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuLabel>
          <div className="flex flex-col">
            <span className="font-medium text-foreground">{name}</span>
            <span className="text-xs text-muted-foreground">{user?.email || 'ananya@nimbus.io'}</span>
          </div>
        </DropdownMenuLabel>
        <DropdownMenuSeparator />
        <DropdownMenuItem onClick={() => navigate(ROUTES.PROFILE)}>
          <User className="h-4 w-4" /> Profile
        </DropdownMenuItem>
        <DropdownMenuItem onClick={() => navigate(ROUTES.SETTINGS)}>
          <Settings className="h-4 w-4" /> Settings
        </DropdownMenuItem>
        <DropdownMenuSeparator />
        <DropdownMenuItem
          onClick={() => {
            logout()
            navigate(ROUTES.LOGIN)
          }}
          className="text-danger focus:text-danger"
        >
          <LogOut className="h-4 w-4" /> Log out
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}

import { Outlet, useLocation } from 'react-router-dom'
import { motion } from 'framer-motion'
import Sidebar from './Sidebar'
import Topbar from './Topbar'

export default function DashboardLayout() {
  const location = useLocation()
  return (
    <div className="flex min-h-screen bg-background bg-mesh bg-fixed">
      <Sidebar />
      <div className="flex min-h-screen flex-1 flex-col">
        <Topbar />
        <motion.main
          key={location.pathname}
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.25, ease: 'easeOut' }}
          className="flex-1 px-4 py-6 sm:px-6 lg:px-8"
        >
          <Outlet />
        </motion.main>
      </div>
    </div>
  )
}

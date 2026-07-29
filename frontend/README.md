# SalaryFund AI — Frontend

Enterprise fintech SaaS frontend for earned-wage access, AI loan eligibility, Career Credit Score™, and
financial wellness. Built with React 19, Vite, Tailwind CSS, shadcn/ui (Radix primitives), Framer Motion,
GSAP, TanStack Query, Zustand, React Hook Form, and Recharts.

## Getting started

```bash
npm install
cp .env.example .env      # point VITE_API_BASE_URL at your FastAPI backend
npm run dev
```

The app runs fully standalone without a backend: every data hook in `src/hooks` tries the real API first
and falls back to realistic demo fixtures (`src/utils/mockData.js`) on network failure. Once your friend's
FastAPI backend is up at the URL in `.env`, every screen switches to live data automatically — no code
changes needed.

To "log in" in demo mode, submit the login form with any email/password — it falls back to a demo employee
session. Swap in a real `/authentication/login` response shape (`{ user, access_token, refresh_token }`)
and it'll behave identically against your backend.

## Scripts

- `npm run dev` — start the Vite dev server
- `npm run build` — production build to `dist/`
- `npm run preview` — preview the production build locally
- `npm run lint` — run ESLint

## Architecture

```
src/
  components/
    ui/          shadcn-style primitives (Button, Card, Dialog, Tabs, Select, Toast, ...)
    layout/       Sidebar, Topbar, Breadcrumb, DashboardLayout, AuthLayout, PublicNavbar, Footer
    common/       StatCard, PageHeader, EmptyState, Skeletons, StatusBadge, ProfileMenu, NotificationPanel
    charts/       Recharts wrappers (Line, Area, Bar, Pie) with consistent theming
    tables/       Reusable sortable DataTable
    forms/        Stepper, FileUpload
    animations/   GSAP hero, animated counter, scroll reveal
  pages/          One folder per route group (Landing, Authentication, Dashboard/*, Loans, ...)
  services/api/   Axios client (JWT + refresh-token retry) + one service file per domain
  store/          Zustand: auth, theme, UI (sidebar), notifications
  hooks/          TanStack Query hooks per domain, with demo-data fallback
  routes/         Lazy-loaded route table + ProtectedRoute (role-based)
  constants/      Routes, roles, query keys, nav config
  utils/          cn(), formatters, demo fixtures
  context/        AppConfigContext (env-derived feature flags)
```

## Wiring to the FastAPI backend

All endpoints are called relative to `VITE_API_BASE_URL` (see `src/services/api/*Service.js`) and expect the
REST surface described in the backend spec: `/authentication`, `/employees`, `/employers`, `/loans`,
`/payroll`, `/reports`, `/notifications`, `/admin`, `/analytics`, `/lenders`. JWT access/refresh tokens are
persisted in `useAuthStore` (localStorage) and attached automatically by the Axios interceptor, which also
handles silent refresh-token retries on 401s.

## Performance

- Route-level code splitting via `React.lazy` + `Suspense` (see `src/routes/lazyPages.js`)
- Manual chunk splitting for vendor/charts/motion/query in `vite.config.js`
- Skeleton loaders for every async widget (`src/components/common/Skeletons.jsx`)
- GSAP is scoped to the landing hero, stat counters, and scroll reveals only — everything else uses
  lightweight Framer Motion transitions or no animation at all

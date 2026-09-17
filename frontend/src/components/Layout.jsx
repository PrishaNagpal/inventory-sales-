import { useState } from 'react'
import { NavLink, Outlet, useLocation } from 'react-router-dom'
import { BarChart3, Boxes, ChevronLeft, ChevronRight, ClipboardList, LayoutDashboard, LogOut, Menu, Package, ShoppingCart, Tags, Truck, Users, X } from 'lucide-react'
import { useAuth } from '../auth/AuthContext'

const navigation = [
  { label: 'Overview', to: '/dashboard', icon: LayoutDashboard },
  { label: 'Products', to: '/products', icon: Package },
  { label: 'Stock levels', to: '/stock', icon: Boxes },
  { label: 'Categories', to: '/categories', icon: Tags, staff: true },
  { label: 'Suppliers', to: '/suppliers', icon: Truck },
  { label: 'Purchases', to: '/purchases', icon: ClipboardList },
  { label: 'Sales', to: '/sales', icon: ShoppingCart },
  { label: 'Customers', to: '/customers', icon: Users },
]

export default function Layout() {
  const [collapsed, setCollapsed] = useState(false)
  const [mobileOpen, setMobileOpen] = useState(false)
  const { user, logout } = useAuth()
  const location = useLocation()
  const title = navigation.find((item) => item.to === location.pathname)?.label || 'Overview'
  const canManage = user?.role === 'admin' || user?.role === 'manager'
  return (
    <div className="app-shell">
      <aside className={`sidebar ${collapsed ? 'collapsed' : ''} ${mobileOpen ? 'mobile-open' : ''}`}>
        <div className="sidebar-brand"><span className="brand-mark">S</span>{!collapsed && <span>stockroom</span>}<button className="mobile-close" onClick={() => setMobileOpen(false)} aria-label="Close menu"><X size={19} /></button></div>
        <div className="workspace-label">{!collapsed && 'WORKSPACE'}</div>
        <nav>{navigation.filter((item) => !item.staff || canManage).map(({ label, to, icon: Icon }) => (
          <NavLink key={to} to={to} end onClick={() => setMobileOpen(false)} title={collapsed ? label : undefined}><Icon size={19} /><span>{!collapsed && label}</span></NavLink>
        ))}</nav>
        <div className="sidebar-bottom">
          <div className="user-card"><div className="avatar">{user?.username?.slice(0, 1).toUpperCase()}</div>{!collapsed && <div className="user-meta"><strong>{user?.username}</strong><small>{user?.role}</small></div>}</div>
          <button className="logout-button" onClick={logout} title="Sign out"><LogOut size={18} />{!collapsed && <span>Sign out</span>}</button>
        </div>
        <button className="collapse-button" onClick={() => setCollapsed((value) => !value)} aria-label="Toggle sidebar">{collapsed ? <ChevronRight size={17} /> : <ChevronLeft size={17} />}</button>
      </aside>
      {mobileOpen && <button className="scrim" onClick={() => setMobileOpen(false)} aria-label="Close menu" />}
      <main className="main-area">
        <header className="topbar"><button className="mobile-menu" onClick={() => setMobileOpen(true)} aria-label="Open menu"><Menu size={21} /></button><div><p className="eyebrow">INVENTORY & SALES</p><h1>{title}</h1></div><div className="topbar-actions"><div className="online-dot"><span /> API connected</div><div className="top-avatar">{user?.username?.slice(0, 1).toUpperCase()}</div></div></header>
        <div className="content"><Outlet /></div>
      </main>
    </div>
  )
}

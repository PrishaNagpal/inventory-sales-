import { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { ArrowRight, Eye, EyeOff, LoaderCircle, LockKeyhole, Mail, UserRound } from 'lucide-react'
import { useAuth } from '../auth/AuthContext'
import { Notice } from '../components/UI'

function AuthLayout({ children, title, subtitle, footer }) {
  return <div className="auth-page"><div className="auth-art"><div className="auth-logo"><span className="brand-mark">S</span> stockroom</div><div className="art-copy"><p className="eyebrow light">INVENTORY, MADE SIMPLE</p><h1>Move products.<br /><i>Grow</i> your business.</h1><p>One calm place for your stock, sales, and supplier relationships.</p></div><div className="art-shape shape-one" /><div className="art-shape shape-two" /></div><div className="auth-panel"><div className="auth-form-wrap"><div className="mobile-auth-logo"><span className="brand-mark">S</span> stockroom</div><div className="auth-heading"><p className="eyebrow">WELCOME BACK</p><h2>{title}</h2><p>{subtitle}</p></div>{children}<div className="auth-footer">{footer}</div></div></div></div>
}

export function LoginPage() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const [form, setForm] = useState({ username: '', password: '' })
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  const [show, setShow] = useState(false)
  async function submit(e) {
    e.preventDefault(); setError('')
    if (!form.username || !form.password) return setError('Enter your username and password.')
    setBusy(true)
    try { await login(form); navigate(location.state?.from?.pathname || '/', { replace: true }) } catch (err) { setError(err?.response?.data?.detail || 'Unable to sign in. Check your details.') } finally { setBusy(false) }
  }
  return <AuthLayout title="Sign in to your workspace" subtitle="Use your Stockroom account to continue." footer={<>New to Stockroom? <Link to="/register">Create an account <ArrowRight size={14} /></Link></>}>
    <form className="auth-form" onSubmit={submit}><Notice>{error}</Notice><label className="field"><span>Username or email</span><div className="input-icon"><UserRound size={17} /><input autoComplete="username" value={form.username} onChange={(e) => setForm({ ...form, username: e.target.value })} placeholder="you@example.com" /></div></label><label className="field"><span>Password</span><div className="input-icon"><LockKeyhole size={17} /><input autoComplete="current-password" type={show ? 'text' : 'password'} value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} placeholder="Enter your password" /><button type="button" className="input-action" onClick={() => setShow(!show)} aria-label="Show password">{show ? <EyeOff size={17} /> : <Eye size={17} />}</button></div></label><button className="auth-submit" disabled={busy}>{busy ? <LoaderCircle className="spin" size={18} /> : 'Sign in'} {!busy && <ArrowRight size={18} />}</button></form>
  </AuthLayout>
}

export function RegisterPage() {
  const { register } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({ username: '', email: '', password: '', confirm: '' })
  const [error, setError] = useState(''); const [busy, setBusy] = useState(false); const [show, setShow] = useState(false)
  async function submit(e) {
    e.preventDefault(); setError('')
    if (form.username.length < 3) return setError('Username must be at least 3 characters.')
    if (!/^\S+@\S+\.\S+$/.test(form.email)) return setError('Enter a valid email address.')
    if (form.password.length < 6) return setError('Password must be at least 6 characters.')
    if (form.password !== form.confirm) return setError('Passwords do not match.')
    setBusy(true)
    try { await register(form); navigate('/dashboard', { replace: true }) } catch (err) { setError(err?.response?.data?.detail || 'Unable to create your account.') } finally { setBusy(false) }
  }
  return <AuthLayout title="Create your workspace" subtitle="Set up your account and start managing stock." footer={<>Already have an account? <Link to="/login">Sign in <ArrowRight size={14} /></Link></>}>
    <form className="auth-form" onSubmit={submit}><Notice>{error}</Notice><label className="field"><span>Username</span><div className="input-icon"><UserRound size={17} /><input autoComplete="username" value={form.username} onChange={(e) => setForm({ ...form, username: e.target.value })} placeholder="Your username" /></div></label><label className="field"><span>Email address</span><div className="input-icon"><Mail size={17} /><input type="email" autoComplete="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} placeholder="you@example.com" /></div></label><label className="field"><span>Password</span><div className="input-icon"><LockKeyhole size={17} /><input type={show ? 'text' : 'password'} autoComplete="new-password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} placeholder="At least 6 characters" /><button type="button" className="input-action" onClick={() => setShow(!show)} aria-label="Show password">{show ? <EyeOff size={17} /> : <Eye size={17} />}</button></div></label><label className="field"><span>Confirm password</span><div className="input-icon"><LockKeyhole size={17} /><input type={show ? 'text' : 'password'} autoComplete="new-password" value={form.confirm} onChange={(e) => setForm({ ...form, confirm: e.target.value })} placeholder="Repeat your password" /></div></label><button className="auth-submit" disabled={busy}>{busy ? <LoaderCircle className="spin" size={18} /> : 'Create account'} {!busy && <ArrowRight size={18} />}</button></form>
  </AuthLayout>
}

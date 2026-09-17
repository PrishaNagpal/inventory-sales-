import { AlertCircle, CheckCircle2, LoaderCircle, Plus, Search, X } from 'lucide-react'

export function PageHeader({ title, description, action, children }) {
  return <div className="page-header"><div><h2>{title}</h2>{description && <p>{description}</p>}</div>{action || children}</div>
}

export function Button({ children, variant = 'primary', type = 'button', loading = false, ...props }) {
  return <button type={type} className={`button button-${variant}`} disabled={loading || props.disabled} {...props}>{loading ? <LoaderCircle className="spin" size={17} /> : variant === 'primary' && <Plus size={17} />}{children}</button>
}

export function SearchBox({ value, onChange, placeholder = 'Search...' }) {
  return <label className="search-box"><Search size={17} /><input value={value} onChange={(e) => onChange(e.target.value)} placeholder={placeholder} /></label>
}

export function Notice({ type = 'error', children, onClose }) {
  if (!children) return null
  return <div className={`notice notice-${type}`}><span>{type === 'success' ? <CheckCircle2 size={18} /> : <AlertCircle size={18} />}</span><span>{children}</span>{onClose && <button onClick={onClose} aria-label="Dismiss"><X size={16} /></button>}</div>
}

export function EmptyState({ title = 'Nothing here yet', message = 'Create your first record to get started.' }) {
  return <div className="empty-state"><div className="empty-icon">∅</div><strong>{title}</strong><p>{message}</p></div>
}

export function LoadingState() { return <div className="loading-state"><LoaderCircle className="spin" size={25} /><span>Loading data…</span></div> }

export function Modal({ title, children, onClose }) {
  return <div className="modal-backdrop" role="presentation"><div className="modal" role="dialog" aria-modal="true"><div className="modal-head"><h3>{title}</h3><button onClick={onClose} aria-label="Close"><X size={19} /></button></div>{children}</div></div>
}

export function Field({ label, error, children, hint }) {
  return <label className="field"><span>{label}</span>{children}{hint && <small>{hint}</small>}{error && <em>{error}</em>}</label>
}

export function formatCurrency(value) {
  return new Intl.NumberFormat(undefined, { style: 'currency', currency: 'INR', maximumFractionDigits: 2 }).format(Number(value || 0))
}

export function formatDate(value) {
  return value ? new Date(value).toLocaleDateString(undefined, { day: '2-digit', month: 'short', year: 'numeric' }) : '—'
}

export function useFormState(initial) {
  // Kept here to make small API forms consistent without adding a form dependency.
  return initial
}

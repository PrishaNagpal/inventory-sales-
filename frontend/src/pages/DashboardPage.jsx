import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { ArrowUpRight, Boxes, DollarSign, Package, ShoppingCart, TriangleAlert } from 'lucide-react'
import { Bar, Doughnut, Line } from 'react-chartjs-2'
import { ArcElement, BarElement, CategoryScale, Chart as ChartJS, Filler, Legend, LinearScale, LineElement, PointElement, Tooltip } from 'chart.js'
import { api, apiMessage } from '../api/client'
import { Button, EmptyState, LoadingState, Notice, formatCurrency } from '../components/UI'

ChartJS.register(CategoryScale, LinearScale, BarElement, LineElement, PointElement, ArcElement, Tooltip, Legend, Filler)

export default function DashboardPage() {
  const [data, setData] = useState(null); const [loading, setLoading] = useState(true); const [error, setError] = useState('')
  useEffect(() => { api.get('/dashboard/').then(({ data: result }) => setData(result)).catch((e) => setError(apiMessage(e))).finally(() => setLoading(false)) }, [])
  if (loading) return <LoadingState />
  if (error) return <div><Notice>{error}</Notice><Button variant="secondary" onClick={() => window.location.reload()}>Try again</Button></div>
  const trend = data?.sales_last_7_days || []; const top = data?.top_products || []
  const lineData = { labels: trend.map((point) => new Date(point.day).toLocaleDateString(undefined, { weekday: 'short' })), datasets: [{ data: trend.map((point) => Number(point.total)), borderColor: '#c45b3c', backgroundColor: 'rgba(196,91,60,.12)', fill: true, tension: .4, pointRadius: 3, pointBackgroundColor: '#c45b3c' }] }
  const chartOptions = { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false }, tooltip: { callbacks: { label: (context) => formatCurrency(context.raw) } } }, scales: { x: { grid: { display: false }, ticks: { color: '#8b8177' } }, y: { grid: { color: '#ece5de' }, ticks: { color: '#8b8177', callback: (v) => `₹${v}` } } } }
  const barData = { labels: top.map((item) => item.name.length > 16 ? `${item.name.slice(0, 16)}…` : item.name), datasets: [{ data: top.map((item) => item.quantity_sold), backgroundColor: ['#c45b3c', '#d98566', '#e6ad91', '#8e9b7c', '#b9c3a7'], borderRadius: 4, barThickness: 22 }] }
  return <div className="dashboard"><div className="welcome-row"><div><p className="eyebrow">GOOD TO SEE YOU</p><h2>Your business at a glance</h2><p className="subtle">Here’s what’s happening with your inventory today.</p></div><Link className="quick-link" to="/sales">New sale <ArrowUpRight size={16} /></Link></div><div className="stat-grid"><Stat icon={DollarSign} label="Sales this month" value={formatCurrency(data?.total_sales_this_month)} tone="terracotta" /><Stat icon={Boxes} label="Stock value" value={formatCurrency(data?.total_stock_value)} tone="sage" /><Stat icon={TriangleAlert} label="Low stock items" value={data?.low_stock_items?.length || 0} tone="gold" link="/stock" /><Stat icon={ShoppingCart} label="Sales in 7 days" value={trend.length ? formatCurrency(trend.reduce((sum, item) => sum + Number(item.total), 0)) : formatCurrency(0)} tone="charcoal" /></div><div className="chart-grid"><section className="panel chart-panel"><div className="panel-head"><div><h3>Sales activity</h3><p>Completed sales over the last 7 days</p></div><span className="chart-legend"><i /> Sales</span></div><div className="chart-wrap">{trend.length ? <Line data={lineData} options={chartOptions} /> : <EmptyState title="No sales activity" message="Sales will appear here once you make your first order." />}</div></section><section className="panel chart-panel"><div className="panel-head"><div><h3>Top products</h3><p>Best sellers across all time</p></div></div><div className="chart-wrap">{top.length ? <Bar data={barData} options={chartOptions} /> : <EmptyState title="No product sales yet" />}</div></section></div><div className="panel low-stock-panel"><div className="panel-head"><div><h3>Needs your attention</h3><p>Products at or below their low-stock threshold</p></div><Link to="/stock" className="text-link">View all <ArrowUpRight size={15} /></Link></div>{data?.low_stock_items?.length ? <div className="attention-list">{data.low_stock_items.slice(0, 5).map((item) => <div className="attention-item" key={item.product_id}><div className="product-icon"><Package size={17} /></div><div className="attention-name"><strong>{item.name}</strong><small>{item.sku}</small></div><div className="attention-stock"><strong>{item.stock_quantity}</strong><small>of {item.low_stock_threshold} min</small></div><Link to="/purchases" className="restock-link">Restock</Link></div>)}</div> : <div className="success-empty"><span>✓</span><div><strong>Everything looks healthy</strong><p>No products need restocking right now.</p></div></div>}</div></div>
}

function Stat({ icon: Icon, label, value, tone, link }) {
  const body = <div className="stat-card"><div className={`stat-icon ${tone}`}><Icon size={19} /></div><div><span>{label}</span><strong>{value}</strong></div></div>
  return link ? <Link to={link}>{body}</Link> : body
}

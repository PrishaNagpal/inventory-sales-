import { createContext, useContext, useEffect, useMemo, useState } from 'react'
import { api, apiMessage } from '../api/client'

const AuthContext = createContext(null)
const TOKEN_KEY = 'inventory_token'

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem(TOKEN_KEY))
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(Boolean(token))

  useEffect(() => {
    if (!token) { setLoading(false); return }
    api.get('/auth/me').then(({ data }) => setUser(data)).catch(() => {
      localStorage.removeItem(TOKEN_KEY); setToken(null); setUser(null)
    }).finally(() => setLoading(false))
  }, [token])

  async function login(credentials) {
    const { data } = await api.post('/auth/login', credentials)
    localStorage.setItem(TOKEN_KEY, data.access_token)
    setToken(data.access_token)
    const me = await api.get('/auth/me')
    setUser(me.data)
  }

  async function register(payload) {
    const { confirm, ...request } = payload
    await api.post('/auth/register', request)
    await login({ username: payload.username, password: payload.password })
  }

  function logout() {
    localStorage.removeItem(TOKEN_KEY); setToken(null); setUser(null)
  }

  const value = useMemo(() => ({ token, user, loading, login, register, logout, apiMessage }), [token, user, loading])
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) throw new Error('useAuth must be used inside AuthProvider')
  return context
}

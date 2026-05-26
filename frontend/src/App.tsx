import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from './store/authStore'
import { useState } from 'react'
import Navbar from './components/Navbar'
import Dashboard from './pages/Dashboard'
import Upload from './pages/Upload'
import Models from './pages/Models'
import Alerts from './pages/Alerts'
import Query from './pages/Query'

function Login() {
  const { login } = useAuthStore()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleLogin = async () => {
    try {
      setLoading(true)
      setError('')
      await login(email, password)
    } catch {
      setError('Invalid credentials')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{
      minHeight: '100vh',
      background: '#f7f5ff',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontFamily: 'DM Sans, sans-serif'
    }}>
      <div style={{
        background: 'rgba(255,255,255,0.7)',
        backdropFilter: 'blur(20px)',
        border: '1px solid rgba(255,255,255,0.8)',
        borderRadius: '16px',
        padding: '40px',
        width: '360px',
        boxShadow: '0 8px 32px rgba(109,40,217,0.1)'
      }}>
        <h1 style={{
          fontFamily: "'Playfair Display', serif",
          fontSize: '28px',
          fontWeight: 400,
          color: '#1e1233',
          marginBottom: '4px'
        }}>
          Nexa<em style={{ color: '#6d28d9' }}>IQ</em>
        </h1>
        <p style={{ color: '#3d3455', fontSize: '13px', marginBottom: '28px' }}>
          AI Decision Intelligence
        </p>
        {error && (
          <div style={{
            background: '#fef2f2',
            color: '#dc2626',
            fontSize: '13px',
            padding: '10px 14px',
            borderRadius: '8px',
            marginBottom: '16px'
          }}>{error}</div>
        )}
        <div style={{ marginBottom: '16px' }}>
          <label style={{ fontSize: '12px', color: '#4a4060', display: 'block', marginBottom: '6px' }}>
            Email
          </label>
          <input
            type="email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleLogin()}
            placeholder="test@nexaiq.com"
            style={{
              width: '100%',
              border: '1px solid rgba(109,40,217,0.15)',
              borderRadius: '8px',
              padding: '10px 14px',
              fontSize: '13px',
              outline: 'none',
              boxSizing: 'border-box'
            }}
          />
        </div>
        <div style={{ marginBottom: '24px' }}>
          <label style={{ fontSize: '12px', color: '#4a4060', display: 'block', marginBottom: '6px' }}>
            Password
          </label>
          <input
            type="password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleLogin()}
            placeholder="••••••••"
            style={{
              width: '100%',
              border: '1px solid rgba(109,40,217,0.15)',
              borderRadius: '8px',
              padding: '10px 14px',
              fontSize: '13px',
              outline: 'none',
              boxSizing: 'border-box'
            }}
          />
        </div>
        <button
          onClick={handleLogin}
          disabled={loading}
          style={{
            width: '100%',
            background: 'linear-gradient(135deg, #7c3aed, #6d28d9)',
            color: '#fff',
            border: 'none',
            borderRadius: '8px',
            padding: '12px',
            fontSize: '13px',
            fontWeight: 600,
            cursor: 'pointer',
            fontFamily: 'DM Sans, sans-serif'
          }}
        >
          {loading ? 'Signing in...' : 'Sign In →'}
        </button>
      </div>
    </div>
  )
}

function ProtectedLayout() {
  return (
    <div style={{ minHeight: '100vh', background: '#f7f5ff' }}>
      <Navbar />
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/upload" element={<Upload />} />
        <Route path="/models" element={<Models />} />
        <Route path="/alerts" element={<Alerts />} />
        <Route path="/query" element={<Query />} />
        <Route path="*" element={<Navigate to="/dashboard" />} />
      </Routes>
    </div>
  )
}

export default function App() {
  const { token } = useAuthStore()
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={token ? <Navigate to="/dashboard" /> : <Login />} />
        <Route path="/*" element={token ? <ProtectedLayout /> : <Navigate to="/" />} />
      </Routes>
    </BrowserRouter>
  )
}

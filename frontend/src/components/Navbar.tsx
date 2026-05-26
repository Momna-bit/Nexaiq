import { Link, useLocation } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'

export default function Navbar() {
  const { user, logout } = useAuthStore()
  const location = useLocation()

  const links = [
    { to: '/dashboard', label: 'Dashboard' },
    { to: '/upload', label: 'Upload' },
    { to: '/models', label: 'Models' },
    { to: '/alerts', label: 'Alerts' },
    { to: '/query', label: 'Ask Data' },
  ]

  return (
    <nav style={{
      background: 'rgba(247,245,255,0.85)',
      backdropFilter: 'blur(20px)',
      borderBottom: '1px solid rgba(109,40,217,0.1)',
      padding: '0 2rem',
      height: '60px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      position: 'sticky',
      top: 0,
      zIndex: 100
    }}>
      <span style={{
        fontFamily: "'Playfair Display', serif",
        fontSize: '18px',
        fontWeight: 600,
        color: '#1e1233'
      }}>
        Nexa<em style={{ color: '#6d28d9' }}>IQ</em>
      </span>

      <div style={{ display: 'flex', gap: '1.5rem', alignItems: 'center' }}>
        {links.map(link => (
          <Link
            key={link.to}
            to={link.to}
            style={{
              textDecoration: 'none',
              fontSize: '13px',
              fontFamily: 'DM Sans, sans-serif',
              fontWeight: 500,
              color: location.pathname === link.to ? '#6d28d9' : '#4a4060',
              borderBottom: location.pathname === link.to
                ? '2px solid #6d28d9' : 'none',
              paddingBottom: '2px'
            }}
          >
            {link.label}
          </Link>
        ))}
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
        {user && (
          <span style={{
            fontSize: '12px',
            color: '#6d28d9',
            background: '#ede9fe',
            padding: '4px 12px',
            borderRadius: '100px',
            fontFamily: 'DM Sans, sans-serif'
          }}>
            {user.role}
          </span>
        )}
        <button
          onClick={logout}
          style={{
            background: 'none',
            border: '1px solid rgba(109,40,217,0.2)',
            color: '#4a4060',
            padding: '6px 16px',
            borderRadius: '8px',
            cursor: 'pointer',
            fontSize: '13px',
            fontFamily: 'DM Sans, sans-serif'
          }}
        >
          Sign Out
        </button>
      </div>
    </nav>
  )
}

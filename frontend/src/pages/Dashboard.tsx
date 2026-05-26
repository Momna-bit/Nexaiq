import { useEffect, useState } from 'react'
import { useAuthStore } from '../store/authStore'
import axios from 'axios'

export default function Dashboard() {
  const { token, user } = useAuthStore()
  const [datasets, setDatasets] = useState([])
  const [models, setModels] = useState([])

  useEffect(() => {
    const headers = { Authorization: `Bearer ${token}` }
    axios.get('http://127.0.0.1:8002/datasets', { headers })
      .then(r => setDatasets(r.data)).catch(() => {})
    axios.get('http://127.0.0.1:8003/models', { headers })
      .then(r => setModels(r.data)).catch(() => {})
  }, [token])

  const cards = [
    { label: 'Datasets Uploaded', value: datasets.length, color: '#6d28d9' },
    { label: 'Models Trained', value: models.length, color: '#7c3aed' },
    { label: 'Best Accuracy', value: models.length > 0 ? `${(Math.max(...models.map((m:any) => m.best_score)) * 100).toFixed(1)}%` : 'N/A', color: '#8b5cf6' },
    { label: 'Services Running', value: 6, color: '#6d28d9' },
  ]

  return (
    <div style={{ padding: '2rem', maxWidth: '1120px', margin: '0 auto', fontFamily: 'DM Sans, sans-serif' }}>
      <h1 style={{
        fontFamily: "'Playfair Display', serif",
        fontSize: '28px',
        fontWeight: 400,
        color: '#1e1233',
        marginBottom: '8px'
      }}>
        Welcome back, <em style={{ color: '#6d28d9' }}>{user?.email?.split('@')[0]}</em>
      </h1>
      <p style={{ color: '#3d3455', fontSize: '14px', marginBottom: '32px' }}>
        Your NexaIQ platform overview
      </p>

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(4, 1fr)',
        gap: '16px',
        marginBottom: '32px'
      }}>
        {cards.map((card, i) => (
          <div key={i} style={{
            background: 'rgba(255,255,255,0.6)',
            backdropFilter: 'blur(16px)',
            border: '1px solid rgba(255,255,255,0.8)',
            borderRadius: '14px',
            padding: '20px',
            boxShadow: '0 2px 12px rgba(109,40,217,0.06)'
          }}>
            <div style={{
              fontSize: '32px',
              fontFamily: "'Playfair Display', serif",
              color: card.color,
              fontWeight: 500
            }}>
              {card.value}
            </div>
            <div style={{ fontSize: '12px', color: '#4a4060', marginTop: '6px' }}>
              {card.label}
            </div>
          </div>
        ))}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
        <div style={{
          background: 'rgba(255,255,255,0.6)',
          backdropFilter: 'blur(16px)',
          border: '1px solid rgba(255,255,255,0.8)',
          borderRadius: '14px',
          padding: '20px'
        }}>
          <h3 style={{ fontSize: '14px', fontWeight: 600, color: '#1e1233', marginBottom: '16px' }}>
            Recent Datasets
          </h3>
          {datasets.length === 0 ? (
            <p style={{ fontSize: '13px', color: '#4a4060' }}>
              No datasets yet. Upload your first CSV!
            </p>
          ) : (
            datasets.slice(0, 5).map((d: any) => (
              <div key={d.id} style={{
                display: 'flex',
                justifyContent: 'space-between',
                padding: '8px 0',
                borderBottom: '1px solid rgba(109,40,217,0.06)'
              }}>
                <span style={{ fontSize: '13px', color: '#1e1233' }}>{d.filename}</span>
                <span style={{
                  fontSize: '11px',
                  background: '#ede9fe',
                  color: '#6d28d9',
                  padding: '2px 8px',
                  borderRadius: '100px'
                }}>{d.status}</span>
              </div>
            ))
          )}
        </div>

        <div style={{
          background: 'rgba(255,255,255,0.6)',
          backdropFilter: 'blur(16px)',
          border: '1px solid rgba(255,255,255,0.8)',
          borderRadius: '14px',
          padding: '20px'
        }}>
          <h3 style={{ fontSize: '14px', fontWeight: 600, color: '#1e1233', marginBottom: '16px' }}>
            Trained Models
          </h3>
          {models.length === 0 ? (
            <p style={{ fontSize: '13px', color: '#4a4060' }}>
              No models yet. Upload data and train!
            </p>
          ) : (
            models.slice(0, 5).map((m: any) => (
              <div key={m.id} style={{
                display: 'flex',
                justifyContent: 'space-between',
                padding: '8px 0',
                borderBottom: '1px solid rgba(109,40,217,0.06)'
              }}>
                <span style={{ fontSize: '13px', color: '#1e1233' }}>{m.model_name}</span>
                <span style={{
                  fontSize: '11px',
                  background: '#ede9fe',
                  color: '#6d28d9',
                  padding: '2px 8px',
                  borderRadius: '100px'
                }}>{(m.best_score * 100).toFixed(1)}%</span>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  )
}

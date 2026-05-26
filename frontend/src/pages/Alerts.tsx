import { useState } from 'react'
import { useAuthStore } from '../store/authStore'
import axios from 'axios'

export default function Alerts() {
  const { token } = useAuthStore()
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)

  const runDetection = async () => {
    setLoading(true)
    try {
      const res = await axios.post('http://127.0.0.1:8004/detect-anomalies', {
        dataset_name: 'Revenue Data',
        data: [
          { revenue: 50000, customers: 100, churn_rate: 0.05 },
          { revenue: 52000, customers: 102, churn_rate: 0.04 },
          { revenue: 51000, customers: 98, churn_rate: 0.06 },
          { revenue: 49000, customers: 101, churn_rate: 0.05 },
          { revenue: 250000, customers: 99, churn_rate: 0.95 },
          { revenue: 53000, customers: 103, churn_rate: 0.04 },
          { revenue: 48000, customers: 97, churn_rate: 0.07 },
          { revenue: 51500, customers: 100, churn_rate: 0.05 }
        ]
      }, { headers: { Authorization: `Bearer ${token}` } })
      setResult(res.data)
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ padding: '2rem', maxWidth: '1120px', margin: '0 auto', fontFamily: 'DM Sans, sans-serif' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '32px' }}>
        <div>
          <h1 style={{ fontFamily: "'Playfair Display', serif", fontSize: '28px', fontWeight: 400, color: '#1e1233', marginBottom: '8px' }}>
            Anomaly <em style={{ color: '#6d28d9' }}>Alerts</em>
          </h1>
          <p style={{ color: '#3d3455', fontSize: '14px' }}>
            AI detects anomalies and generates executive alerts automatically.
          </p>
        </div>
        <button
          onClick={runDetection}
          disabled={loading}
          style={{
            background: 'linear-gradient(135deg, #7c3aed, #6d28d9)',
            color: '#fff', border: 'none', borderRadius: '8px',
            padding: '10px 24px', fontSize: '13px', fontWeight: 600,
            cursor: loading ? 'not-allowed' : 'pointer',
            fontFamily: 'DM Sans, sans-serif'
          }}
        >
          {loading ? 'Detecting...' : 'Run Detection'}
        </button>
      </div>

      {result && (
        <>
          <div style={{
            background: 'rgba(109,40,217,0.06)',
            border: '1px solid rgba(109,40,217,0.2)',
            borderRadius: '14px', padding: '20px', marginBottom: '20px'
          }}>
            <h3 style={{ fontSize: '15px', fontWeight: 600, color: '#1e1233', marginBottom: '12px' }}>
              {result.anomalies_found} Anomalies Detected
            </h3>
            <div style={{
              background: 'rgba(255,255,255,0.6)', borderRadius: '10px',
              padding: '14px 16px', fontSize: '13px', color: '#3d3455',
              lineHeight: 1.8, fontStyle: 'italic'
            }}>
              {result.ai_alert}
            </div>
          </div>

          <div style={{
            background: 'rgba(255,255,255,0.6)', backdropFilter: 'blur(16px)',
            border: '1px solid rgba(255,255,255,0.8)',
            borderRadius: '14px', padding: '20px'
          }}>
            <h3 style={{ fontSize: '14px', fontWeight: 600, color: '#1e1233', marginBottom: '16px' }}>
              Anomaly Details
            </h3>
            {result.anomalies.map((a: any, i: number) => (
              <div key={i} style={{
                padding: '12px 0', borderBottom: '1px solid rgba(109,40,217,0.06)',
                display: 'flex', justifyContent: 'space-between', alignItems: 'center'
              }}>
                <div>
                  <div style={{ fontSize: '13px', fontWeight: 600, color: '#1e1233' }}>
                    Column: <span style={{ color: '#6d28d9' }}>{a.column}</span>
                  </div>
                  <div style={{ fontSize: '12px', color: '#4a4060', marginTop: '2px' }}>
                    Value: {a.value} · Z-score: {a.z_score} · Mean: {a.mean}
                  </div>
                </div>
                <span style={{
                  fontSize: '11px', background: '#fef2f2', color: '#dc2626',
                  padding: '3px 10px', borderRadius: '100px', fontWeight: 600
                }}>
                  ANOMALY
                </span>
              </div>
            ))}
          </div>
        </>
      )}

      {!result && (
        <div style={{
          background: 'rgba(255,255,255,0.6)', backdropFilter: 'blur(16px)',
          border: '1px solid rgba(255,255,255,0.8)',
          borderRadius: '14px', padding: '40px', textAlign: 'center'
        }}>
          <p style={{ fontSize: '14px', color: '#4a4060' }}>
            Click "Run Detection" to scan your data for anomalies.
          </p>
        </div>
      )}
    </div>
  )
}

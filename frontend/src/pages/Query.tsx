import { useState } from 'react'
import { useAuthStore } from '../store/authStore'
import axios from 'axios'

const SUGGESTIONS = [
  'Show me all datasets I have uploaded',
  'Show me all trained ML models and their accuracy',
  'How many datasets do I have?',
  'Show me the latest model trained'
]

export default function Query() {
  const { token } = useAuthStore()
  const [question, setQuestion] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [error, setError] = useState('')

  const ask = async (q?: string) => {
    const query = q || question
    if (!query.trim()) return
    setLoading(true)
    setError('')
    setResult(null)
    try {
      const res = await axios.post('http://127.0.0.1:8005/ask',
        { question: query },
        { headers: { Authorization: `Bearer ${token}` } }
      )
      setResult(res.data)
      setQuestion(query)
    } catch (e: any) {
      setError(e.response?.data?.detail || 'Query failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ padding: '2rem', maxWidth: '1120px', margin: '0 auto', fontFamily: 'DM Sans, sans-serif' }}>
      <h1 style={{ fontFamily: "'Playfair Display', serif", fontSize: '28px', fontWeight: 400, color: '#1e1233', marginBottom: '8px' }}>
        Ask Your <em style={{ color: '#6d28d9' }}>Data</em>
      </h1>
      <p style={{ color: '#3d3455', fontSize: '14px', marginBottom: '32px' }}>
        Type a question in plain English — AI generates SQL and returns results instantly.
      </p>

      <div style={{
        background: 'rgba(255,255,255,0.6)', backdropFilter: 'blur(16px)',
        border: '1px solid rgba(255,255,255,0.8)', borderRadius: '14px',
        padding: '20px', marginBottom: '20px'
      }}>
        <div style={{ display: 'flex', gap: '10px' }}>
          <input
            value={question}
            onChange={e => setQuestion(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && ask()}
            placeholder="e.g. Show me all trained ML models and their accuracy"
            style={{
              flex: 1, border: '1px solid rgba(109,40,217,0.15)',
              borderRadius: '8px', padding: '12px 16px',
              fontSize: '14px', outline: 'none',
              fontFamily: 'DM Sans, sans-serif'
            }}
          />
          <button
            onClick={() => ask()}
            disabled={loading}
            style={{
              background: 'linear-gradient(135deg, #7c3aed, #6d28d9)',
              color: '#fff', border: 'none', borderRadius: '8px',
              padding: '12px 24px', fontSize: '13px', fontWeight: 600,
              cursor: loading ? 'not-allowed' : 'pointer',
              fontFamily: 'DM Sans, sans-serif', whiteSpace: 'nowrap'
            }}
          >
            {loading ? 'Thinking...' : 'Ask →'}
          </button>
        </div>

        <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', marginTop: '12px' }}>
          {SUGGESTIONS.map((s, i) => (
            <button
              key={i}
              onClick={() => ask(s)}
              style={{
                background: 'rgba(237,233,254,0.7)',
                border: '1px solid rgba(109,40,217,0.15)',
                color: '#6d28d9', padding: '5px 14px',
                borderRadius: '100px', fontSize: '12px',
                cursor: 'pointer', fontFamily: 'DM Sans, sans-serif'
              }}
            >
              {s}
            </button>
          ))}
        </div>
      </div>

      {error && (
        <div style={{ background: '#fef2f2', color: '#dc2626', padding: '12px 16px', borderRadius: '8px', fontSize: '13px', marginBottom: '16px' }}>
          {error}
        </div>
      )}

      {result && (
        <div style={{
          background: 'rgba(255,255,255,0.6)', backdropFilter: 'blur(16px)',
          border: '1px solid rgba(255,255,255,0.8)', borderRadius: '14px', padding: '20px'
        }}>
          <div style={{ marginBottom: '16px' }}>
            <div style={{ fontSize: '12px', color: '#4a4060', marginBottom: '6px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
              Generated SQL
            </div>
            <div style={{
              background: '#1e1233', color: '#a78bfa', padding: '12px 16px',
              borderRadius: '8px', fontSize: '12px', fontFamily: 'monospace',
              lineHeight: 1.6
            }}>
              {result.sql}
            </div>
          </div>

          <div style={{ fontSize: '12px', color: '#4a4060', marginBottom: '10px' }}>
            {result.row_count} rows returned
          </div>

          {result.data.length > 0 && (
            <div style={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '13px' }}>
                <thead>
                  <tr>
                    {result.columns.map((col: string) => (
                      <th key={col} style={{
                        textAlign: 'left', padding: '8px 12px',
                        background: 'rgba(109,40,217,0.06)',
                        color: '#6d28d9', fontSize: '11px',
                        textTransform: 'uppercase', letterSpacing: '0.5px',
                        borderBottom: '1px solid rgba(109,40,217,0.1)'
                      }}>
                        {col}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {result.data.map((row: any, i: number) => (
                    <tr key={i}>
                      {result.columns.map((col: string) => (
                        <td key={col} style={{
                          padding: '8px 12px',
                          borderBottom: '1px solid rgba(109,40,217,0.04)',
                          color: '#3d3455', fontSize: '12px',
                          maxWidth: '200px', overflow: 'hidden',
                          textOverflow: 'ellipsis', whiteSpace: 'nowrap'
                        }}>
                          {String(row[col] ?? '')}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

import { useEffect, useState } from 'react'
import { useAuthStore } from '../store/authStore'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import axios from 'axios'

export default function Models() {
  const { token } = useAuthStore()
  const [models, setModels] = useState([])
  const [loading, setLoading] = useState(true)
  const [training, setTraining] = useState(false)
  const [trainResult, setTrainResult] = useState<any>(null)

  useEffect(() => {
    axios.get('http://127.0.0.1:8003/models', {
      headers: { Authorization: `Bearer ${token}` }
    }).then(r => {
      setModels(r.data)
      setLoading(false)
    }).catch(() => setLoading(false))
  }, [token])

  const runQuickTrain = async () => {
    setTraining(true)
    try {
      const res = await axios.post('http://127.0.0.1:8003/train', {
        dataset_id: 'demo-dataset',
        target_column: 'churn',
        data: [
          { age: 30, salary: 50000, churn: 0 },
          { age: 45, salary: 75000, churn: 1 },
          { age: 28, salary: 42000, churn: 0 },
          { age: 52, salary: 90000, churn: 1 },
          { age: 35, salary: 60000, churn: 0 },
          { age: 41, salary: 70000, churn: 1 },
          { age: 29, salary: 45000, churn: 0 },
          { age: 38, salary: 65000, churn: 1 },
          { age: 44, salary: 80000, churn: 1 },
          { age: 31, salary: 55000, churn: 0 }
        ]
      }, { headers: { Authorization: `Bearer ${token}` } })
      setTrainResult(res.data)
      const r2 = await axios.get('http://127.0.0.1:8003/models', {
        headers: { Authorization: `Bearer ${token}` }
      })
      setModels(r2.data)
    } catch (e) {
      console.error(e)
    } finally {
      setTraining(false)
    }
  }

  const chartData = trainResult?.all_results?.map((r: any) => ({
    name: r.model_name.replace('Regression', 'Reg').replace('Forest', 'RF'),
    accuracy: parseFloat((r.metrics.accuracy * 100 || 0).toFixed(1)),
    f1: parseFloat((r.metrics.f1_score * 100 || 0).toFixed(1))
  })) || []

  return (
    <div style={{ padding: '2rem', maxWidth: '1120px', margin: '0 auto', fontFamily: 'DM Sans, sans-serif' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '32px' }}>
        <div>
          <h1 style={{ fontFamily: "'Playfair Display', serif", fontSize: '28px', fontWeight: 400, color: '#1e1233', marginBottom: '8px' }}>
            ML <em style={{ color: '#6d28d9' }}>Models</em>
          </h1>
          <p style={{ color: '#3d3455', fontSize: '14px' }}>
            AutoML trains 4 models and picks the best automatically.
          </p>
        </div>
        <button
          onClick={runQuickTrain}
          disabled={training}
          style={{
            background: 'linear-gradient(135deg, #7c3aed, #6d28d9)',
            color: '#fff', border: 'none', borderRadius: '8px',
            padding: '10px 24px', fontSize: '13px', fontWeight: 600,
            cursor: training ? 'not-allowed' : 'pointer',
            fontFamily: 'DM Sans, sans-serif'
          }}
        >
          {training ? '⏳ Training...' : '⚡ Run AutoML'}
        </button>
      </div>

      {trainResult && chartData.length > 0 && (
        <div style={{
          background: 'rgba(255,255,255,0.6)', backdropFilter: 'blur(16px)',
          border: '1px solid rgba(255,255,255,0.8)', borderRadius: '14px',
          padding: '24px', marginBottom: '24px'
        }}>
          <h3 style={{ fontSize: '14px', fontWeight: 600, color: '#1e1233', marginBottom: '8px' }}>
            🏆 Best Model: <span style={{ color: '#6d28d9' }}>{trainResult.best_model}</span>
            <span style={{ marginLeft: '8px', fontSize: '12px', background: '#ede9fe', color: '#6d28d9', padding: '2px 10px', borderRadius: '100px' }}>
              {(trainResult.best_score * 100).toFixed(1)}% accuracy
            </span>
          </h3>
          <p style={{ fontSize: '12px', color: '#4a4060', marginBottom: '20px' }}>Model comparison — all 4 models trained and evaluated</p>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(109,40,217,0.08)" />
              <XAxis dataKey="name" tick={{ fontSize: 12, fill: '#4a4060' }} />
              <YAxis tick={{ fontSize: 12, fill: '#4a4060' }} domain={[0, 100]} />
              <Tooltip
                contentStyle={{ background: 'rgba(255,255,255,0.9)', border: '1px solid rgba(109,40,217,0.15)', borderRadius: '8px', fontSize: '12px' }}
              />
              <Bar dataKey="accuracy" fill="#6d28d9" radius={[4, 4, 0, 0]} name="Accuracy %" />
              <Bar dataKey="f1" fill="#a78bfa" radius={[4, 4, 0, 0]} name="F1 Score %" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      <div style={{
        background: 'rgba(255,255,255,0.6)', backdropFilter: 'blur(16px)',
        border: '1px solid rgba(255,255,255,0.8)', borderRadius: '14px', padding: '20px'
      }}>
        <h3 style={{ fontSize: '14px', fontWeight: 600, color: '#1e1233', marginBottom: '16px' }}>All Trained Models</h3>
        {loading ? (
          <p style={{ fontSize: '13px', color: '#4a4060' }}>Loading...</p>
        ) : models.length === 0 ? (
          <p style={{ fontSize: '13px', color: '#4a4060' }}>No models yet. Click "Run AutoML" to train!</p>
        ) : (
          models.map((m: any) => (
            <div key={m.id} style={{
              display: 'flex', justifyContent: 'space-between', alignItems: 'center',
              padding: '12px 0', borderBottom: '1px solid rgba(109,40,217,0.06)'
            }}>
              <div>
                <div style={{ fontSize: '13px', fontWeight: 600, color: '#1e1233' }}>{m.model_name}</div>
                <div style={{ fontSize: '11px', color: '#4a4060', marginTop: '2px' }}>{m.problem_type} · target: {m.target_column}</div>
              </div>
              <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                <span style={{ fontSize: '11px', background: '#ede9fe', color: '#6d28d9', padding: '3px 10px', borderRadius: '100px', fontWeight: 600 }}>
                  {(m.best_score * 100).toFixed(1)}%
                </span>
                <span style={{ fontSize: '11px', background: 'rgba(16,185,129,0.1)', color: '#059669', padding: '3px 10px', borderRadius: '100px' }}>
                  {m.status}
                </span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

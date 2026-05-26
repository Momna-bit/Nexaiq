import { useState } from 'react'
import { useAuthStore } from '../store/authStore'
import axios from 'axios'

export default function Upload() {
  const { token } = useAuthStore()
  const [file, setFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [error, setError] = useState('')

  const handleUpload = async () => {
    if (!file) return
    setLoading(true)
    setError('')
    setResult(null)
    try {
      const formData = new FormData()
      formData.append('file', file)
      const res = await axios.post('http://127.0.0.1:8002/upload', formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data'
        }
      })
      setResult(res.data)
    } catch (e: any) {
      setError(e.response?.data?.detail || 'Upload failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto', fontFamily: 'DM Sans, sans-serif' }}>
      <h1 style={{ fontFamily: "'Playfair Display', serif", fontSize: '28px', fontWeight: 400, color: '#1e1233', marginBottom: '8px' }}>
        Upload <em style={{ color: '#6d28d9' }}>Data</em>
      </h1>
      <p style={{ color: '#3d3455', fontSize: '14px', marginBottom: '32px' }}>
        Upload a CSV file — it goes to Azure Blob Storage and runs through the pipeline automatically.
      </p>

      <div style={{
        background: 'rgba(255,255,255,0.6)',
        backdropFilter: 'blur(16px)',
        border: '2px dashed rgba(109,40,217,0.2)',
        borderRadius: '16px',
        padding: '40px',
        textAlign: 'center',
        marginBottom: '24px'
      }}>
        <div style={{ fontSize: '40px', marginBottom: '16px' }}>📁</div>
        <p style={{ fontSize: '14px', color: '#3d3455', marginBottom: '16px' }}>
          Select a CSV file to upload
        </p>
        <input
          type="file"
          accept=".csv"
          onChange={e => setFile(e.target.files?.[0] || null)}
          style={{ display: 'none' }}
          id="fileInput"
        />
        <label htmlFor="fileInput" style={{
          background: 'rgba(237,233,254,0.8)',
          color: '#6d28d9',
          border: '1px solid rgba(109,40,217,0.2)',
          padding: '10px 24px',
          borderRadius: '8px',
          cursor: 'pointer',
          fontSize: '13px',
          fontWeight: 500
        }}>
          Choose File
        </label>
        {file && (
          <p style={{ marginTop: '12px', fontSize: '13px', color: '#6d28d9', fontWeight: 500 }}>
            ✓ {file.name} selected
          </p>
        )}
      </div>

      {error && (
        <div style={{ background: '#fef2f2', color: '#dc2626', padding: '12px 16px', borderRadius: '8px', fontSize: '13px', marginBottom: '16px' }}>
          {error}
        </div>
      )}

      <button
        onClick={handleUpload}
        disabled={!file || loading}
        style={{
          background: file && !loading ? 'linear-gradient(135deg, #7c3aed, #6d28d9)' : '#e5e7eb',
          color: file && !loading ? '#fff' : '#9ca3af',
          border: 'none',
          borderRadius: '8px',
          padding: '12px 32px',
          fontSize: '14px',
          fontWeight: 600,
          cursor: file && !loading ? 'pointer' : 'not-allowed',
          width: '100%',
          fontFamily: 'DM Sans, sans-serif'
        }}
      >
        {loading ? '⏳ Uploading to Azure + Running Pipeline...' : 'Upload & Process →'}
      </button>

      {result && (
        <div style={{
          marginTop: '24px',
          background: 'rgba(237,233,254,0.5)',
          border: '1px solid rgba(109,40,217,0.2)',
          borderRadius: '12px',
          padding: '20px'
        }}>
          <h3 style={{ fontSize: '14px', fontWeight: 600, color: '#1e1233', marginBottom: '12px' }}>
            ✅ Upload Successful!
          </h3>
          <div style={{ fontSize: '13px', color: '#3d3455', lineHeight: 1.8 }}>
            <div><strong>File:</strong> {result.filename}</div>
            <div><strong>Dataset ID:</strong> {result.dataset_id}</div>
            <div><strong>Azure URL:</strong> <a href={result.blob_url} target="_blank" rel="noreferrer" style={{ color: '#6d28d9' }}>View in Azure →</a></div>
          </div>
        </div>
      )}
    </div>
  )
}

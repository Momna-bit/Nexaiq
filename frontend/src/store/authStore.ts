import { create } from 'zustand'
import axios from 'axios'

const API = 'http://127.0.0.1:8001'

interface AuthStore {
  token: string | null
  user: any | null
  login: (email: string, password: string) => Promise<void>
  logout: () => void
}

export const useAuthStore = create<AuthStore>((set) => ({
  token: localStorage.getItem('token'),
  user: null,

  login: async (email: string, password: string) => {
    const form = new URLSearchParams()
    form.append('username', email)
    form.append('password', password)
    const res = await axios.post(`${API}/auth/login`, form)
    const token = res.data.access_token
    localStorage.setItem('token', token)
    const me = await axios.get(`${API}/auth/me`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    set({ token, user: me.data })
  },

  logout: () => {
    localStorage.removeItem('token')
    set({ token: null, user: null })
  }
}))

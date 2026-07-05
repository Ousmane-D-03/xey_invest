import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'

export default function Dashboard() {
  const navigate = useNavigate()
  const [investments, setInvestments] = useState([])

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) {
      navigate('/login')
      return
    }
    api.get('/investments/me').then(response => {
      setInvestments(response.data)
    })
  }, [navigate])

  return (
    <div>
      <h1>Mon tableau de bord</h1>
      {investments.map(inv => (
        <div key={inv.id}>
          <p>Campagne : {inv.campaign_id}</p>
          <p>Parts : {inv.nombrePartAchetees}</p>
        </div>
      ))}
    </div>
  )
}
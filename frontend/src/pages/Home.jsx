import { useState, useEffect } from 'react'
import api from '../services/api'
import { Link } from 'react-router-dom'


function Home() {
  const [campaigns, setCampaigns] = useState([])

  useEffect(() => {
    api.get('/campaigns').then(response => {
      setCampaigns(response.data)
    })
  }, []) 

  return (

    <div>
      {campaigns.map(campaign => (
        <div key={campaign.id}>
          <h2>{campaign.title}</h2>
          <p>{campaign.description}</p>
          <Link to={`/campaigns/${campaign.id}`}>Voir les détails</Link>
        </div>
      ))}
    </div>
  )
}
export default Home


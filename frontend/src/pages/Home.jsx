import { useState, useEffect } from 'react'
import api from '../services/api'


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
        </div>
      ))}
    </div>
  )
}
export default Home
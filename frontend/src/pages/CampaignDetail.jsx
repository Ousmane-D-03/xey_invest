import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../services/api';


export default function CampaignDetail() {
  const { id } = useParams();

  const [campaign, setCampaign] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [nombreParts, setNombreParts] = useState(1)
  const [message, setMessage] = useState('')

  useEffect(() => {
    const fetchCampaign = async () => {
      try {
        setLoading(true);
        const response = await api.get(`/campaigns/${id}`);
        setCampaign(response.data);
        setError(null);
      } catch (err) {
        console.error('Erreur de chargement :', err);
        setError('Impossible de charger les détails de la campagne. Veuillez réessayer.');
      } finally {
        setLoading(false);
      }
    };


    if (id) {
      fetchCampaign();
    }

  }, [id]);

  const handleInvest = async (e) => {
    e.preventDefault();
    try {
      await api.post('/investments', {
        nombrePartAchetees: nombreParts,
        campaign_id: parseInt(id)
      });
      setMessage('Investissement réussi !');
    } catch (error) {
      setMessage(error.response?.data?.detail || 'Erreur lors de l\'investissement.');
    }
  };

  

  if (loading) return <p>Chargement des détails...</p>;
  if (error) return <p style={{ color: 'red' }}>{error}</p>;
  if (!campaign) return <p>Campagne introuvable.</p>;

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
      <h1>{campaign.title}</h1>
      <p style={{ fontSize: '1.2rem' }}>{campaign.description}</p>
      <hr />
      <p><strong>Objectif :</strong> {campaign.goal_amount} €</p>
      <p><strong>Taux de rendement :</strong> {(campaign.yield_rate * 100).toFixed(2)} %</p>
      <p><strong>Date de début :</strong> {new Date(campaign.start_date).toLocaleDateString()}</p>
      <p><strong>Date de fin :</strong> {new Date(campaign.end_date).toLocaleDateString()}</p>
      <p><strong>Statut :</strong> {campaign.status || 'Non spécifié'}</p>

    <form onSubmit={handleInvest}>
    <input
        type="number"
        min="1"
        value={nombreParts}
        onChange={(e) => setNombreParts(parseInt(e.target.value))}
    />
    <button type="submit">Investir</button>
    </form>
    {message && <p>{message}</p>}
    </div>
  );
}
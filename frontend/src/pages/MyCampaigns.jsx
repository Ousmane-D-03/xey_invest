import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

export default function MyCampaigns() {
  const navigate = useNavigate();
  const [campaigns, setCampaigns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
      return;
    }

    const fetchMyCampaigns = async () => {
      try {
        setLoading(true);
        const response = await api.get('/my-campaigns');
        setCampaigns(response.data);
        setError(null);
      } catch (err) {
        console.error(err);
        setError('Impossible de charger vos campagnes.');
        if (err.response?.status === 401) {
          localStorage.removeItem('token');
          navigate('/login');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchMyCampaigns();
  }, [navigate]);

  if (loading) return <p>Chargement de vos campagnes...</p>;
  if (error) return <p style={{ color: 'red' }}>{error}</p>;

  return (
    <div>
      <h2>Mes campagnes</h2>
      
      <button onClick={() => navigate('/campaigns/new')}>
        + Créer une campagne
      </button>

      {campaigns.length === 0 ? (
        <p>Vous n'avez pas encore créé de campagne.</p>
      ) : (
        <ul>
          {campaigns.map((camp) => (
            <li key={camp.id}>
              <strong>{camp.title}</strong> — {camp.description?.slice(0, 60)}...
              <br />
              Objectif : {camp.goal_amount} Cfa | Statut : {camp.status || 'Non défini'}
              <br />
              <button onClick={() => navigate(`/campaigns/${camp.id}`)}>
                Voir détail
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
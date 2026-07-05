import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';


export default function Admin() {
  const navigate = useNavigate();

  // ===== ÉTATS GÉNÉRAUX =====
  const [users, setUsers] = useState([]);
  const [campaigns, setCampaigns] = useState([]);
  const [investments, setInvestments] = useState([]);
  const [distributions, setDistributions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('users');
  
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
      return;
    }

    const fetchAllData = async () => {
      try {
        setLoading(true);
        setError(null);

        // Charger tous les utilisateurs (seul l'admin peut le faire)
        const usersRes = await api.get('/auth/users');
        setUsers(usersRes.data);

        // Charger toutes les campagnes
        const campaignsRes = await api.get('/campaign/campaigns');
        setCampaigns(campaignsRes.data);

        // Charger tous les investissements
        const investmentsRes = await api.get('/investment/investments');
        setInvestments(investmentsRes.data);

        // Charger toutes les distributions
        const distributionsRes = await api.get('/distribution/distributions');
        setDistributions(distributionsRes.data);

      } catch (err) {
        console.error('Erreur Admin :', err);
        if (err.response?.status === 403) {
          setError("Accès interdit. Vous n'avez pas les droits d'administrateur.");
          // Rediriger vers le dashboard après 3 secondes
          setTimeout(() => navigate('/dashboard'), 3000);
        } else if (err.response?.status === 401) {
          localStorage.removeItem('token');
          navigate('/login');
        } else {
          setError('Erreur de chargement des données. Veuillez réessayer.');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchAllData();
  }, [navigate]);

  const handleRoleChange = async (userId, newRole) => {
    try {
      await api.patch(`/auth/users/${userId}/role`, { role: newRole });
      // Mettre à jour la liste
      setUsers(users.map(u => u.id === userId ? { ...u, role: newRole } : u));
      alert(`Rôle de l'utilisateur ${userId} mis à jour vers ${newRole}`);
    } catch {
      alert('Erreur lors du changement de rôle');
    }
  };

  const handleDeleteUser = async (userId) => {
    if (!window.confirm(`Supprimer définitivement l'utilisateur ${userId} ?`)) return;
    try {
      await api.delete(`/auth/users/${userId}`);
      setUsers(users.filter(u => u.id !== userId));
      alert('Utilisateur supprimé');
    } catch {
      alert('Erreur lors de la suppression');
    }
  };

  const handleValidateCampaign = async (campaignId) => {
    try {
      await api.patch(`/campaign/campaigns/${campaignId}/status`, { status: 'active' });
      setCampaigns(campaigns.map(c => c.id === campaignId ? { ...c, status: 'active' } : c));
      alert('Campagne validée');
    } catch {
      alert('Erreur lors de la validation');
    }
  };

  const handleRejectCampaign = async (campaignId) => {
    try {
      await api.patch(`/campaign/campaigns/${campaignId}/status`, { status: 'rejected' });
      setCampaigns(campaigns.map(c => c.id === campaignId ? { ...c, status: 'rejected' } : c));
      alert('Campagne rejetée');
    } catch {
      alert('Erreur lors du rejet');
    }
  };

  // ===== ACTIONS INVESTISSEMENTS =====
  const handleValidateInvestment = async (investmentId) => {
    try {
      await api.patch(`/investment/investments/${investmentId}/status`, { status: 'validated' });
      setInvestments(investments.map(i => i.id === investmentId ? { ...i, status: 'validated' } : i));
      alert('Investissement validé');
    } catch {
      alert('Erreur lors de la validation');
    }
  };

  // ===== ACTIONS DISTRIBUTIONS =====
  const handleValidateDistribution = async (distributionId) => {
    try {
      await api.patch(`/distribution/distributions/${distributionId}/validate`, {});
      setDistributions(distributions.map(d => d.id === distributionId ? { ...d, status: 'validated' } : d));
      alert('Distribution validée');
    } catch {
      alert('Erreur lors de la validation');
    }
  };

  if (loading) return <p>⏳ Chargement du panneau d'administration...</p>;
  if (error) return <p style={{ color: 'red' }}>{error}</p>;

  const stats = {
    users: users.length,
    campaigns: campaigns.length,
    investments: investments.length,
    distributions: distributions.length,
  };

  return (
    <div>
      <h1>Panneau d'administration</h1>

      {/* Statistiques */}
      <div style={{ display: 'flex', gap: '20px', marginBottom: '20px' }}>
        <p><strong>Utilisateurs :</strong> {stats.users}</p>
        <p><strong>Campagnes :</strong> {stats.campaigns}</p>
        <p><strong>Investissements :</strong> {stats.investments}</p>
        <p><strong>Distributions :</strong> {stats.distributions}</p>
      </div>

      {/* Onglets */}
      <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
        <button onClick={() => setActiveTab('users')}>👥 Utilisateurs</button>
        <button onClick={() => setActiveTab('campaigns')}>📢 Campagnes</button>
        <button onClick={() => setActiveTab('investments')}>💰 Investissements</button>
        <button onClick={() => setActiveTab('distributions')}>📦 Distributions</button>
      </div>


      {activeTab === 'users' && (
        <div>
          <h2>Gestion des utilisateurs</h2>
          <p>Total : {users.length}</p>
          <table border="1" cellPadding="5">
            <thead>
              <tr>
                <th>ID</th>
                <th>Username</th>
                <th>Email</th>
                <th>Rôle</th>
                <th>Statut</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user) => (
                <tr key={user.id}>
                  <td>{user.id}</td>
                  <td>{user.username}</td>
                  <td>{user.email}</td>
                  <td>
                    <select
                      value={user.role}
                      onChange={(e) => handleRoleChange(user.id, e.target.value)}
                    >
                      <option value="investor">Investisseur</option>
                      <option value="project_owner">Porteur de projet</option>
                      <option value="admin">Admin</option>
                    </select>
                  </td>
                  <td>{user.status || 'Actif'}</td>
                  <td>
                    <button onClick={() => handleDeleteUser(user.id)} style={{ color: 'red' }}>
                      Supprimer
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}


      {activeTab === 'campaigns' && (
        <div>
          <h2>Gestion des campagnes</h2>
          <p>Total : {campaigns.length}</p>
          <table border="1" cellPadding="5">
            <thead>
              <tr>
                <th>ID</th>
                <th>Titre</th>
                <th>Objectif (€)</th>
                <th>Statut</th>
                <th>Propriétaire</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {campaigns.map((camp) => (
                <tr key={camp.id}>
                  <td>{camp.id}</td>
                  <td>{camp.title}</td>
                  <td>{camp.goal_amount}</td>
                  <td>
                    {camp.status === 'active' && 'Active'}
                    {camp.status === 'pending' && 'En attente'}
                    {camp.status === 'rejected' && 'Rejetée'}
                    {!camp.status && 'Non définie'}
                  </td>
                  <td>{camp.owner_id || 'N/A'}</td>
                  <td>
                    {camp.status !== 'active' && camp.status !== 'rejected' && (
                      <>
                        <button onClick={() => handleValidateCampaign(camp.id)} style={{ color: 'green' }}>
                          Valider
                        </button>
                        <button onClick={() => handleRejectCampaign(camp.id)} style={{ color: 'red' }}>
                          Rejeter
                        </button>
                      </>
                    )}
                    <button onClick={() => navigate(`/campaigns/${camp.id}`)}>Voir</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}


      {activeTab === 'investments' && (
        <div>
          <h2>Gestion des investissements</h2>
          <p>Total : {investments.length}</p>
          <table border="1" cellPadding="5">
            <thead>
              <tr>
                <th>ID</th>
                <th>Investisseur</th>
                <th>Campagne</th>
                <th>Parts</th>
                <th>Montant</th>
                <th>Statut</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {investments.map((inv) => (
                <tr key={inv.id}>
                  <td>{inv.id}</td>
                  <td>{inv.user_id}</td>
                  <td>{inv.campaign_id}</td>
                  <td>{inv.nombrePartAchetees}</td>
                  <td>{inv.montant || '—'}</td>
                  <td>{inv.status || 'En attente'}</td>
                  <td>
                    {inv.status !== 'validated' && (
                      <button onClick={() => handleValidateInvestment(inv.id)} style={{ color: 'green' }}>
                        Valider
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}


      {activeTab === 'distributions' && (
        <div>
          <h2>Gestion des distributions</h2>
          <p>Total : {distributions.length}</p>
          <table border="1" cellPadding="5">
            <thead>
              <tr>
                <th>ID</th>
                <th>Campagne</th>
                <th>Date</th>
                <th>Montant total</th>
                <th>Statut</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {distributions.map((dist) => (
                <tr key={dist.id}>
                  <td>{dist.id}</td>
                  <td>{dist.campaign_id}</td>
                  <td>{new Date(dist.dateDistribution).toLocaleDateString()}</td>
                  <td>{dist.montantTotal || '—'}</td>
                  <td>{dist.status || 'En attente'}</td>
                  <td>
                    {dist.status !== 'validated' && (
                      <button onClick={() => handleValidateDistribution(dist.id)} style={{ color: 'green' }}>
                        Valider
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
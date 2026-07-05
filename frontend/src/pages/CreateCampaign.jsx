import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

export default function CreateCampaign() {
  const navigate = useNavigate();
  
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [sector, setSector] = useState('');
  const [goalAmount, setGoalAmount] = useState('');
  const [unitPrice, setUnitPrice] = useState('');
  const [totalParts, setTotalParts] = useState('');
  const [yieldRate, setYieldRate] = useState('');
  const [repaymentDuration, setRepaymentDuration] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);


  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError(null);

    const payload = {
      title,
      description,
      sector,
      goal_amount: parseFloat(goalAmount),
      unit_price: parseFloat(unitPrice),
      total_parts: parseInt(totalParts, 10),
      yield_rate: parseFloat(yieldRate),
      repayment_duration: parseInt(repaymentDuration, 10),
      start_date: startDate, 
      end_date: endDate,
    };

    try {
      const response = await api.post('/campaign/campaigns', payload);
      console.log('Campagne créée :', response.data);
      
      navigate('/my-campaigns');
    } catch (err) {
      console.error('Erreur :', err);
      setError(err.response?.data?.detail || 'Erreur lors de la création de la campagne.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Créer une campagne</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      
      <form onSubmit={handleSubmit}>
        {/* Titre */}
        <div>
          <label>Titre *</label><br />
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
          />
        </div>

        {/* Description */}
        <div>
          <label>Description *</label><br />
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
          />
        </div>

        {/* Secteur */}
        <div>
          <label>Secteur *</label><br />
          <input
            type="text"
            value={sector}
            onChange={(e) => setSector(e.target.value)}
            required
          />
        </div>

        {/* Objectif de collecte */}
        <div>
          <label>Objectif (€) *</label><br />
          <input
            type="number"
            step="0.01"
            value={goalAmount}
            onChange={(e) => setGoalAmount(e.target.value)}
            required
          />
        </div>

        {/* Prix unitaire de la part */}
        <div>
          <label>Prix unitaire de la part (€) *</label><br />
          <input
            type="number"
            step="0.01"
            value={unitPrice}
            onChange={(e) => setUnitPrice(e.target.value)}
            required
          />
        </div>

        {/* Nombre total de parts */}
        <div>
          <label>Nombre total de parts *</label><br />
          <input
            type="number"
            step="1"
            value={totalParts}
            onChange={(e) => setTotalParts(e.target.value)}
            required
          />
        </div>

        {/* Taux de rendement (%) */}
        <div>
          <label>Taux de rendement (%) *</label><br />
          <input
            type="number"
            step="0.01"
            value={yieldRate}
            onChange={(e) => setYieldRate(e.target.value)}
            required
          />
        </div>

        {/* Durée de remboursement (mois) */}
        <div>
          <label>Durée de remboursement (mois) *</label><br />
          <input
            type="number"
            step="1"
            value={repaymentDuration}
            onChange={(e) => setRepaymentDuration(e.target.value)}
            required
          />
        </div>

        {/* Date de début */}
        <div>
          <label>Date de début *</label><br />
          <input
            type="datetime-local"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            required
          />
        </div>

        {/* Date de fin */}
        <div>
          <label>Date de fin *</label><br />
          <input
            type="datetime-local"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            required
          />
        </div>

        <br />
        <button type="submit" disabled={loading}>
          {loading ? 'Création en cours...' : 'Créer la campagne'}
        </button>
        <button type="button" onClick={() => navigate('/my-campaigns')}>
          Annuler
        </button>
      </form>
    </div>
  );
}
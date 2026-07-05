import { useState } from 'react';
import api from '../services/api'


export function Register(){
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [username, setUsername] = useState('');
    const [role, setRole] = useState('investor');
    const [secteur_activite, setSecteur] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault()
        try {
            const response = await api.post('/auth/register', { email, password, username, role, secteur_activite })
            const token = response.data.access_token
            localStorage.setItem('token', token)
            console.log('inscrit ! Token :', token)
        } catch (error) {
            console.log('Erreur :', error.response.data.detail)
        }
    }

     return (
    <form onSubmit={handleSubmit}>
      <input 
        type="email" 
        placeholder="Email" 
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input 
        type="text" 
        placeholder="Nom d'utilisateur" 
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
        <input 
        type="password" 
        placeholder="Mot de passe" 
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
        <select value={role} onChange={(e) => setRole(e.target.value)} required>
            <option value="investor">Investisseur</option>
            <option value="project_owner">Porteur de projet</option>
            <option value="admin">Admin</option>
        </select>
      <input 
        type="text" 
        placeholder="Secteur" 
        value={secteur_activite}
        onChange={(e) => setSecteur(e.target.value)}
      />
      <button type="submit">S'inscrire</button>
    </form>
  );
}

export default Register;
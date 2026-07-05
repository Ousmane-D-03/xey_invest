import { useState } from 'react';
import api from '../services/api'

export function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');


const handleSubmit = async (event) => {
  event.preventDefault()
  try {
    const response = await api.post('/auth/login', { email, password })
    const token = response.data.access_token
    localStorage.setItem('token', token)
    console.log('Connecté ! Token :', token)
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
        onChange={(e) => setEmail(e.target.value)} // Met à jour l'état en direct
      />
      <input 
        type="password" 
        placeholder="Mot de passe" 
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button type="submit">Se connecter</button>
    </form>
  );
}

export default Login;
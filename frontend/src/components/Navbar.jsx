import { Link } from 'react-router-dom'


export function Navbar() {
    const token = localStorage.getItem('token')
    return (
        <nav>
        <Link to="/">Accueil</Link>
        {token ? (
        <>
            <Link to="/dashboard">Dashboard</Link>
            <button onClick={() => { localStorage.removeItem('token'); window.location.reload() }}>
            Déconnexion
            </button>
        </>
        ) : (
        <>
            <Link to="/login">Connexion</Link>
            <Link to="/register">S'inscrire</Link>
        </>
        )}
        </nav>
    )
}
export default Navbar
import './navbar.css'

const Navbar = () => {
    return (
      <div className='navbar'>
        <ul>
          <li className="nav-item">
            <a className="navbar-brand" href="/">
              Home
            </a>
            <a className="navbar-brand" href="/logout">
              Logout
            </a>
            <a className="navbar-brand" href="/login">
              Login
            </a>
            <a className="navbar-brand" href="/registration">
              Novo Usuario
            </a>
            <a className="navbar-brand" href="/characters">
              Personagens
            </a>
          </li>
        </ul>
      </div>
    );
  }
  
  export default Navbar;
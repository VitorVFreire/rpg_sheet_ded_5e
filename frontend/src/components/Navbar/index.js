import React from 'react';
import './navbar.css'

const Navbar = (props) => {
  return (
    <div className='navbar'>
      <ul>
        <li className="nav-item">
          <a className="navbar-brand" href="/">
            Home
          </a>
          {props.isLoggedIn ? (
            <>
              <a className="navbar-brand" href="/logout">Logout</a>
              <a className="navbar-brand" href="/characters">Personagens</a>
            </>
          ) : (
            <>
              <a className="navbar-brand" href="/login">Login</a>
            </>
          )}
        </li>
      </ul>
    </div>
  );
}

export default Navbar;
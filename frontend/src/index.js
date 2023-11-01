import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'; 
import './index.css';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import CharactersPage from './pages/CharactersPage';
import CharacterPage from './pages/CharacterPage';

const idUser = window.initialData || false;

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <Router>
    <Routes> 
      <Route path="/" element={<HomePage idUser={idUser} />} />
      <Route path="/login" element={<LoginPage idUser={idUser} />} />
      <Route path='/personagens' element={<CharactersPage idUser={idUser} />} />
      <Route path='/personagem/:id' element={<CharacterPage idUser={idUser} />} />
    </Routes>
  </Router>
);


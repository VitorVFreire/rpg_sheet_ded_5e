import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'; 
import './index.css';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import CharactersPage from './pages/CharactersPage';
import CharacterPage from './pages/CharacterPage';
import CreateCharacter from './pages/CreateCharacter'
import CreateUser from './pages/CreateUser';

const idUser = window.initialData || false;

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <Router>
    <Routes> 
      <Route path="/" element={<HomePage idUser={idUser} />} />
      <Route path="/user_registration" element={<CreateUser idUser={idUser} />} />
      <Route path="/login" element={<LoginPage idUser={idUser} />} />
      <Route path="/create_character" element={<CreateCharacter idUser={idUser} />} />
      <Route path='/characters_page' element={<CharactersPage idUser={idUser} />} />
      <Route path='/character_page/:id' element={<CharacterPage idUser={idUser} />} />
    </Routes>
  </Router>
);


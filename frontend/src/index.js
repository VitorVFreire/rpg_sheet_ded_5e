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
import EquipmentRegister from './pages/EquipmentRegister';
import AddEquipment from './pages/AddEquipment';
import AddSpell from './pages/ModalSpells';
import SpellRegister from './pages/SpellRegister';
import RoomPage from './pages/RoomPage';
import Roons from './pages/Roons';

const idUser = window.initialData;

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <Router>
    <Routes> 
      <Route path='/' element={<HomePage idUser={idUser} />} />
      {/*User*/}
      <Route path='/user_registration' element={<CreateUser idUser={idUser} />} />
      <Route path='/login' element={<LoginPage idUser={idUser} />} />
      {/*Character*/}
      <Route path='/create_character' element={<CreateCharacter idUser={idUser} />} />
      <Route path='/characters_page' element={<CharactersPage idUser={idUser} />} />
      <Route path='/character_page/:id' element={<CharacterPage idUser={idUser} />} />
      {/*Room*/}
      <Route path='/roons_page' element={<Roons idUser={idUser} />} />
      <Route path='/room/:room_id/:user_room_id' element={<RoomPage idUser={idUser} />} />
      {/*Equipment*/}
      <Route path='/equipment_register' element={<EquipmentRegister idUser={idUser} />} /> {/*Admin*/}
      <Route path='/add_equipment/:id' element={<AddEquipment idUser={idUser} />} />
      {/*Spell*/}
      <Route path='/spell_register' element={<SpellRegister idUser={idUser} />} /> {/*Admin*/}
    </Routes>
  </Router>
);


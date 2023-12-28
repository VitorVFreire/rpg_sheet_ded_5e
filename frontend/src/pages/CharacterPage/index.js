import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import './CharacterPage.css'
import Navbar from '../../components/Navbar';
import Character from './Character';
import Characteristics from './Characteristic';
import Attribute from './Attribute';
import SavingThrow from './SavingThrow';
import StatusBase from './StatusBase';
import Skill from './Skill';
import Spell from './Spell';
import Coin from './Coin';

function CharacterPage(props) {
    const { id } = useParams();
    return (
        <div className='character-page'>
            <Navbar isLoggedIn={props.idUser} />
            <Character id={id} />
            <StatusBase id={id} />
            <div className='main'>
                <Attribute id={id} />
                <div className='div1'>
                    <SavingThrow id={id} />
                    <Coin id={id} />
                </div>
                <Characteristics id={id} />
                <Skill id={id} />
            </div>
            <div className='additional-components'>
                <Spell id={id} />
            </div>
        </div>
    );
}

export default CharacterPage;


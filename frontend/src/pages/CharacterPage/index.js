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
import ButtonLink from '../../components/ButtonLink';
import ModalSpells from '../ModalSpells';

function CharacterPage(props) {
    const { id } = useParams();
    const [modalSpellsIsOpen, setModalSpellsIsOpen] = useState(false);

    function openModalSpells() {
        setModalSpellsIsOpen(true);
    }

    function closeModalSpells() {
        setModalSpellsIsOpen(false);
    }
    return (
        <div className='character-page'>
            <Navbar isLoggedIn={props.idUser} />
            <Character id={id} />
            <div className='main'>
                <Attribute id={id} />
                <div className='div1'>
                    <SavingThrow id={id} />
                    <Skill id={id} />
                </div>
                <div className='div2'>
                    <StatusBase id={id} />
                </div>
                <Characteristics id={id} />
            </div>
            <div className='additional-components'>
                <button onClick={openModalSpells}>click</button>
                <ModalSpells id={id} modalSpellsIsOpen={modalSpellsIsOpen} closeModalSpells={closeModalSpells} />
                <h3>Spell: </h3>
                <Spell id={id} />
            </div>
        </div>
    );
}

export default CharacterPage;


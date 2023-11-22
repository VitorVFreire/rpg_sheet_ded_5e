import React, { useEffect } from 'react';
import './CharactersPage.css';
import Navbar from '../../components/Navbar';
import CharactersSection from './charactersSection';
import ButtonLink from '../../components/ButtonLink';

function CharactersPage(props) {
    const idUser = props.idUser; 
    useEffect(() => {
        document.title = 'Personagens';
      }, []);
    return (
        <div>
            <Navbar isLoggedIn={idUser} />
            <div className='content'>
                <div>
                    <ButtonLink link='/create_character' text='Criar Personagem'/>
                    <ButtonLink link='/room' text='Entrar Sala'/>
                </div>
                <CharactersSection />
            </div>
        </div>
    );
}

export default CharactersPage;

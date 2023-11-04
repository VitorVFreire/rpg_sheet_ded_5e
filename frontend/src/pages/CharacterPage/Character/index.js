import React, { useEffect, useState } from 'react';
import CustomInput from '../../../components/CustomInput';
import './Character.css';

function Character(props) {
    const [character, setCharacter] = useState([]);

    useEffect(() => {
        async function fetchCharacter() {
            try {
                const response = await fetch('/character/' + props.id);
                const data = await response.json();
                if (data !== false) {
                    setCharacter(data);
                } else {
                    console.error('Erro ao buscar dados');
                }
            } catch (error) {
                console.error('Erro na requisição:', error);
            }
        }

        fetchCharacter();
    }, [props.id]);

    const namePage = character['name_character']

    useEffect(() => {
        document.title = namePage;
    }, [namePage]);

    return (
        <section className='character_inputs'>
            <div>
                <CustomInput
                    characterID={props.id}
                    label='Nome'
                    type={'text'}
                    id={'personagem'}
                    name='name_character'
                    InputValue={character['name_character']}
                />
            </div>
        </section>
    );
}

export default Character;
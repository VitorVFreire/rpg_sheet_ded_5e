import React, { useEffect, useState } from 'react';
import CustomInput from '../../../components/CustomInput';
import './Character.css';
import DropdownList from '../../../components/DropdownListMethodGet';
import LoadingIndicator from '../../../components/LoadingIndicator/LoadingIndicator';
import requestInput from '../../../server/requestInput';

function Character(props) {
    const [character, setCharacter] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        async function fetchCharacter() {
            try {
                const response = await fetch('/character/' + props.id);
                const data = await response.json();
                if (data.result !== false) {
                    if (data.data !== null) {
                        setCharacter(data.data);
                    }
                } else {
                    console.error('Erro ao buscar dados');
                }
            } catch (error) {
                console.error('Erro na requisição:', error);
            }
        }

        fetchCharacter();
    }, [props.id]);

    const namePage = character['character_name']

    useEffect(() => {
        document.title = namePage;
    }, [namePage]);

    const handleSelectItem = (race_id, text) => {
        requestInput('race_id', race_id, 'character', props.id, 'PUT', setLoading);
    }

    return (
        <section className='character_inputs'>
            <CustomInput
                characterID={props.id}
                label='Nome'
                type={'text'}
                id={'character'}
                name='character_name'
                InputValue={character['character_name']}
            />
            <div>
                <label>Raça</label>
                <DropdownList
                    url={`/character_race/${props.id}`}
                    label={character['race_name']}
                    valueLabel={character['race_id']}
                    id='race_id'
                    name='race_name'
                    className='dropDawnListCharacterRaces'
                    handleSelectItem={handleSelectItem}
                />
            </div>
        </section>
    );
}

export default Character;
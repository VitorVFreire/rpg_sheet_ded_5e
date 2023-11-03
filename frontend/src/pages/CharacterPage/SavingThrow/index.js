import './SavingThrow.css';
import React, { useEffect, useState } from 'react';
import CustomInput from '../../../components/CustomInput';

function SavingThrow(props) {
    const url = 'salvaguardas';
    const [savingThrow, setSavingThrow] = useState({});
    const [checkedSavingThrows, setCheckedSavingThrows] = useState([]);

    const list = {
        'strength_resistance': 'Resistência de Força',
        'dexterity_resistance': 'Resistência de Destreza',
        'intelligence_resistance': 'Resistência de Inteligência',
        'constituition_resistance': 'Resistência de Constituição',
        'wisdom_resistance': 'Resistência de Sabedoria',
        'charisma_resistance': 'Resistência de Carisma',
    }

    useEffect(() => {
        async function fetchSavingThrow() {
            try {
                const response = await fetch('/' + url + '/' + props.id);
                const data = await response.json();
                if (data !== false) {
                    setSavingThrow(data);
                    setCheckedSavingThrows(data.saving_throw_name_list || []);
                } else {
                    console.error('Erro ao buscar dados');
                }
            } catch (error) {
                console.error('Erro na requisição:', error);
            }
        }

        fetchSavingThrow();
    }, [props.id]);

    return (
        <section className='saving_throw'>
            {Object.entries(list).map(([key, value]) => (
                <div key={key}>
                    <CustomInput
                        characterID={props.id}
                        label={value}
                        type='checkbox'
                        id={url}
                        name={key}
                        checked={checkedSavingThrows.includes(key)}
                    />
                    <div id={key}>
                        {savingThrow[key]}
                    </div>
                </div>
            ))}
        </section>
    );    
}

export default SavingThrow;
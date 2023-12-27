import './SavingThrow.css';
import React, { useEffect, useState } from 'react';
import CustomInput from '../../../components/CustomInput';

function SavingThrow(props) {
    const url = 'saving_throws';
    const [savingThrow, setSavingThrow] = useState({});
    const [checkedSavingThrows, setCheckedSavingThrows] = useState([]);

    const list = {
        'strength_resistance': 'Força',
        'dexterity_resistance': 'Destreza',
        'intelligence_resistance': 'Inteligência',
        'constitution_resistance': 'Constituição',
        'wisdom_resistance': 'Sabedoria',
        'charisma_resistance': 'Carisma',
    }

    useEffect(() => {
        async function fetchSavingThrow() {
            try {
                const response = await fetch('/' + url + '/' + props.id);
                const data = await response.json();
                if (data.result !== false) {
                    if (data.data !== null) {
                        setSavingThrow(data.data);
                        setCheckedSavingThrows(data.data.saving_throw_name_list || []);
                    }
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
        <section className='saving_throw' style={{border: '30px solid transparent', borderImage: `url("/openimg/borda.png") 100 round`}}>
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
                    <div className='bonus-container'>
                        <div name='bonus' id={key}>
                            {savingThrow[key]}
                        </div>
                    </div>
                </div>
            ))}
        </section>
    );
}

export default SavingThrow;
import React, { useEffect, useState } from 'react';
import CustomInput from '../../../components/CustomInput';
import './StatusBase.css';
import { list } from 'postcss';

function StatusBase(props) {
    const [statusBase, setStatusBase] = useState([]);

    list = {
        'level': 'Nivel',
        'alignment': 'Alinhamento',
        'faction': 'Facção',
        'background': 'Antecedente',
        'experience_points': 'xp',
        'movement': 'Deslocamento',
        'initiative': 'Iniciativa',
        'hit_points': 'Vida',
        'current_hit_points': 'Vida Atual',
        'temporary_hit_points': 'Vida Temporaria',
        'inspiration': 'Inpiração',
        'armor_class': 'ca'
    }

    const types = {
        'level': 'number',
        'alignment': 'text',
        'faction': 'text',
        'background': 'text',
        'experience_points': 'number',
        'movement': 'number',
        'initiative': 'number',
        'hit_points': 'number',
        'current_hit_points': 'number',
        'temporary_hit_points': 'number',
        'inspiration': 'number',
        'armor_class': 'number'
    }

    useEffect(() => {
        async function fetchStatusBase() {
            try {
                const response = await fetch('/status_base/' + props.id);
                const data = await response.json();
                if (data !== false) {
                    setStatusBase(data);
                } else {
                    console.error('Erro ao buscar dados');
                }
            } catch (error) {
                console.error('Erro na requisição:', error);
            }
        }

        fetchStatusBase();
    }, [props.id]);

    return (
        <section className='status_base'>
            {Object.entries(list).map(([key, value]) => (
                <div key={key}>
                    <CustomInput
                        characterID={props.id}
                        label={value}
                        type={types[key]}
                        id={'status_base'}
                        name={key}
                        InputValue={statusBase[key]}
                    />
                </div>
            ))}
        </section>
    );
}

export default StatusBase;
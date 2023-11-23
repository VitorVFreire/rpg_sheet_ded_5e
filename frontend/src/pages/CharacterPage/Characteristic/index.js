import React, { useEffect, useState } from 'react';
import CustomInput from '../../../components/CustomInput';
import './Characteristic.css';

function Characteristics(props) {
    const [characteristics, setCharacteristics] = useState([]);

    const list = {
        'age': 'Idade',
        'height': 'Altura',
        'weight': 'Peso',
        'eye_color': 'Cor dos Olhos',
        'skin_color': 'Cor da Pele',
        'color_hair': 'Cor do Cabelo',
        'character_image': 'Imagem do Personagem'
    }

    const types = {
        'age': 'number',
        'height': 'number',
        'weight': 'number',
        'eye_color': 'text',
        'skin_color': 'text',
        'color_hair': 'text',
        'character_image': 'file'
    }

    useEffect(() => {
        async function fetchCharacteristics() {
            try {
                const response = await fetch('/characteristics/' + props.id);
                const data = await response.json();
                if (data !== false) {
                    setCharacteristics(data);
                } else {
                    console.error('Erro ao buscar dados');
                }
            } catch (error) {
                console.error('Erro na requisição:', error);
            }
        }

        fetchCharacteristics();
    }, [props.id]);

    return (
        <section className='characteristics'>
            {Object.entries(characteristics).map(([key, value]) => (
                <div key={key}>
                    <CustomInput
                        characterID={props.id}
                        label={list[key]}
                        type={types[key]}
                        id={'characteristics'}
                        name={key}
                        accept={types[key] === 'file' ? 'image/*' : undefined}
                        InputValue={(types[key] !== 'file') ? value : undefined}
                        src={types[key] === 'file' ? value : undefined}
                    />
                </div>
            ))}
        </section>
    );
}

export default Characteristics;

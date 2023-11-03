import React, { useEffect, useState } from 'react';
import CustomInput from '../../../components/CustomInput';
import './Characteristic.css';

function Characteristics(props) {
    const [characteristics, setCharacteristics] = useState([]);

    const list = {
        'idade': 'Idade',
        'altura': 'Altura',
        'peso': 'Peso',
        'cor_olhos': 'Cor dos Olhos',
        'cor_pele': 'Cor da Pele',
        'cor_cabelo': 'Cor do Cabelo',
        'imagem_personagem': 'Imagem do Personagem'
    }

    const types = {
        'idade': 'number',
        'altura': 'number',
        'peso': 'number',
        'cor_olhos': 'text',
        'cor_pele': 'text',
        'cor_cabelo': 'text',
        'imagem_personagem': 'file'
    }

    useEffect(() => {
        async function fetchCharacteristics() {
            try {
                const response = await fetch('/caracteristicas/' + props.id);
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
                        id={'caracteristicas'}
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

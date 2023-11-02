import React, { useEffect, useState } from 'react';
import CustomInput from '../../../components/CustomInput';
import './Attribute.css'

function Attribute(props) {
    const [attributes, setAttribute] = useState([]);

    const list = {
        'strength': 'Força',
        'dexterity': 'Destreza',
        'intelligence': 'Inteligência',
        'constitution': 'Constituição',
        'wisdom': 'Sabedoria',
        'charisma': 'Carisma'
    }    

    const bonus = {
        'strength': 'strength_bonus',
        'dexterity': 'dexterity_bonus',
        'intelligence': 'intelligence_bonus',
        'constitution': 'constitution_bonus',
        'wisdom': 'wisdom_bonus',
        'charisma': 'charisma_bonus'
    }    

    useEffect(() => {
        async function fetchAttribute() {
            try {
                const response = await fetch('/atributos/' + props.id);
                const data = await response.json();
                if (data !== false) {
                    setAttribute(data);
                } else {
                    console.error('Erro ao buscar dados');
                }
            } catch (error) {
                console.error('Erro na requisição:', error);
            }
        }

        fetchAttribute();
    }, [props.id]);

    return (
        <section className='attributes'>
            {Object.entries(list).map(([key, value]) => (
                <div key={key}>
                    <CustomInput
                        characterID={props.id}
                        label={value}
                        InputValue={attributes[key]}
                        type='number'
                        id={'atributos'}
                        name={key}
                        min={1}
                        max={30}
                    />
                    <div id={bonus[key]} className='bonus'>
                        {attributes[bonus[key]]}
                    </div>
                </div>
            ))}
            <div>
                <CustomInput
                    characterID={props.id}
                    label='Bônus de Proficiência'
                    type='number'
                    id={'atributos'}
                    name={'proficiency_bonus'}
                    InputValue={attributes.proficiency_bonus}
                    min={0}
                />
            </div>
        </section>
    );
}

export default Attribute;
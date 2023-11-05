import './Skill.css';
import React, { useEffect, useState } from 'react';
import CustomInput from '../../../components/CustomInput';

function Skill(props) {
    const url = 'pericias';
    const [skills, setSkills] = useState({});
    const [checkedSkills, setCheckedSkills] = useState([]);

    const list = {
        'acrobatics': 'Acrobacia',
        'arcana': 'Arcanismo',
        'athletics': 'Atletismo',
        'performance': 'Atuacao',
        'deception': 'Enganacao',
        'stealth': 'Furtividade',
        'history': 'Historia',
        'intimidation': 'Intimidação',
        'insight': 'Intuição',
        'investigation': 'Investigação',
        'animal_handling': 'Lidar com Animais',
        'medicine': 'Medicina',
        'nature': 'Natureza',
        'perception': 'Percepção',
        'persuasion': 'Persuasao',
        'sleight_of_hand': 'Prestidigitação',
        'religion': 'Religião',
        'survival': 'Sobrevivencia'
    }

    useEffect(() => {
        async function fetchSkills() {
            try {
                const response = await fetch('/' + url + '/' + props.id);
                const data = await response.json();
                if (data !== false) {
                    setSkills(data.skills);
                    setCheckedSkills(data.character_skills || []);
                } else {
                    console.error('Erro ao buscar dados');
                }
            } catch (error) {
                console.error('Erro na requisição:', error);
            }
        }

        fetchSkills();
    }, [props.id]);

    return (
        <section className='skills'>
            {Object.entries(list).map(([key, value]) => (
                <div className='skill-container' key={key}>
                    <label htmlFor={key}>{value}</label>
                    <div className='skill_bonus' id={key}>
                        {skills[key]}
                    </div>
                    <CustomInput
                        characterID={props.id}
                        type='checkbox'
                        id={url}
                        name={key}
                        checked={checkedSkills.includes(key)}
                    />
                </div>
            ))}
        </section>
    );
}

export default Skill;
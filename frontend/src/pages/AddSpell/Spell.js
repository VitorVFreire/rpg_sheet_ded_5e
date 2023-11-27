// Spell.js
import React, { useEffect, useState } from 'react';
import CustomInput from '../../components/CustomInput';
import './Spell.css';

function Spell({ characterId }) {
  const [spellList, setSpellList] = useState([]);
  const [checkedSpells, setCheckedSpells] = useState([]);

  useEffect(() => {
    async function fetchSpells() {
      try {
        const response = await fetch(`/get_spell/${characterId}`);
        const data = await response.json();

        if (data.result) {
          setSpellList(data.data);
          setCheckedSpells(data.data.filter((item) => item.character_has).map((item) => item.spell_id));
        } else {
          console.error('Erro ao buscar dados de spells');
        }
      } catch (error) {
        console.error('Erro na requisição:', error);
      }
    }

    fetchSpells();
  }, [characterId]);

  return (
    <section className='spells'>
      {spellList.map((spell) => (
        <div className='spell-container' key={spell.spell_id}>
          <label htmlFor={`spell_${spell.spell_id}`}>
            <h3>{spell.spell_name}</h3>
          </label>
          <div className='spell_bonus'>{spell.description_spell}</div>
          <CustomInput
            characterID={characterId}
            type='checkbox'
            id='spell'
            name={spell.spell_id}
            checked={checkedSpells.includes(spell.spell_id)}
          />
        </div>
      ))}
    </section>
  );
}

export default Spell;

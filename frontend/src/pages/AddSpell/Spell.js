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
    <section className='spells-add'>
      {spellList.map((spell) => (
        <div className='spell-container' key={spell.spell_id}>
          <CustomInput
            characterID={characterId}
            type='checkbox'
            id='spell'
            name={spell.spell_id}
            checked={checkedSpells.includes(spell.spell_id)}
          />
          <label htmlFor={`spell_${spell.spell_id}`}>
            <h3>{spell.spell_name}</h3>
          </label>
          <h4>level:</h4> {spell.spell_level}
          <h4>Dados:</h4> {spell.amount_dice}d{spell.side_dice}
          <h4>Tipo de dano:</h4> {spell.type_damage_name}
          {spell.description_spell}
        </div>
      ))}
    </section>
  );
}

export default Spell;

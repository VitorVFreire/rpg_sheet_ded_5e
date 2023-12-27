import React, { useEffect, useRef, useState } from 'react';
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
      <table>
        <thead>
          <tr>
            <th>Selecionar</th>
            <th>Nome</th>
            <th>Nível</th>
            <th>Dados</th>
            <th>Tipo de Dano</th>
            <th>Descrição</th>
          </tr>
        </thead>
        <tbody>
          {spellList.map((spell) => (
            <tr key={spell.spell_id} className='spell-container'>
              <td>
                <CustomInput
                  characterID={characterId}
                  type='checkbox'
                  id='spell'
                  name={spell.spell_id}
                  checked={checkedSpells.includes(spell.spell_id)}
                />
              </td>
              <td>
                {spell.spell_name}
              </td>
              <td>
                {spell.spell_level}
              </td>
              <td>
                {`${spell.amount_dice}d${spell.side_dice}`}
              </td>
              <td>
                {spell.type_damage_name}
              </td>
              <td>{spell.description_spell}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}

export default Spell;



import React, { useEffect, useState } from 'react';
import './Spell.css';
import DeleteButton from '../../../components/DeleteButton';

function Spell(props) {
    const [spells, setSpells] = useState([]);

    useEffect(() => {
        async function fetchSpell() {
            try {
                const response = await fetch('/spell/' + props.id);
                const data = await response.json();
                if (data.result !== false) {
                    if (data.data !== null){
                        setSpells(data.data);
                    }
                } else {
                    console.error('Erro ao buscar dados');
                }
            } catch (error) {
                console.error('Erro na requisição:', error);
            }
        }

        fetchSpell();
    }, [props.id]);

    const handleCharacterDeleted = (outherId) => {
        const updatedSpell = spells.filter((spell) => spell.spell_id !== outherId);
        setSpells(updatedSpell);
    };

    return (
        <section className='spells'>
            {spells.map((spell, index) => (
                <div id='spell' className='spell'>
                    <div>
                        <DeleteButton url='spell' keyData='spell_id' outherId={spell.spell_id} characterId={props.id} onCharacterDeleted={handleCharacterDeleted} />
                    </div>
                    <h4>{spell.nome_habilidade}</h4>
                    <label>Nivel: {spell.spell_level}</label>
                    <label>Dados: {spell.amount_dice}D{spell.side_dice}</label>
                    <label>Bonus: {spell.attribute_use}</label>
                    <label>Tipo de Dano: {spell.type_damage}</label>
                    <label>Detalhes: {spell.description_spell}</label>
                </div>
            ))}
        </section>
    );
}

export default Spell;
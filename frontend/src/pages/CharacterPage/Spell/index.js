import React, { useEffect, useState } from 'react';
import './Spell.css';
import DeleteButton from '../../../components/DeleteButton';
import ModalSpells from './ModalSpells';

function Spell(props) {
    const [spells, setSpells] = useState([]);
    const [modalSpellsIsOpen, setModalSpellsIsOpen] = useState(false);

    function openModalSpells() {
        setModalSpellsIsOpen(true);
    }

    function closeModalSpells() {
        setModalSpellsIsOpen(false);
        fetchSpell();
    }

    async function fetchSpell() {
        try {
            const response = await fetch('/spell/' + props.id);
            const data = await response.json();
            if (data.result !== false) {
                if (data.data !== null) {
                    setSpells(data.data);
                }
            } else {
                console.error('Error retrieving data:', data.error || 'Unknown error');
            }
        } catch (error) {
            console.error('Request error:', error);
        }
    }

    useEffect(() => {
        fetchSpell();
    }, [props.id]);

    const handleCharacterDeleted = (otherId) => {
        const updatedSpell = spells.filter((spell) => spell.spell_id !== otherId);
        setSpells(updatedSpell);
    };

    return (
        <div>
            <ModalSpells id={props.id} modalSpellsIsOpen={modalSpellsIsOpen} closeModalSpells={closeModalSpells} />
            <div className='title_spell'>
                <button onClick={openModalSpells}>Adicionar Mágia</button>
                <h3>Spell: </h3>
            </div>
            <section className='spells'>
                {spells.map((spell, index) => (
                    <div key={spell.spell_id} className='spell'>
                        <div>
                            <DeleteButton
                                url={'/spell/' + props.id}
                                keyData='key'
                                outherId={spell.spell_id}
                                attFunction={handleCharacterDeleted}
                            />
                        </div>
                        <h4>{spell.spell_name}</h4>
                        <label>Nivel: {spell.spell_level}</label>
                        <label>Dados: {spell.amount_dice}D{spell.side_dice}</label>
                        <label>Bonus: {spell.attribute_use}</label>
                        <label>Tipo de Dano: {spell.type_damage_name}</label>
                        <label>Detalhes: {spell.description_spell}</label>
                    </div>
                ))}
            </section>
        </div>
    );
}

export default Spell;

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
                    setSpells(data.data);
                } else {
                    console.error('Erro ao buscar dados');
                }
            } catch (error) {
                console.error('Erro na requisição:', error);
            }
        }

        fetchSpell();
    }, [props.id]);

    console.log(spells)

    const handleCharacterDeleted = (outherId) => {
        const updatedSpell = spells.filter((spell) => spell.id_habilidade !== outherId);
        setSpells(updatedSpell);
    };

    return (
        <section className='spells'>
            {spells.map((spell, index) => (
                <div id='spell' className='spell'>
                    <div>
                        <DeleteButton url='spell' keyData='id_habilidade' outherId={spell.id_habilidade} characterId={props.id} onCharacterDeleted={handleCharacterDeleted} />
                    </div>
                    <h4>{spell.nome_habilidade}</h4>
                    <label>Nivel: {spell.nivel_habilidade}</label>
                    <label>Dados: {spell.qtd_dados}D{spell.lados_dados}</label>
                    <label>Bonus: {spell.nome_atributo}</label>
                    <label>Tipo de Dano: {spell.tipo_dano}</label>
                    <label>Detalhes: <a href={spell.link_detalhes} target='_blank'>Clique Aqui!</a></label>
                </div>
            ))}
        </section>
    );
}

export default Spell;
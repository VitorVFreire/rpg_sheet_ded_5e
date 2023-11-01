import React, { useEffect, useState } from 'react';
import CharacterDeleteButton from '../../components/CharacterDeleteButton';

function CharactersSection() {
  const [characters, setCharacters] = useState([]);

  useEffect(() => {
    async function fetchCharacters() {
      try {
        const response = await fetch('/characters');
        const data = await response.json();
        if (data !== false) {
          setCharacters(data);
        } else {
          console.error('Erro ao buscar dados');
        }
      } catch (error) {
        console.error('Erro na requisição:', error);
      }
    }

    fetchCharacters();
  }, []);

  const handleCharacterDeleted = (characterId) => {
    // Remove o personagem da lista com base no characterId
    const updatedCharacters = characters.filter((character) => character.id_personagem !== characterId);
    setCharacters(updatedCharacters);
  };

  return (
    <section className='characters'>
      {characters.map((character) => (
        <div key={character.id_personagem} className='character'>
          <div><img src={character.img} alt={character.nome_personagem} /></div>
          <div>{character.nome_personagem}</div>
          <div>{character.nome_raca}</div>
          <div><a href={`/personagem/${character.id_personagem}`}>Ficha</a></div>
          <div>
            <CharacterDeleteButton characterId={character.id_personagem} onCharacterDeleted={handleCharacterDeleted} />
          </div>
        </div>
      ))}
    </section>
  );
}

export default CharactersSection;
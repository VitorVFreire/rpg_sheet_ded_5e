import React, { useEffect, useState } from 'react';
import DeleteButton from '../../components/DeleteButton';

function CharactersSection() {
  const [characters, setCharacters] = useState([]);

  useEffect(() => {
    async function fetchCharacters() {
      try {
        const response = await fetch('/characters');
        const data = await response.json();
        if (data.result !== false) {
          if (data.data !== null){
            setCharacters(data.data);
          }
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
    const updatedCharacters = characters.filter((character) => character.character_id !== characterId);
    setCharacters(updatedCharacters);
  };

  return (
    <section className='characters'>
      {characters.map((character) => (
        <div key={character.character_id} className='character'>
          <div><img src={character.img} alt={character.character_name} /></div>
          <div>{character.character_name}</div>
          <div>{character.race_name}</div>
          <div><a href={`/character_page/${character.character_id}`}>Ficha</a></div>
          <div>
            <DeleteButton url={'/character/' + character.character_id} outherId={character.character_id} attFunction={handleCharacterDeleted} />
          </div>
        </div>
      ))}
    </section>
  );
}

export default CharactersSection;
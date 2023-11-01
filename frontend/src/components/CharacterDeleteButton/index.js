import React, { useState } from 'react';
import './characterDeleteButton.css';

const CharacterDeleteButton = ({ characterId, onCharacterDeleted }) => {
  const handleDelete = async () => {
    try {
      const response = await fetch(`/personagem/${characterId}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        onCharacterDeleted(characterId);
      } else {
        console.error('Erro ao excluir o personagem:', response.status);
      }
    } catch (error) {
      console.error('Erro na requisição:', error);
    }
  };

  return (
    <button className="delete-button" onClick={handleDelete}>
      <span className="delete-icon">X</span>
    </button>
  );
};

export default CharacterDeleteButton;


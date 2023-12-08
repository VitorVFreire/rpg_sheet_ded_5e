import React, { useState } from 'react';
import './DeleteButton.css';

const DeleteButton = ({ attFunction ,url, outherId, keyData }) => {
  const handleDelete = async () => {
    try {
      const json = {
        method: 'DELETE',
      };

      if (keyData) {
        const data = new FormData();
        data.append(keyData, outherId)
        json.body = data;
      }

      const response = await fetch(url, json);
      if (response.ok) {
        attFunction(outherId);
      } else {
        console.error('Erro ao excluir:', response.status);
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

export default DeleteButton;
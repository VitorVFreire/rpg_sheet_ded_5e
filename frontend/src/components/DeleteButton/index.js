import React, { useState } from 'react';
import './DeleteButton.css';
import LoadingIndicator from '../LoadingIndicator/LoadingIndicator';

const DeleteButton = ({ attFunction, url, outherId, keyData }) => {
  const [loading, setLoading] = useState(false);

  const handleDelete = async () => {
    try {
      setLoading(true);
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
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <LoadingIndicator loading={loading} />
      <button className="delete-button" onClick={handleDelete}>
        <span className="delete-icon">X</span>
      </button>
    </div>
  );
};

export default DeleteButton;
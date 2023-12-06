import React, { useState } from 'react';
import './ButtonAdd.css';

const ButtonAdd = ({ onAddSquare, url, value }) => {
    const [isLoading, setIsLoading] = useState(false);

    const handleClick = async () => {
        if (isLoading) {
            return;
        }

        setIsLoading(true);

        try {
            const formData = new FormData();
            formData.append('key', value);
            const response = await fetch(url, {
                method: 'POST',
                body: formData,
            });

            const responseData = await response.json();

            if (responseData.result !== false && responseData.data !== null) {
                onAddSquare(responseData.data);
            } else {
                console.error('Erro ao criar uma nova square');
            }
        } catch (error) {
            console.error('Erro na solicitação:', error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <button className="add-button" onClick={handleClick} disabled={isLoading}>
            {isLoading ? 'Aguarde...' : '+'}
        </button>
    );
};

export default ButtonAdd;



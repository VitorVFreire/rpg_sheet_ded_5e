import React, { useState } from 'react';
import './ButtonAdd.css';

const ButtonAdd = ({ url, value, method }) => {
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
                method: method,
                body: formData,
            });

            const responseData = await response.json();
        } catch (error) {
            console.error('Erro na solicitação:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const className = method == "POST" ? "add-button" : "delete-button"
    const text = method == "POST" ? "+" : "x"

    return (
        <button className={className} onClick={handleClick} disabled={isLoading}>
            {isLoading ? 'Aguarde...' : text}
        </button>
    );
};

export default ButtonAdd;



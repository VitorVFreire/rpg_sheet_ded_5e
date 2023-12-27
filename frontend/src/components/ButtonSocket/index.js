import React, { useState } from 'react';
import './ButtonSocket.css';
import LoadingIndicator from '../LoadingIndicator/LoadingIndicator';

const ButtonSocket = ({ url, value, method }) => {
    const [loading, setLoading] = useState(false);
    const handleClick = async () => {
        setLoading(true);
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
            setLoading(false);
        }
    };

    const className = method == "POST" ? "add" : "delete"
    const text = method == "POST" ? "+" : "x"

    return (
        <div>
            <LoadingIndicator loading={loading} />
            <button className={'button ' + className} onClick={handleClick}>
                {text}
            </button>
        </div>
    );
};

export default ButtonSocket;



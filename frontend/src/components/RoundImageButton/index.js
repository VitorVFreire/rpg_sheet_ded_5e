import React, { useState } from 'react';
import './RoundImageButton.css';
import LoadingIndicator from '../LoadingIndicator/LoadingIndicator';

const RoundImageButton = ({ imageUrl, url, square_id, method }) => {
    const [loading, setLoading] = useState(false);

    const handleImageUpload = async (e) => {
        setLoading(true);

        const file = e.target.files[0];
        if (!file) {
            return;
        }

        try {
            const formData = new FormData();
            formData.append('image', file);
            if (square_id) {
                formData.append('square_id', square_id);
            }

            const response = await fetch(url, {
                method: method,
                body: formData,
            });

            const responseData = await response.json();

            if (responseData.result !== false && responseData.data !== null) {
                console.log('ok')
            } else {
                console.error('Erro ao fazer upload da imagem');
            }
        } catch (error) {
            console.error('Erro na solicitação:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <LoadingIndicator loading={loading} />
            <label className="round-image-button" id={square_id} style={{ backgroundImage: `url(${imageUrl})` }}>
                <input type="file" accept='image/*' onChange={handleImageUpload} />
            </label>
        </div>

    );
};

export default RoundImageButton;

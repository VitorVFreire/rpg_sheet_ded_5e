import React, { useState, useEffect } from 'react';
import './LoadingIndicator.css';

const LoadingIndicator = ({ loading }) => {
    const [dotsCount, setDotsCount] = useState(1);

    useEffect(() => {
        let interval;

        if (loading) {
            interval = setInterval(() => {
                setDotsCount((prevCount) => (prevCount < 3 ? prevCount + 1 : 1));
            }, 500);
        }

        return () => {
            clearInterval(interval);
        };
    }, [loading]);

    return loading ? (
        <div style={loadingIndicatorStyle}>
            <div className="message">
                <b>Carregando<span className="dots">{Array(dotsCount).fill('.').join('')}</span></b>
            </div>
        </div>
    ) : null;
};

const loadingIndicatorStyle = {
    position: 'fixed',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    backgroundColor: 'rgba(0, 0, 0, 0.7)', 
    padding: '20px',
    borderRadius: '8px',
    textAlign: 'center', 
};

export default LoadingIndicator;




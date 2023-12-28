import React, { useState, useEffect } from 'react';
import './DropdownList.css';

function DropdownList({ url, label, valueLabel='', id, name, className = 'dropdownlist', handleSelectItem = () => {} }) {
    const [data, setData] = useState([]);
    const [selectedItem, setSelectedItem] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(url);
                const result = await response.json();

                if (result.result) {
                    setData(result.data);
                } else {
                    setError('Error fetching data');
                }
            } catch (error) {
                console.error('Error fetching data:', error);
                setError('Error fetching data');
            }
        };

        fetchData();
    }, [url]);

    const handleSelect = (item) => {
        const value = item.target.value
        const text = item.target.options[item.target.selectedIndex].text;
        setSelectedItem(value);
        handleSelectItem(value, text);
    };

    return (
        <div className={className}>
            <label>{label}</label>
            <select name={id} id={id} onChange={(e) => handleSelect(e)}>
                <option value={valueLabel}>{label}</option>
                {data.map((item) => (
                    <option key={item[id]} value={item[id]}>
                        {item[name]}
                    </option>
                ))}
            </select>
            {error && <div className="error-message">{error}</div>}
        </div>
    );
}

export default DropdownList;
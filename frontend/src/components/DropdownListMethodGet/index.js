import React, { useState, useEffect } from 'react';
import './DropdownList.css'

function DropdownList({ url, label, id, name}) {
    const [data, setData] = useState([]);
    const [selectedItem, setSelectedItem] = useState(null);

    useEffect(() => {
        fetch(url)
            .then((response) => response.json())
            .then((data) => {
                setData(data);
            })
            .catch((error) => {
                console.error('Erro ao buscar os dados da API:', error);
            });
    }, []);

    const handleSelect = (item) => {
        setSelectedItem(item);
    };

    return (
        <div>
            <label>{label}</label>
            <select name={id} id={id} onChange={(e) => handleSelect(e.target.value)}>
                <option value="">Selecione {label}</option>
                {data.map((item) => (
                    <option key={item[id]} value={item[id]}>
                        {item[name]}
                    </option>
                ))}
            </select>
        </div>
    );
}

export default DropdownList;

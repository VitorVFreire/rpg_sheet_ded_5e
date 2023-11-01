import React, { useState, useEffect, useRef } from 'react';
import { uploadImage } from '../../server/uploadImage'; // Certifique-se de importar a função corretamente
import requestInput from '../../server/requestInput';

function CustomInput({ type, name, id, required, placeholder, onInputBlur, defaultChecked, value, min, max, accept, label, characterID, src }) {
  const [inputValue, setInputValue] = useState(type === 'checkbox' ? true : value);
  const [imageUrl, setImageUrl] = useState(src);
  const fileInputRef = useRef(null);

  const handleBlur = (e) => {
    if (type === 'number' ||  type === 'text') {
      requestInput(name, inputValue, id, characterID, 'PUT');
    }
  };

  const handleChange = async (e) => {
    if (type === 'checkbox') {
      setInputValue(e.target.checked);
    } else if (type === 'file') {
      const selectedFile = e.target.files[0];
      const imageData = await uploadImage(selectedFile, characterID);
      if (imageData) {
        setImageUrl(imageData.url);
      }
    } else if (type === 'number' && (min || max)) {
      const numericValue = parseFloat(e.target.value);
      if (!isNaN(numericValue)) {
        const newValue = Math.min(Math.max(numericValue, min), max);
        setInputValue(newValue);
      }
    } else {
      setInputValue(e.target.value);
    }
  };

  const handleImageClick = () => {
    fileInputRef.current.click();
  };

  const displayInputDefault = src ? { display: 'none' } : undefined;
  return (
    <div>
      <label>{label}</label>
      <input
        type={type}
        name={name}
        id={id}
        required={required}
        placeholder={placeholder}
        defaultChecked={type === 'checkbox' ? defaultChecked : undefined}
        value={(type !== 'checkbox' && type !== 'file') ? inputValue : undefined}
        onBlur={handleBlur}
        onChange={handleChange}
        style={displayInputDefault}
        min={min}
        max={max}
        accept={accept}
      />
      <img
        src={imageUrl}
        id={'img' + id}
        className='characterImage'
        style={{ display: imageUrl ? 'block' : 'none' }}
        alt="Imagem do personagem"
        onClick={handleImageClick}
      />
      <input
        type="file"
        ref={fileInputRef}
        style={{ display: 'none' }}
        onChange={handleChange}
        accept="image/*"
      />
    </div>
  );
}

export default CustomInput;
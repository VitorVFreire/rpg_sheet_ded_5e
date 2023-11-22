import React, { useState, useEffect, useRef } from 'react';
import { uploadImage } from '../../server/uploadImage'; 
import requestInput from '../../server/requestInput';
import './CustomInput.css'

function CustomInput({ type, name, id, required, placeholder, checked, InputValue, min, max, accept, label, characterID, src }) {
  const [inputValue, setInputValue] = useState('');
  const [isChecked, setCheck] = useState(false);

  useEffect(() => {
    setInputValue(InputValue);
  }, [InputValue]);

  useEffect(() => {
    setCheck(checked);
  }, [checked]);

  const [imageUrl, setImageUrl] = useState(src);
  const fileInputRef = useRef(null);

  const handleBlur = (e) => {
    if (type === 'number' || type === 'text') {
      requestInput(name, inputValue, id, characterID, 'PUT');
    }
  };

  const handleCheckboxClick = () => {
    const newInputValue = !isChecked;

    if (type === 'checkbox') {
      setCheck(newInputValue);

      if (newInputValue) {
        requestInput(name, null, id, characterID, 'POST');
      } else {
        requestInput(name, null, id, characterID, 'DELETE');
      }
    }
  };

  const handleChange = async (e) => {
    if (type === 'file') {
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
        value={(type !== 'checkbox' && type !== 'file') ? inputValue : undefined}
        onBlur={handleBlur}
        onChange={handleChange}
        style={displayInputDefault}
        min={min}
        max={max}
        accept={accept}
        checked={type === 'checkbox' ? isChecked : undefined}
      />
      {type === 'checkbox' && (
        <span
          className={`checkmark ${isChecked ? 'checked' : ''}`}
          onClick={handleCheckboxClick}
        ></span>
      )}
      {type === 'file' && (
        <>
          <img
            src={imageUrl}
            id={'img' + id}
            className='characterImage'
            style={{ display: imageUrl ? 'block' : 'none' }}
            alt='Imagem do personagem'
            onClick={handleImageClick}
          />
          <input
            type='file'
            ref={fileInputRef}
            style={{ display: 'none' }}
            onChange={handleChange}
            accept='image/*'
          />
        </>
      )}
    </div>
  );
}

export default CustomInput;
// Equipment.js
import React, { useEffect, useState } from 'react';
import CustomInput from '../../components/CustomInput';
import './Equipment.css'

function Equipment({ characterId }) {
  const [equipmentList, setEquipmentList] = useState([]);
  const [checkedEquipment, setCheckedEquipment] = useState([]);

  useEffect(() => {
    async function fetchEquipment() {
      try {
        const response = await fetch(`/get_equipment/${characterId}`);
        const data = await response.json();

        if (data.result !== false && data.data !== null) {
          setEquipmentList(data.data);
          setCheckedEquipment(data.data.filter((item) => item.character_has).map((item) => item.equipment_id));
        } else {
          console.error('Erro ao buscar dados de equipamento');
        }
      } catch (error) {
        console.error('Erro na requisição:', error);
      }
    }

    fetchEquipment();
  }, [characterId]);

  return (
    <section className='equipment'>
      {equipmentList.map((equipment) => (
        <div className='equipment-container' key={equipment.equipment_id}>
          <label htmlFor={`equipment_${equipment.equipment_id}`}>
            <h3>{equipment.equipment_name}</h3>
          </label>
          <div className='equipment_bonus'>{equipment.description_equipment}</div>
          <CustomInput
            characterID={characterId}
            type='checkbox'
            id='equipments'
            name={equipment.equipment_id}
            checked={checkedEquipment.includes(equipment.equipment_id)}
          />
          {checkedEquipment.includes(equipment.equipment_id) && (<CustomInput
            characterID={characterId}
            label='Quantidade'
            type={'number'}
            id='equipments'
            name={equipment.equipment_id}
            InputValue={equipment.amount}
          /> )}
        </div>
      ))}
    </section>
  );
}

export default Equipment;

import React, { useEffect, useState } from 'react';
import CustomInput from '../../../components/CustomInput';
import './Coin.css';
import ModalCoins from './ModalCoins';

function Coin(props) {
    const [coins, setCoins] = useState([]);
    const [modalCoinsOpen, setModalCoinsOpen] = useState(false);

    function openModalCoins() {
        setModalCoinsOpen(true);
    }

    function closeModalCoins() {
        setModalCoinsOpen(false);
    }

    useEffect(() => {
        async function fetchCoins() {
            try {
                const response = await fetch('/coins/' + props.id);
                const data = await response.json();
                if (data.result !== false) {
                    if (data.data !== null) {
                        setCoins(data.data);
                    }
                } else {
                    console.error('Erro ao buscar dados');
                }
            } catch (error) {
                console.error('Erro na requisição:', error);
            }
        }

        fetchCoins();
    }, [props.id]);

    return (
        <section className='coins'>
            <ModalCoins id={props.id} ModalCoinsIsOpen={modalCoinsOpen} closeModalCoins={closeModalCoins}/>
            <button className='buttun-details' onClick={openModalCoins}>!</button>
            {coins.map((coin) => (
                <div key={coin.coin_name}>
                    <CustomInput
                        characterID={props.id}
                        label={coin.coin_name}
                        type='number'
                        id='coins'
                        name={coin.coin_id}
                        InputValue={coin.amount_coin}
                    />
                </div>
            ))}
        </section>
    );
}

export default Coin;
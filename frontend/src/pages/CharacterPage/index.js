import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import Navbar from '../../components/Navbar';
import CustomInput from '../../components/CustomInput';
import Characteristics from './Characteristic';

function CharacterPage(props) {
    const { id } = useParams();

    return (
        <div>
            <Navbar isLoggedIn={props.idUser} />
            <Characteristics id={id} />
        </div>
    );
}

export default CharacterPage;


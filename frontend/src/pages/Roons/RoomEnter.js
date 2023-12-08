import { useEffect, useState } from "react";
import TextInput from '../../components/TextInput';
import Button from "../../components/Button";

const RoomEnter = (props) => {
    const [roomName, setRoomName] = useState('');
    const [roomPassword, setRoomPassword] = useState('');

    const postInput = async (url, data) => {
        try {
            const response = await fetch(url, {
                method: 'POST',
                body: data,
            });
            const responseData = await response.json();
            if (responseData.result) {
                if (responseData.data) {
                    props.newRoons(responseData.data);
                    // Limpar o estado de erro ao obter dados com sucesso
                    props.setErrorReturn('');
                }
            } else {
                // Definir o estado de erro se houver um erro
                props.setErrorReturn(responseData.error);
            }
        } catch (error) {
            console.error('Erro na requisição:', error);
        }
    };

    const handleClick = (event) => {
        const buttonId = event.currentTarget.id;

        const data = new FormData();
        data.append('room_name', roomName);
        data.append('room_password', roomPassword);

        if (buttonId === 'register') {
            postInput('/room', data)
        }

        if (buttonId === 'enter') {
            postInput('/user_room', data)
        }
    };

    const handleInputName = (value) => {
        setRoomName(value);
    }

    const handleInputPassword = (value) => {
        setRoomPassword(value);
    }

    return (
        <div className="room_inputs">
            <TextInput
                name="room_name"
                required={true}
                placeholder="Digite o nome da sala"
                type="text"
                value={roomName}
                onChange={handleInputName}
            />
            <TextInput
                name="room_password"
                placeholder="Digite a senha da sala"
                type="text"
                value={roomPassword}
                onChange={handleInputPassword}
            />
            <Button id='register' onClick={handleClick}>Criar</Button>
            <Button id='enter' onClick={handleClick}>Entrar</Button>
        </div>
    );
};


export default RoomEnter;
import { useParams } from 'react-router-dom';
import Navbar from '../../components/Navbar';
import CartesianPlane from '../../components/CartesianPlane';
import { useEffect, useRef, useState } from 'react';
import socket from '../../components/Socket';
import ChatComponent from '../../components/Chat';
import './RoomPage.css'

function RoomPage(props) {
    const [userName, setUserName] = useState('');
    const [room, setRoom] = useState({})
    const { room_id, user_room_id } = useParams();
    const [showPassword, setShowPassword] = useState(false);
    const ToggleButton = useRef(null);

    useEffect(() => {
        const fetchRoomData = async () => {
            try {
                const response = await fetch(`/get_room/${room_id}`);
                const data = await response.json();
                if (data.result !== false) {
                    if (data.data !== null) {
                        setRoom(data.data);
                    }
                } else {
                    console.error('Erro ao buscar dados');
                }
            } catch (error) {
                console.error('Erro na requisição:', error);
            }
        };

        fetchRoomData();

        const fetchUser = async () => {
            try {
                const response = await fetch(`/user`);
                const data = await response.json();
                if (data.result) {
                    setUserName(data.data.user_name);
                }
            } catch (error) {
                console.error('Erro ao buscar mensagens:', error);
            }
        };

        fetchUser();

        const handleResize = () => {
            const heightNavBar = document.querySelector('.navbar').offsetHeight;
            const height = window.innerHeight;
            document.querySelector('.chat-container').style.height = `${height - heightNavBar}px`;
        };

        window.addEventListener('resize', handleResize);
        document.title = room.room_name;

        socket.emit('join', { room_id: room_id });

        return () => {
            window.removeEventListener('resize', handleResize);
            socket.emit('leave', { room_id: room_id });
        };
    }, [room_id, user_room_id, userName]);

    const handleTogglePassword = () => {
        setShowPassword((prevShowPassword) => !prevShowPassword);
        ToggleButton.current.style.backgroundImage = `url(${showPassword ? '/openimg/eye-open.png' : '/openimg/eye-close.png'})`    
    };

    if (room.background === null) {
        return <div>Loading...</div>
    }
    if (room.background != null) {
        return (
            <div>
                <Navbar isLoggedIn={props.idUser} />
                <div className='infos'>
                    <h5>Sala: {room.room_name}</h5>
                    <h5 className='password'>
                        Senha: {showPassword ? room.room_password : '********'}
                        <button ref={ToggleButton} className='button_toggle' onClick={handleTogglePassword}>
                        </button>
                    </h5>
                </div>
                <CartesianPlane room_id={room_id} user_room_id={user_room_id} background={room.background} />
                <ChatComponent room_id={room_id} user_room_id={user_room_id} user_id={props.idUser} user_name={userName} />
            </div>
        );
    }
}

export default RoomPage;

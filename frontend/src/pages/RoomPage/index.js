import { useParams } from 'react-router-dom';
import Navbar from '../../components/Navbar';
import CartesianPlane from '../../components/CartesianPlane';
import { useEffect, useState } from 'react';
import socket from '../../components/Socket';
import ChatComponent from '../../components/Chat';

function RoomPage(props) {
    const [userName, setUserName] = useState('');
    const { code_room, id } = useParams();
    console.log(code_room, id);

    useEffect(() => {
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
        document.title = `${code_room}_${userName}`;

        socket.emit('join', { room_id: code_room });

        return () => {
            window.removeEventListener('resize', handleResize);
            socket.emit('leave', { room_id: code_room });
        };
    }, [code_room, id, userName]);

    if (userName === '') {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <Navbar isLoggedIn={props.idUser} />
            <CartesianPlane room_id={code_room} user_room_id={id} />
            <ChatComponent room_id={code_room} user_room_id={id} user_id={props.idUser} user_name={userName} />
        </div>
    );
}

export default RoomPage;

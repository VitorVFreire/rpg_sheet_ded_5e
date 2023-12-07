import { useParams } from 'react-router-dom';
import Navbar from '../../components/Navbar';
import CartesianPlane from '../../components/CartesianPlane';
import { useEffect } from 'react';
import socket from '../../components/Socket';
import ChatComponent from '../../components/Chat';

function RoomPage(props) {
    const { code_room, id } = useParams();
    console.log(code_room, id);

    useEffect(() => {
        const handleResize = () => {
            const heightNavBar = document.querySelector('.navbar').offsetHeight;
            const height = window.innerHeight;
            document.querySelector('.chat-container').style.height = `${height - heightNavBar}px`;
        };

        window.addEventListener('resize', handleResize);
        document.title = `${code_room}_user_${id}`;

        socket.emit('join', { room_id: code_room });

        return () => {
            window.removeEventListener('resize', handleResize);
            socket.emit('leave', { room_id: code_room });
        };
    }, [code_room, id]);

    return (
        <div>
            <Navbar isLoggedIn={props.idUser} />
            <CartesianPlane room_id={code_room} character_id={id} />
            <ChatComponent room_id={code_room} />
        </div>
    );
}

export default RoomPage;

import { useParams } from 'react-router-dom';
import Navbar from '../../components/Navbar';
import CartesianPlane from '../../components/CartesianPlane';
import { useEffect } from 'react';
import socket from '../../components/Socket';

function RoomPage(props) {
    const { code_room, id } = useParams();
    console.log(code_room, id);

    useEffect(() => {
        socket.emit('join_cartesian', { room_id: code_room });

        return () => {
            socket.emit('leave_cartesian', { room_id: code_room });
        };
    }, [code_room]);

    return (
        <div>
            <Navbar isLoggedIn={props.idUser} />
            <CartesianPlane room_id={code_room} character_id={id}/>
        </div>
    );
}

export default RoomPage;

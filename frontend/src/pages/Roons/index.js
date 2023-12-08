import Navbar from '../../components/Navbar';
import ButtonLink from '../../components/ButtonLink';
import './Roons.css';
import { useEffect, useState } from 'react';
import RoomEnter from './RoomEnter';
import DeleteButton from '../../components/DeleteButton';

function Roons(props) {
    const [roons, setRoons] = useState([]);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const response = await fetch(`/roons`);
                const data = await response.json();
                if (data.result) {
                    setRoons(data.data);
                }
            } catch (error) {
                console.error('Erro ao buscar mensagens:', error);
            }
        };

        fetchUser();

        document.title = 'Roons';
    }, []);

    const newRoons = (item) => {
        setRoons((prevMessages) => [...prevMessages, item]);
    };

    const setErrorReturn = (item) => {
        console.log(item)
        setError(item);
    };

    const handleRoomDeleted = (outherId) => {
        const updatedRoon = roons.filter((room) => room.room_id !== outherId);
        setRoons(updatedRoon);
    };

    return (
        <div>
            <Navbar isLoggedIn={props.idUser} />
            <div className='roons_page'>
                <RoomEnter newRoons={newRoons} setErrorReturn={setErrorReturn} />
                {error && <div className='error'><h3>{error}</h3></div>}
                <div className="roons">
                    {roons.map((room, index) => (
                        <div key={index}>
                            {room.can_delete && (
                                <>
                                    <DeleteButton url='/room' keyData='room_id' outherId={room.room_id} attFunction={handleRoomDeleted} />
                                </>
                            )}
                            <h4>{room.room_name}</h4>
                            <ButtonLink link={`/room/${room.room_id}/${room.user_room_id}`} text='Entrar Sala' />
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default Roons;
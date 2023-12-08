import Navbar from '../../components/Navbar';
import ButtonLink from '../../components/ButtonLink';
import './Roons.css';
import { useEffect, useState } from 'react';
import RoomEnter from './RoomEnter';
import DeleteButton from '../../components/DeleteButton';
import Button from '../../components/Button';

function Roons(props) {
    const [roons, setRoons] = useState([]);
    const [error, setError] = useState('');

    const leaveRoom = async (roomId) => {
        try {
            const data = new FormData();
            data.append('room_id', roomId);

            const response = await fetch('/user_room', {
                method: 'DELETE',
                body: data,
            });

            if (response.ok) {
                handleRoomDeleted(roomId);
            } else {
                const responseData = await response.json();
                setError(`Erro ao sair da sala: ${responseData.error}`);
            }
        } catch (error) {
            console.error('Erro na requisição:', error);
        }
    };

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
                            <section className='roons_buttons'>
                                <ButtonLink link={`/room/${room.room_id}/${room.user_room_id}`} text='Entrar Sala' />
                                <Button children='Sair' id={room.room_id} onClick={() => leaveRoom(room.room_id)} />
                            </section>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default Roons;
import { useParams } from 'react-router-dom';
import Navbar from '../../components/Navbar';
import CartesianPlane from '../../components/CartesianPlane';

function RoomPage(props) {
    const { code_room, id } = useParams();
    console.log(code_room, id);
    return (
        <div>
            <Navbar isLoggedIn={props.idUser} />
            <CartesianPlane room_id={code_room} character_id={id}/>
        </div>
    );
}

export default RoomPage;

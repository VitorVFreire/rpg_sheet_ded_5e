import { useParams } from 'react-router-dom';
import Navbar from '../../components/Navbar';
import Equipment from './Equipment';

function AddEquipment(props) {
    const { id } = useParams();

    return (
        <div>
            <Navbar isLoggedIn={props.idUser} />
            <Equipment characterId={id} />
    </div>
  );
}

export default AddEquipment;

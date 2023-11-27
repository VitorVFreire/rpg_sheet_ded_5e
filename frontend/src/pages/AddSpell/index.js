import { useParams } from 'react-router-dom';
import Navbar from '../../components/Navbar';
import Spell from './Spell';

function AddSpell(props) {
    const { id } = useParams();

    return (
        <div>
            <Navbar isLoggedIn={props.idUser} />
            <Spell characterId={id} />
    </div>
  );
}

export default AddSpell;
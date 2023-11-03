import { useParams } from 'react-router-dom';
import Navbar from '../../components/Navbar';
import Character from './Character';
import Characteristics from './Characteristic';
import Attribute from './Attribute';
import SavingThrow from './SavingThrow';
import StatusBase from './StatusBase';
import Skill from './Skill';

function CharacterPage(props) {
    const { id } = useParams();

    return (
        <div>
            <Navbar isLoggedIn={props.idUser} />
            <Character id={id} />
            <Characteristics id={id} />
            <Attribute id={id} />
            <SavingThrow id={id} />
            <StatusBase id={id} />
            <Skill id={id} />
        </div>
    );
}

export default CharacterPage;


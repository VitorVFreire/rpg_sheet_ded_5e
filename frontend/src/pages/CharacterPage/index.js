import { useParams } from 'react-router-dom';
import './CharacterPage.css'
import Navbar from '../../components/Navbar';
import Character from './Character';
import Characteristics from './Characteristic';
import Attribute from './Attribute';
import SavingThrow from './SavingThrow';
import StatusBase from './StatusBase';
import Skill from './Skill';
import Spell from './Spell';

function CharacterPage(props) {
    const { id } = useParams();

    return (
        <div>
            <Navbar isLoggedIn={props.idUser} />
            <div className='layout'>
                <div className='header'>
                    <Character id={id} />
                    <Characteristics id={id} />
                </div>
                <div className='body'>
                    <SavingThrow id={id} />
                    <Skill id={id} />
                </div>
                <div className='leftSide'>
                    <Attribute id={id} />
                </div>
                <div className='rightSide'>
                    <StatusBase id={id} />
                </div>
                <div className='footer'>
                    <h3>Spell: </h3>
                    <Spell id={id} />
                </div>
            </div>

        </div>
    );
}

export default CharacterPage;


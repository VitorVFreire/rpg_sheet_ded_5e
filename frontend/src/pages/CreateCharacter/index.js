import './CreateCharacter.css'
import Navbar from "../../components/Navbar";
import TextInput from "../../components/TextInput"
import { useEffect } from 'react';
import DropdownList from '../../components/DropdownListMethodGet';
import Button from '../../components/Button';

function CreateCharacter(props) {
    const idUser = props.idUser;
    useEffect(() => {
        document.title = 'Criar Personagem';
    }, []);
    return (
        <div>
            <Navbar isLoggedIn={idUser} />
            <div className="create_character">
                <form action='/character' method='POST'>
                    <TextInput
                        name="character_name"
                        label="Nome"
                        id="character_name"
                        required={true}
                        placeholder="Insira um nome para o personagem"
                        type="text"
                    />
                    <DropdownList
                        url='/races'
                        label='Raça'
                        id='race_id'
                        name='race_name'
                    />
                    <DropdownList
                        url='/classes'
                        label='Classe'
                        id='class_id'
                        name='class_name'
                    />
                    <Button>
                        Criar
                    </Button>
                </form>
            </div>
        </div>
    );
}

export default CreateCharacter;
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
                <form action='/personagem' method='POST'>
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
                        id='id_raca'
                        name='nome_raca'
                    />
                    <DropdownList
                        url='/classes'
                        label='Classe'
                        id='id_classe'
                        name='nome_classe'
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
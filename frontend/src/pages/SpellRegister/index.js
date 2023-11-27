// SpellRegister.js
import React, { useEffect } from 'react';
import './SpellRegister.css';
import Navbar from '../../components/Navbar';
import TextInput from '../../components/TextInput';
import DropdownList from '../../components/DropdownListMethodGet';
import Button from '../../components/Button';

function SpellRegister(props) {
    const idUser = props.idUser;

    useEffect(() => {
        document.title = 'Cadastrar Magia';
    }, []);

    const handleSpellSubmit = async (event) => {
        event.preventDefault();

        const formData = new FormData(event.target);
        const response = await fetch('/spell_register', {
            method: 'POST',
            body: formData,
        });

        const result = await response.json();
        console.log(result); // Você pode lidar com o resultado da resposta aqui

        // Adicione lógica para lidar com a resposta, como redirecionar ou exibir uma mensagem ao usuário.
    };

    return (
        <div>
            <Navbar isLoggedIn={idUser} />
            <div className="equipment_register">
                <form onSubmit={handleSpellSubmit} encType="multipart/form-data">
                    <TextInput
                        name="spell_name"
                        label="Nome da Magia"
                        id="spell_name"
                        required={true}
                        placeholder="Insira o nome da magia"
                        type="text"
                    />
                    <TextInput
                        name="attribute_use"
                        label="Atributo de Uso"
                        id="attribute_use"
                        required={true}
                        placeholder="Insira o atributo de uso da magia"
                        type="text"
                    />
                    <TextInput
                        name="side_dice"
                        label="Quantidade de Lados"
                        id="side_dice"
                        required={false}
                        placeholder="Insira a quantidade de lados da magia"
                        type="number"
                    />
                    <TextInput
                        name="description_spell"
                        label="Descrição da Magia"
                        id="description_spell"
                        required={true}
                        placeholder="Insira a descrição da magia"
                        type="text"
                    />
                    <DropdownList
                        url="/types_damage"
                        label="Tipo de Dano"
                        id="type_damage_id"
                        name="type_damage_name"
                    />
                    <TextInput
                        name="amount_dice"
                        label="Quantidade de Dados"
                        id="amount_dice"
                        required={false}
                        placeholder="Insira a quantidade de dados da magia"
                        type="number"
                    />
                    <TextInput
                        name="spell_level"
                        label="Nível da Magia"
                        id="spell_level"
                        required={true}
                        placeholder="Insira o nível da magia"
                        type="number"
                    />
                    <TextInput
                        name="add_per_level"
                        label="Incremento por Nível"
                        id="add_per_level"
                        required={true}
                        placeholder="Insira o incremento por nível da magia"
                        type="number"
                    />
                    <Button>
                        Criar
                    </Button>
                </form>
            </div>
        </div>
    );
}

export default SpellRegister;

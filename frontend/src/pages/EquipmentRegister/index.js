import './EquipmentRegister.css'
import Navbar from "../../components/Navbar";
import TextInput from "../../components/TextInput"
import { useEffect } from 'react';
import DropdownList from '../../components/DropdownListMethodGet';
import Button from '../../components/Button';

function EquipmentRegister(props) {
    const idUser = props.idUser;
    useEffect(() => {
        document.title = 'Cadastrar Equipamento';
    }, []);
    return (
        <div>
            <Navbar isLoggedIn={idUser} />
            <div className="equipment_register">
                <form action='/equipment_register' method='POST'>
                    <TextInput
                        name="equipment_name"
                        label="Nome do Equipamento"
                        id="equipment_name"
                        required={true}
                        placeholder="Insira o nome do equipamento"
                        type="text"
                    />
                    <TextInput
                        name="description_equipment"
                        label="Descrição do Equipamento"
                        id="description_equipment"
                        required={true}
                        placeholder="Insira a descrição do equipamento"
                        type="text"
                    />
                    <TextInput
                        name="price"
                        label="Preço"
                        id="price"
                        required={true}
                        placeholder="Insira o Preço do Equipamento"
                        type="number"
                    />
                    <DropdownList
                        url='/coins'
                        label='Selecione a moeda'
                        id='coin_id'
                        name='coin_name'
                    />
                    <TextInput
                        name="weight"
                        label="Tamanho"
                        id="weight"
                        required={true}
                        placeholder="Insira o Tamanho do Equipamento"
                        type="number"
                    />
                    <TextInput
                        name="armor_class"
                        label="CA"
                        id="armor_class"
                        required={false}
                        placeholder="Insira a CA do Equipamento"
                        type="number"
                    />
                    <TextInput
                        name="amount_dice"
                        label="Quantidade de Dados"
                        id="amount_dice"
                        required={false}
                        placeholder="Insira a Quantidade de Dados do Equipamento"
                        type="number"
                    />
                    <TextInput
                        name="side_dice"
                        label="Quantidade de Lados"
                        id="side_dice"
                        required={false}
                        placeholder="Insira a Quantidade de Lados do Equipamento"
                        type="number"
                    />
                    <TextInput
                        name="bonus"
                        label="Bonus"
                        id="bonus"
                        required={false}
                        placeholder="Insira o Bonus do Equipamento"
                        type="number"
                    />
                    <TextInput
                        name="equipment_image"
                        label="Imagem do Equipamento"
                        id="equipment_image"
                        required={false}
                        type="file"
                    />
                    <DropdownList
                        url='/types_damage'
                        label='Selecione o tipo de dano'
                        id='type_damage_id'
                        name='type_damage_name'
                    />
                    <DropdownList
                        url='/kind_equipments'
                        label='Selecione o tipo de equipamento'
                        id='kind_equipment_id'
                        name='kind_equipment_name'
                    />
                    <Button>
                        Criar
                    </Button>
                </form>
            </div>
        </div>
    );
}

export default EquipmentRegister;
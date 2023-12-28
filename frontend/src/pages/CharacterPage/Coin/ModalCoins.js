import Modal from 'react-modal';
import './Coin.css'

const customStyles = {
    content: {
        top: '50%',
        left: '50%',
        right: 'auto',
        bottom: 'auto',
        marginRight: '-50%',
        transform: 'translate(-50%, -50%)',
        backgroundColor: 'antiquewhite',
        MaxWidth: '800px',
        maxHeight: '200px',
        overflow: 'auto'
    },
};

function ModalCoins(props) {
    return (
        <div className='modal_spell'>
            <Modal
                isOpen={props.ModalCoinsIsOpen}
                onRequestClose={props.closeModalCoins}
                style={customStyles}
                contentLabel="Coins"
            >
                <button className='button_close_modal' onClick={props.closeModalCoins}>X</button>
                <div className='details-coins'>
                    <table>
                        <thead>
                            <tr>
                                <th>Moeda</th>
                                <th>Quantidade</th>
                                <th>Outra Moeda</th>
                                <th>Valor Convertido</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>
                                    DA
                                </td>
                                <td>
                                    1
                                </td>
                                <td>
                                    PL
                                </td>
                                <td>
                                    100
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    PL
                                </td>
                                <td>
                                    1
                                </td>
                                <td>
                                    PO
                                </td>
                                <td>
                                    10
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    PO
                                </td>
                                <td>
                                    1
                                </td>
                                <td>
                                    PP
                                </td>
                                <td>
                                    10
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    PP
                                </td>
                                <td>
                                    1
                                </td>
                                <td>
                                    PC
                                </td>
                                <td>
                                    10
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </Modal>
        </div>
    );
}

export default ModalCoins;
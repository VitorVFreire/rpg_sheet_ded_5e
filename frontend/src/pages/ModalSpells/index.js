import Spell from './Spell';
import Modal from 'react-modal';

const customStyles = {
  content: {
    top: '50%',
    left: '50%',
    right: 'auto',
    bottom: 'auto',
    marginRight: '-50%',
    transform: 'translate(-50%, -50%)',
  },
};

function ModalSpells(props) {
  return (
    <div>
      <Modal
        isOpen={props.modalSpellsIsOpen}
        onRequestClose={props.closeModalSpells}
        style={customStyles}
        contentLabel="Spells"
      >
        <button onClick={props.closeModalSpells}>close</button>
        <Spell characterId={props.id} />
      </Modal>
    </div>
  );
}

/*function ModalSpells(props) {
    const { id } = useParams();

    return (
        <div>
            
    </div>
  );
}*/

export default ModalSpells;
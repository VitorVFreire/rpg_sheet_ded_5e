import Spell from './Spell';
import Modal from 'react-modal';
import './Spell.css'

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

function ModalSpells(props) {
  return (
    <div className='modal_spell'>
      <Modal
        isOpen={props.modalSpellsIsOpen}
        onRequestClose={props.closeModalSpells}
        style={customStyles}
        contentLabel="Spells"
      >
        <button className='button_close_modal' onClick={props.closeModalSpells}>X</button>
        <Spell characterId={props.id} />
      </Modal>
    </div>
  );
}

export default ModalSpells;
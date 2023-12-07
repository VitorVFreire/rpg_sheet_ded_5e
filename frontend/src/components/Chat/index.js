import React, { useState, useEffect, useRef } from 'react';
import './Chat.css';
import socket from '../Socket';
import DropdownList from '../DropdownListMethodGet';

const ChatComponent = (props) => {
  const [messages, setMessages] = useState([]);
  const [messageInput, setMessageInput] = useState('');
  const [offSet, setOffSet] = useState('');
  const [idUserMessage, setIdUserMessage] = useState({ 'user_id': props.user_id, 'name': props.user_name });
  const messagesContainerRef = useRef(null);

  useEffect(() => {
    const fetchMessages = async () => {
      try {
        const response = await fetch(`/messages/room=${props.room_id}`);
        const data = await response.json();
        if (data.result) {
          setMessages(data.data.messages);
          setOffSet(data.data.offset);
        }
      } catch (error) {
        console.error('Erro ao buscar mensagens:', error);
      }
    };

    fetchMessages();

    socket.on('message', (data) => {
      const message = data.message;
      const name = data.name;
      setMessages((prevMessages) => [...prevMessages, { 'message': message, 'name': name }]);
      // Mover o scroll para a parte inferior ao adicionar uma nova mensagem
      messagesContainerRef.current.scrollTop = messagesContainerRef.current.scrollHeight;
    });

  }, [props.room]);

  const sendMessage = () => {
    if (messageInput.trim() !== '') {
      socket.emit('message', { room_id: props.room_id, id: idUserMessage, message: messageInput });
      setMessageInput('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      sendMessage();
    }
  };

  const handleSelectItem = (id, name) => {
    if (id !== '') {
      setIdUserMessage({ 'character_id': id, 'name': name });
    } else {
      setIdUserMessage({ 'user_id': props.user_id, 'name': props.user_name });
    }
  }

  return (
    <section className='chat'>
      <div className="chat-dropdown-container">
        <DropdownList
          url='/characters'
          label='Personagem'
          id='character_id'
          name='character_name'
          className='dropdowncartesian'
          handleSelectItem={handleSelectItem}
        />
        <div className="chat-container">
          <div className="messages" ref={messagesContainerRef}>
            {messages.map((message, index) => (
              <div key={index}>{`${message['name']}`} - {`${message['message']}`}</div>
            ))}
          </div>

          <div className="input-container">
            <input
              type="text"
              placeholder="Message"
              value={messageInput}
              onChange={(e) => setMessageInput(e.target.value)}
              onKeyPress={handleKeyPress}
            />
            <button onClick={sendMessage}>Send Message</button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ChatComponent;
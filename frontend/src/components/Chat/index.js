import React, { useState, useEffect, useRef } from 'react';
import './Chat.css';
import socket from '../Socket';

const ChatComponent = (props) => {
  const [messages, setMessages] = useState([]);
  const [messageInput, setMessageInput] = useState('');
  const messagesContainerRef = useRef(null);

  useEffect(() => {
    const fetchMessages = async () => {
      try {
        const response = await fetch(`/messages/room=${props.room_id}`);
        const data = await response.json();
        const newMessages = data.messages || [];
        setMessages(newMessages);
      } catch (error) {
        console.error('Erro ao buscar mensagens:', error);
      }
    };

    fetchMessages();

    socket.on('message', (data) => {
      const message = data.message;
      setMessages((prevMessages) => [...prevMessages, { message }]);
      // Mover o scroll para a parte inferior ao adicionar uma nova mensagem
      messagesContainerRef.current.scrollTop = messagesContainerRef.current.scrollHeight;
    });

  }, [props.room]);

  const sendMessage = () => {
    if (messageInput.trim() !== '') {
      socket.emit('message', { room_id: props.room_id, message: messageInput });
      setMessageInput('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="chat-container">
      <div className="messages" ref={messagesContainerRef}>
        {messages.map((message, index) => (
          <div key={index}>{`${message.message}`}</div>
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
  );
};

export default ChatComponent;
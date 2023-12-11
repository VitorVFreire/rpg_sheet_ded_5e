import React, { useState, useEffect, useRef } from 'react';
import './Chat.css';
import socket from '../Socket';
import DropdownList from '../DropdownListMethodGet';

const ChatComponent = (props) => {
  const [messages, setMessages] = useState([]);
  const [messageInput, setMessageInput] = useState('');
  const [offSet, setOffSet] = useState(0);
  const [getOldMessages, setGetOldMessages] = useState(0);
  const [loadAllScroll, setLoadAllScroll] = useState(0);
  const [loadingOldMessages, setLoadingOldMessages] = useState(false);
  const [isUserMessageSender, setIsUserMessageSender] = useState(false);
  const [startScrollMessages, setStartScrollMessages] = useState(0);
  const messagesContainerRef = useRef(null);
  const [idUserMessage, setIdUserMessage] = useState({ 'user_id': props.user_id, 'name': props.user_name });

  useEffect(() => {
    const fetchMessages = async () => {
      try {
        const response = await fetch(`/messages/room=${props.room_id}`);
        const data = await response.json();
        if (data.result) {
          setMessages(data.data.messages);
          setOffSet(data.data.offset);
          setStartScrollMessages((prevStartScrollMessages) => prevStartScrollMessages + 1);
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
      setOffSet((prevOffSet) => prevOffSet + 1);
    });

    if (messagesContainerRef.current) {
      mutationObserver.observe(messagesContainerRef.current, {
        childList: true,
        subtree: true,
      });

      return () => {
        mutationObserver.disconnect();
      };
    }
  }, [props.room]);

  useEffect(() => {
    const fetchOldMessages = async () => {
      try {
        setLoadingOldMessages(true); // Define como true ao começar a carregar mensagens antigas
        setGetOldMessages((prevGetOldMessages) => prevGetOldMessages + 1);
        const response = await fetch(`/messages/room=${props.room_id}?offset=${offSet}`);
        const responseData = await response.json();
        if (responseData.result) {
          setMessages((prevMessages) => [...responseData.data.messages, ...prevMessages]);
          setOffSet(responseData.data.offset);
        }
      } catch (error) {
        console.error('Erro ao buscar mensagens:', error);
      } finally {
        setLoadingOldMessages(false); // Define como false quando terminar o carregamento
      }
    };

    if (messagesContainerRef.current) {
      if (startScrollMessages === 1) {
        calculeteScroll();
        setStartScrollMessages(startScrollMessages + 1);
      }

      if (isUserMessageSender === true) {
        calculeteScroll();
        setIsUserMessageSender(false);
      }
    }

    const handleScroll = () => {
      if (messagesContainerRef.current.scrollTop === (messagesContainerRef.current.scrollHeight - messagesContainerRef.current.clientHeight)) {
        setLoadAllScroll((prevLoadAllScroll) => prevLoadAllScroll + 1);
        if (getOldMessages > 1) {
          setGetOldMessages(0);
        }
      }
      if ((messagesContainerRef.current.scrollTop < 40 && messagesContainerRef.current.scrollTop > 30) && startScrollMessages > 1 && loadAllScroll > 0 && getOldMessages === 0) {
        fetchOldMessages();
      }
    };

    messagesContainerRef.current.addEventListener('scroll', handleScroll);

    return () => {
      messagesContainerRef.current.removeEventListener('scroll', handleScroll);
    };
  }, [startScrollMessages, loadAllScroll, messages, isUserMessageSender]);

  const mutationObserver = new MutationObserver(async () => {
    if (messagesContainerRef.current.scrollTop > (messagesContainerRef.current.scrollHeight / 3)) {
      calculeteScroll();
    }
  });

  function calculeteScroll() {
    messagesContainerRef.current.scrollTop = messagesContainerRef.current.scrollHeight - messagesContainerRef.current.clientHeight;
  }

  const sendMessage = () => {
    if (messageInput.trim() !== '') {
      socket.emit('message', { room_id: props.room_id, id: idUserMessage, message: messageInput });
      setMessageInput('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      setIsUserMessageSender(true);
      sendMessage();
    }
  };

  const handleSelectItem = (id, name) => {
    if (id !== '') {
      setIdUserMessage({ 'character_id': id, 'name': name });
    } else {
      setIdUserMessage({ 'user_id': props.user_id, 'name': name });
    }
  };

  return (
    <section className='chat'>
      <div className="chat-dropdown-container">
        <DropdownList
          url='/characters'
          label={props.user_name}
          id='character_id'
          name='character_name'
          className='dropdowncartesian'
          handleSelectItem={handleSelectItem}
        />
        <div className="chat-container">
          <div className="messages" ref={messagesContainerRef}>
            {loadingOldMessages && <div>Loading...</div>}
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

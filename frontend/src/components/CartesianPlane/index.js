import './cartesian_plane.css';
import React, { useState, useEffect } from "react";
import socket from '../Socket';
import ButtonAdd from '../ButtonAdd';
import RoundImageButton from '../RoundImageButton';

function CartesianPlane(props) {
  const [isDragging, setIsDragging] = useState(false);
  const [draggedSquare, setDraggedSquare] = useState(null);
  const [squares, setSquares] = useState([]);
  const [background, setBackground] = useState(null);
  const gridSize = 50;

  useEffect(() => {
    async function fetchSquares() {
      try {
        const response = await fetch('/squares/' + props.room_id);
        const data = await response.json();
        if (data.result !== false) {
          if (data.data !== null) {
            setSquares(data.data);
          }
          setBackground(data.background);
        } else {
          console.error('Erro ao buscar dados');
        }
      } catch (error) {
        console.error('Erro na requisição:', error);
      }
    }

    fetchSquares();

    socket.on('update_square', (updatedSquare) => {
      setSquares((prevSquares) =>
        prevSquares.map((square) =>
          square.square_id === updatedSquare.square_id
            ? { ...square, x: updatedSquare.x, y: updatedSquare.y }
            : square
        )
      );
    });

    socket.on('new_background', (new_background) => {
      setBackground(new_background.background_image);
    });

    socket.on('new_squares', (new_squares) => {
      setSquares((prevSquares) => [...prevSquares, new_squares]);
    });

    socket.on('update_squares', (updated_squares) => {
      const elements = document.querySelectorAll(`.square[data-key="${updated_squares.square_id}"]`);

      if (elements) {
        elements.forEach((element) => {
          element.style.backgroundImage = `url('${updated_squares.square_image}')`;
        });
      }
    });

    socket.on('delete_square', (delete_square) => {
      const id = delete_square.square_id;
      console.log('Before deletion:', squares);
      setSquares((prevSquares) =>
        prevSquares.filter((square) => square.square_id != id)
      );
      console.log('After deletion:', squares);
    });

  }, [props.room_id]);

  const handleMouseDown = (id) => {
    setIsDragging(true);
    setDraggedSquare(id);
    // Atualize apenas o quadrado que está sendo arrastado
    setSquares((prevSquares) =>
      prevSquares.map((square) =>
        square.square_id === id ? { ...square, isDragging: true } : square
      )
    );
  };

  const handleMouseUp = () => {
    setIsDragging(false);
    // Obtenha o quadrado movido com base no ID
    const movedSquare = squares.find((square) => square.square_id === draggedSquare);
    setDraggedSquare(null);
    // Reinicie o status de arrastar para todos os quadrados
    setSquares((prevSquares) =>
      prevSquares.map((square) => ({ ...square, isDragging: false }))
    );

    if (movedSquare) {
      socket.emit('new_square_position', {
        room_id: props.room_id,
        character_id: props.character_id,
        square_id: movedSquare.square_id,
        x: movedSquare.x,
        y: movedSquare.y
      });
    }
  };

  const handleMouseMove = (e, id) => {
    if (isDragging) {
      const x = Math.floor(e.clientX / gridSize);
      const y = Math.floor(e.clientY / gridSize);
      if (x <= 10 && y <= 10)
        setSquares((prevSquares) =>
          prevSquares.map((square) =>
            square.square_id === id && square.isDragging
              ? { ...square, x, y }
              : square
          )
        );
      socket.emit('update_coordinates', {
        room_id: props.room_id,
        character_id: props.character_id,
        square_id: id,
        x,
        y
      });
    }
  };

  if (background === null) {
    return <div>Loading...</div>;
  }

  return (
    <div className="App">
      <div className="container">
        <div
          className="cartesian-plane"
          style={{
            backgroundImage: `url('${background}')`,
            backgroundSize: 'cover',
          }}
          onMouseUp={handleMouseUp}
          onMouseMove={(e) => {
            handleMouseMove(e, draggedSquare);
          }}
        >
          {Array.from({ length: 10 }, (_, rowIndex) =>
            Array.from({ length: 10 }, (_, colIndex) => (
              <div
                key={`${rowIndex}-${colIndex}`}
                className="grid-square"
                style={{
                  left: `${colIndex * gridSize}px`,
                  top: `${rowIndex * gridSize}px`,
                }}
              ></div>
            ))
          )}
          {squares.map((square) => (
            <div
              key={square.square_id}
              className="square"
              data-key={square.square_id}
              style={{
                left: `${square.x * gridSize}px`,
                top: `${square.y * gridSize}px`,
                backgroundImage: `url('${square.square_image}')`,
                backgroundSize: 'cover',
                position: 'absolute',
                cursor: 'pointer',
              }}
              onMouseDown={() => handleMouseDown(square.square_id)}
            >
              {square.square_id}
            </div>
          ))}
        </div>
        <div className='buttons'>
          <ButtonAdd
            url={`/squares/${props.room_id}`}
            value={props.character_id}
            method={'POST'}
          />
          <RoundImageButton
            imageUrl="http://localhost:8085/openimg/ilustracao.png"
            url={`/background_cartesian_plane/${props.room_id}`}
            method={'PUT'}
          />
        </div>
      </div>

      {squares.map((square) => (
        <div className='square-list' key={square.square_id}>
          <div
            className="square"
            data-key={square.square_id}
            style={{
              backgroundImage: `url('${square.square_image}')`,
              backgroundSize: 'cover',
            }}
          >
            {square.square_id}
          </div>
          <RoundImageButton
            imageUrl="http://localhost:8085/openimg/img.png"
            url={`/squares/${props.room_id}`}
            square_id={square.square_id}
            method={'PUT'}
          />
          <ButtonAdd
            url={`/squares/${props.room_id}`}
            value={square.square_id}
            method={'DELETE'}
          />
        </div>
      ))}
    </div>
  );
}

export default CartesianPlane;


import './cartesian_plane.css';
import React, { useState, useEffect } from "react";
import io from 'socket.io-client';

const socket = io('http://localhost:8085');

function CartesianPlane(props) {
  const [isDragging, setIsDragging] = useState(false);
  const [draggedSquare, setDraggedSquare] = useState(null);
  const [squares, setSquares] = useState([]);
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
        } else {
          console.error('Erro ao buscar dados');
        }
      } catch (error) {
        console.error('Erro na requisição:', error);
      }
    }

    fetchSquares();
  }, [props.room_id]);

  const handleMouseDown = (id) => {
    setIsDragging(true);
    setDraggedSquare(id);
    // Atualize apenas o quadrado que está sendo arrastado
    setSquares((prevSquares) =>
      prevSquares.map((square) =>
        square.id === id ? { ...square, isDragging: true } : square
      )
    );
  };

  const handleMouseUp = () => {
    setIsDragging(false);
    // Obtenha o quadrado movido com base no ID
    const movedSquare = squares.find((square) => square.id === draggedSquare);
    setDraggedSquare(null);
    // Reinicie o status de arrastar para todos os quadrados
    setSquares((prevSquares) =>
      prevSquares.map((square) => ({ ...square, isDragging: false }))
    );
    // Imprima o id, x e y do quadrado movido após ser solto
    if (movedSquare) {
      socket.emit('new_square_position', {
        room_id: props.room_id,
        character_id: props.character_id,
        square_id: movedSquare.id,
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
            square.id === id && square.isDragging
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

  return (
    <div className="App">
      <div
        className="cartesian-plane"
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
            key={square.id}
            className="square"
            style={{
              left: `${square.x * gridSize}px`,
              top: `${square.y * gridSize}px`,
              backgroundImage: `url('${square.url}')`,
              backgroundSize: 'cover', // ou 'contain', dependendo do efeito desejado
              position: 'absolute',
              cursor: 'pointer',
            }}
            onMouseDown={() => handleMouseDown(square.id)}
          >
            {square.id}
          </div>
        ))}
      </div>
    </div>
  );
}

export default CartesianPlane;

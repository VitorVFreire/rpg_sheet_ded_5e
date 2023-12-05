import './cartesian_plane.css';
import { useState } from "react";

function CartesianPlane() {
  const [isDragging, setIsDragging] = useState(false);
  const [draggedSquare, setDraggedSquare] = useState(null);
  const [squares, setSquares] = useState([
    { id: 0, x: 0, y: 0 },
    { id: 1, x: 1, y: 1 }
  ]);
  const gridSize = 50;

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
      console.log(`id: ${movedSquare.id} X:${movedSquare.x} Y:${movedSquare.y}`);
    }
  };

  const handleMouseMove = (e, id) => {
    if (isDragging) {
      const x = Math.floor(e.clientX / gridSize);
      const y = Math.floor(e.clientY / gridSize);
      setSquares((prevSquares) =>
        prevSquares.map((square) =>
          square.id === id && square.isDragging
            ? { ...square, x, y }
            : square
        )
      );
      console.log(`Movendo: id: ${id} ${x} ${y}`)
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
            }}
            onMouseDown={() => handleMouseDown(square.id)}
          >{square.id}</div>
        ))}
      </div>
    </div>
  );
}

export default CartesianPlane;

import React, { useState } from 'react';
import './cartesian_plane.css';

function CartesianPlane() {
      const [isDragging, setIsDragging] = useState(false);
      const [position, setPosition] = useState({ x: 0, y: 0 });
      const gridSize = 50;
    
      const handleMouseDown = (e) => {
        setIsDragging(true);
      };
    
      const handleMouseUp = (e) => {
        setIsDragging(false);
      };
    
      const handleMouseMove = (e) => {
        if (isDragging) {
          const x = Math.floor(e.clientX / gridSize);
          const y = Math.floor(e.clientY / gridSize);
          setPosition({ x, y });
        }
      };
    
      return (
        <div className="App">
          <div
            className="cartesian-plane"
            onMouseUp={handleMouseUp}
            onMouseMove={handleMouseMove}
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
            <div
              className="square"
              style={{
                left: `${position.x * gridSize}px`,
                top: `${position.y * gridSize}px`,
              }}
              onMouseDown={handleMouseDown}
            ></div>
          </div>
        </div>
      );
    }
export default CartesianPlane;

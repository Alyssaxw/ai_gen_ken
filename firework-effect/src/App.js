import React from 'react';
import FireworkEffect from './components/FireworkEffect';
import './App.css';

function App() {
  return (
    <div className="App">
      <div className="instructions">
        Click anywhere on the screen to create fireworks!
      </div>
      <FireworkEffect />
    </div>
  );
}

export default App;